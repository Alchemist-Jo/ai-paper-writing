#!/usr/bin/env python3
"""Deterministic scan of a LaTeX paper for the paper-checklist skill.

Follows \\input and \\include from the main file, tracks the section each line
belongs to, and reports candidate problems. Every hit is a candidate: the
agent confirms it against the manuscript's own conventions before reporting.

Output goes to stdout, one hit per line (TSV by default, or JSON).
A summary of detected sections and hit counts goes to stderr.

Columns: check, tier, owner, location, excerpt, message
Tiers:   submit (blocks submission), clarity (affects understanding),
         local (local wording or layout), info (context for the agent)

Examples:
  python3 scan.py main.tex
  python3 scan.py main.tex --format json > hits.json
  python3 scan.py main.tex --method-titles "Our Approach,Framework"
  python3 scan.py main.tex --only method-digit,wrap-float
"""

import argparse
import json
import os
import re
import sys

FLOAT_ENVS = {
    "figure", "figure*", "table", "table*", "wrapfigure", "wraptable",
    "subfigure", "subtable", "algorithm", "algorithm*", "SCfigure", "sidewaystable",
}
MATH_ENVS = {
    "equation", "equation*", "align", "align*", "gather", "gather*",
    "multline", "multline*", "flalign", "flalign*", "eqnarray", "eqnarray*",
    "displaymath", "math",
}
SKIP_ENVS = {"verbatim", "lstlisting", "minted", "comment", "Verbatim"}
LIST_ENVS = {"itemize", "enumerate", "description"}
TABULAR_ENVS = {"tabular", "tabular*", "tabularx", "tabulary", "longtable", "tblr"}

BANNED_OPENERS = [
    "It is worth noting", "Notably", "Specifically", "In particular",
    "In recent years", "With the rapid development",
]
BANNED_WORDS = [
    r"leverag(?:e|es|ed|ing)", r"utiliz(?:e|es|ed|ing|ation)", r"delv(?:e|es|ed|ing)",
    r"pivotal", r"showcas(?:e|es|ed|ing)", r"underscor(?:e|es|ed|ing)", r"intricate",
    r"plays? a crucial role", r"attracted increasing attention", r"seamless(?:ly)?",
    r"groundbreaking", r"revolutionary", r"paradigm shift", r"a myriad of", r"a plethora of",
]
PROCESS_PATTERNS = [
    r"\bpending\b", r"\bongoing\b", r"\bwork in progress\b", r"\bwill be updated\b",
    r"\bto be updated\b", r"\barchived\b", r"\bhistorical (?:run|result|checkpoint)s?\b",
    r"\b(?:previous|earlier|old|historical) checkpoints?\b", r"\bsingle seed\b",
    r"\bas of\b", r"\b20\d\d-\d\d-\d\d\b",
    r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, 20\d\d\b",
    r"(?<![A-Za-z\-])v\d+(?:\.\d+)?\b",
]
PENDING_PATTERNS = [
    r"\bTODO\b", r"\bTBD\b", r"\bFIXME\b", r"\bXXX\b", r"\\todo\b", r"\[cite\]", r"\?\?",
]
SECRET_PATTERNS = [
    r"sk-[A-Za-z0-9_\-]{20,}", r"ghp_[A-Za-z0-9]{30,}", r"hf_[A-Za-z0-9]{30,}",
    r"AKIA[0-9A-Z]{16}", r"xox[abprs]-[A-Za-z0-9\-]{10,}",
]
OWNER_BY_KIND = {
    "abstract": "paper-opening", "intro": "paper-opening", "related": "paper-opening",
    "method": "paper-method", "experiments": "paper-experiments",
    "analysis": "paper-experiments",
}

ENV_RE = re.compile(r"\\(begin|end)\{([^}]+)\}")
INPUT_RE = re.compile(r"\\(?:input|include)\{([^}]+)\}")
SECTION_RE = re.compile(r"\\section\*?\{(.*)\}")
HEADING_RE = re.compile(r"\\(?:sub)*section\*?\{")
CITE_RE = re.compile(r"\\cite[a-zA-Z]*\*?(?:\[[^\]]*\])*\{([^}]*)\}")
REF_RE = re.compile(r"\\(ref|eqref|cref|Cref|autoref)\{([^}]*)\}")


def strip_comment(line):
    return re.sub(r"(?<!\\)%.*$", "", line)


def resolve(base_dir, name):
    path = os.path.join(base_dir, name)
    if not os.path.splitext(path)[1]:
        path += ".tex"
    return path


def load(path, base_dir, seen, out):
    """Expand \\input and \\include recursively into (file, lineno, text) tuples."""
    real = os.path.realpath(path)
    if real in seen:
        return
    seen.add(real)
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            lines = handle.read().splitlines()
    except OSError as err:
        print(f"warning: cannot read {path}: {err}", file=sys.stderr)
        return
    rel = os.path.relpath(path, base_dir)
    for number, raw in enumerate(lines, 1):
        text = strip_comment(raw)
        match = INPUT_RE.search(text)
        if match:
            before = text[: match.start()]
            if before.strip():
                out.append((rel, number, before))
            load(resolve(base_dir, match.group(1)), base_dir, seen, out)
            after = text[match.end():]
            if after.strip():
                out.append((rel, number, after))
            continue
        out.append((rel, number, text))


def classify(title, filename, method_titles):
    low = title.lower()
    if any(t and t.lower() == low.strip() for t in method_titles):
        return "method"
    if re.search(r"statement|ethics|reproducibility|acknowledg|llm usage|ai use", low):
        return "statement"
    if "introduction" in low:
        return "intro"
    if "related" in low:
        return "related"
    if re.search(r"method|approach|methodology|framework|formulation|preliminar", low):
        return "method"
    if re.search(r"experiment|evaluation|results", low):
        return "experiments"
    if re.search(r"analysis|discussion", low):
        return "analysis"
    if "conclusion" in low:
        return "conclusion"
    if "method" in filename.lower():
        return "method"
    return "other"


def prose_part(text):
    """Remove inline math and return (prose, list_of_inline_math)."""
    maths = re.findall(r"\$[^$]+\$|\\\(.*?\\\)", text)
    prose = re.sub(r"\$[^$]+\$|\\\(.*?\\\)", " MATH ", text)
    return prose, maths


def strip_nonnumeric_args(text):
    """Remove command arguments whose digits are not manuscript numbers."""
    text = re.sub(r"\\(?:label|ref|eqref|cref|Cref|autoref|pageref|cite[a-zA-Z]*|url|href|input|include|"
                  r"includegraphics|vspace|hspace|setlength|addtolength|fontsize|captionsetup|"
                  r"cmidrule|cline|color|textcolor|definecolor|rule|raisebox|resizebox|scalebox|"
                  r"multicolumn|multirow|arraystretch|tabcolsep)(?![a-zA-Z])\*?"
                  r"(?:\([^)]*\))?(?:\[[^\]]*\])*(?:\{[^{}]*\})*", " ", text)
    text = re.sub(r"\\begin\{[^}]*\}(?:\[[^\]]*\])*(?:\{[^{}]*\})*", " ", text)
    text = re.sub(r"\\end\{[^}]*\}", " ", text)
    text = re.sub(r"\\\\(?:\[[^\]]*\])?", " ", text)
    text = re.sub(r"\[[^\]]*\]", " ", text)
    return text


def excerpt(text, width=110):
    text = " ".join(text.split())
    return text if len(text) <= width else text[: width - 3] + "..."


class Scanner:
    def __init__(self, args, lines, base_dir):
        self.args = args
        self.lines = lines
        self.base_dir = base_dir
        self.hits = []
        self.only = set(args.only.split(",")) if args.only else None
        self.method_titles = [t.strip() for t in (args.method_titles or "").split(",")]
        self.math_envs = set(MATH_ENVS)
        self.bib_files = []
        self.cited = set()
        self.sections = []
        self.tables = []
        self.wrap_neg = []

    def hit(self, check, tier, owner, loc, text, message):
        if self.only and check not in self.only:
            return
        self.hits.append({
            "check": check, "tier": tier, "owner": owner,
            "location": f"{loc[0]}:{loc[1]}" if loc[1] != "" else loc[0],
            "excerpt": excerpt(text), "message": message,
        })

    def preamble(self, upto):
        for _, _, text in self.lines[:upto]:
            for name, body in re.findall(r"\\newenvironment\{([^}]+)\}(?:\[\d\])?\{(.*)", text):
                if re.search(r"\\begin\{(equation|align|gather|multline)", body):
                    self.math_envs.add(name)
            for match in re.finditer(r"\\(?:bibliography|addbibresource)\{([^}]+)\}", text):
                self.bib_files.extend(b.strip() for b in match.group(1).split(","))

    def run(self):
        start = next((i for i, (_, _, t) in enumerate(self.lines) if "\\begin{document}" in t), 0)
        self.preamble(start)
        for _, _, text in self.lines[start:]:
            for match in re.finditer(r"\\(?:bibliography|addbibresource)\{([^}]+)\}", text):
                self.bib_files.extend(b.strip() for b in match.group(1).split(","))
        for fname, number, text in self.lines:
            for match in re.finditer(r"\\[a-z]*finalcopy\b|\\usepackage\[(?:final|preprint|accepted)\]", text):
                self.hit("anon-option", "info", "paper-typesetting", (fname, number), match.group(0),
                         "非匿名版本选项，投稿版需确认已关闭")
        self.body(start)
        if self.wrap_neg:
            self.hit("wrap-caption", "clarity", "paper-typesetting", (self.wrap_neg[0], ""),
                     f"{len(self.wrap_neg)} 个绕排浮动体", "图注之后有负 \\vspace，wrapfig 按缩小后的高度预留行数，"
                     f"图注可能压住下方正文，需在渲染页逐个确认：{', '.join(self.wrap_neg)}")
        self.check_tables()
        self.check_bib()

    def body(self, start):
        kind = "front"
        envs = []
        in_appendix = False
        last_opener = None
        wrap = None  # dict(loc, env, chars, limit) while a wrapped float's span is open
        wrap_float = None  # dict(loc, env, caption, neg, limit) inside a wrapped float
        abstract_sentences = []
        list_ok_until = -1
        table = None
        float_label = None
        float_tables = []

        for index in range(start, len(self.lines)):
            fname, number, text = self.lines[index]
            loc = (fname, number)
            if "\\end{document}" in text:
                break
            if not text.strip():
                last_opener = None
                continue
            if "\\appendix" in text:
                in_appendix = True
                kind = "appendix"
            if wrap_float is not None:
                if "\\caption" in text:
                    wrap_float["caption"] = True
                if wrap_float["caption"] and re.search(r"\\vspace\*?\{\s*-", text):
                    wrap_float["neg"] = True

            sec = SECTION_RE.search(text)
            if sec:
                title = re.sub(r"\\[a-zA-Z]+\{?|\}", "", sec.group(1))
                kind = "appendix" if in_appendix else classify(title, fname, self.method_titles)
                self.sections.append((f"{fname}:{number}", title.strip(), kind))
                if kind == "statement" and re.search(r"acknowledg", title, re.I):
                    self.hit("anon-ack", "submit", "paper-typesetting", loc, text, "匿名投稿含致谢部分")

            for action, name in ENV_RE.findall(text):
                if action == "begin":
                    envs.append(name)
                    if name == "abstract":
                        kind = "abstract"
                    if name in LIST_ENVS and kind not in ("appendix", "statement") and not in_appendix:
                        if not (kind == "intro" and index <= list_ok_until):
                            self.hit("list-in-prose", "local", "paper-language", loc, text,
                                     "正文列表（贡献列表除外）")
                    if name in FLOAT_ENVS:
                        float_label = None
                        float_tables = []
                    if name in TABULAR_ENVS:
                        table = {"loc": f"{fname}:{number}", "lines": [], "float_label": None,
                                 "appendix": in_appendix}
                    if name in ("wrapfigure", "wraptable"):
                        given = re.search(r"\\begin\{wrap(?:figure|table)\}\[(\d+)\]", text)
                        wrap_float = {"loc": f"{fname}:{number}", "env": name, "caption": False, "neg": False,
                                      "limit": int(given.group(1)) * 70 if given else self.args.wrap_chars}
                    if wrap and (name in self.math_envs or name in LIST_ENVS):
                        self.wrap_hit(wrap, loc, text, "行间公式" if name in self.math_envs else "列表")
                        wrap = None
                else:
                    if name in envs:
                        while envs and envs.pop() != name:
                            pass
                    if name == "abstract":
                        kind = "front"
                        self.check_abstract(abstract_sentences)
                    if name in ("wrapfigure", "wraptable") and wrap_float is not None:
                        if wrap_float["neg"]:
                            self.wrap_neg.append(wrap_float["loc"])
                        wrap = {"loc": wrap_float["loc"], "env": name, "chars": 0, "limit": wrap_float["limit"]}
                        wrap_float = None
                    if name in TABULAR_ENVS and table:
                        self.tables.append(table)
                        float_tables.append(table)
                        table = None
                    if name in FLOAT_ENVS:
                        for item in float_tables:
                            item["float_label"] = item["float_label"] or float_label
                        float_tables = []

            if "contribution" in text.lower() and kind == "intro":
                list_ok_until = index + 6

            if any(e in SKIP_ENVS for e in envs):
                continue

            in_float = any(e in FLOAT_ENVS for e in envs)
            in_display = any(e in self.math_envs for e in envs) or "\\[" in text or "$$" in text
            in_tab = any(e in TABULAR_ENVS for e in envs)
            owner = OWNER_BY_KIND.get(kind, "paper-language")

            if table is not None:
                table["lines"].append(text)
            if in_float:
                label = re.search(r"\\label\{([^}]+)\}", text)
                if label and float_label is None:
                    float_label = label.group(1)

            if wrap is not None:
                if HEADING_RE.search(text):
                    self.wrap_hit(wrap, loc, text, "标题")
                    wrap = None
                elif ("\\[" in text or "$$" in text) and not in_float:
                    self.wrap_hit(wrap, loc, text, "行间公式")
                    wrap = None
                elif not in_float:
                    wrap["chars"] += len(text.strip())
                    if wrap["chars"] > wrap["limit"]:
                        wrap = None

            for _ in re.finditer(r"\\hline\b", text):
                self.hit("hline", "local", "paper-visuals", loc, text, "使用 \\hline，应改为 booktabs 规则")
            if "\\vspace" in text and not in_float and not text.lstrip().startswith("\\newcommand"):
                self.hit("vspace-outside-float", "local", "paper-typesetting", loc, text,
                         "\\vspace 位于浮动体之外")

            for match in CITE_RE.finditer(text):
                keys = [k for k in match.group(1).split(",") if k.strip()]
                self.cited.update(k.strip() for k in keys)
                if len(keys) > 4:
                    self.hit("cite-count", "local", "paper-opening", loc, match.group(0),
                             f"一个引用命令含 {len(keys)} 个 key，超过 4 个")

            for pattern in SECRET_PATTERNS:
                for match in re.finditer(pattern, text):
                    self.hit("anon-secret", "submit", "paper-typesetting", loc, match.group(0)[:12] + "...",
                             "疑似密钥或令牌")
            for match in re.finditer(r"[\w.+-]+@[A-Za-z][\w-]*(?:\.[\w-]+)*\.[A-Za-z]{2,}\b", text):
                self.hit("anon-email", "submit", "paper-typesetting", loc, match.group(0), "正文含邮箱地址")
            for match in re.finditer(r"(?:https?://)?(?:www\.)?(?:github\.com|huggingface\.co|gitlab\.com)/[\w.\-]+", text):
                self.hit("anon-url", "submit", "paper-typesetting", loc, match.group(0), "代码托管链接含用户名，匿名投稿需确认")
            if re.search(r"\bour (?:previous|prior|earlier) (?:work|paper|study)\b", text, re.I):
                self.hit("anon-self", "submit", "paper-typesetting", loc, text, "第一人称引用自己的已有工作")

            for pattern in PENDING_PATTERNS:
                for match in re.finditer(pattern, text):
                    self.hit("pending-marker", "submit", owner, loc, text, f"待定标记 {match.group(0)}")
            if re.search(r"\\(?:pending|tbd|placeholder)\b", text):
                self.hit("pending-marker", "submit", owner, loc, text, "待定宏")

            if in_display or in_tab:
                if kind == "method" and in_display and not in_float:
                    self.method_digits(loc, text, math_only=True)
                continue

            prose, maths = prose_part(text)

            if "\u2014" in prose or "\u2014\u2014" in prose or re.search(r"(?<!-)---(?!-)", prose):
                self.hit("em-dash", "local", "paper-language", loc, text, "正文含 em dash")
            if re.search(r"\$\s*[<>]\s*\$", text):
                self.hit("gt-lt-in-prose", "local", "paper-language", loc, text,
                         "正文用 $>$/$<$，应写 greater than / less than")
            for opener in BANNED_OPENERS:
                if re.search(r"(?:^|[.!?]\s+|\}\s*)" + re.escape(opener) + r"\b", prose.strip()):
                    self.hit("banned-opener", "local", "paper-language", loc, text, f"禁用句首 “{opener}”")
            for word in BANNED_WORDS:
                for match in re.finditer(r"\b" + word + r"\b", prose, re.I):
                    self.hit("banned-word", "local", "paper-language", loc, text, f"禁用词 “{match.group(0)}”")
            if re.search(r"\bnot\s+(?!only\b)[^.;:]{1,60}?,?\s+but\s+(?!also\b)", prose):
                self.hit("not-x-but-y", "local", "paper-language", loc, text, "“not X but Y” 句式，确认对比本身是否为论点")
            if re.search(r"\bsignificant(?:ly)?\b", prose, re.I):
                self.hit("significant", "local", "paper-language", loc, text, "“significant” 需对应已做的统计检验")
            for pattern in PROCESS_PATTERNS:
                for match in re.finditer(pattern, prose, re.I):
                    self.hit("process-text", "clarity", owner, loc, text, f"疑似过程或状态说明 “{match.group(0)}”")

            for sentence in re.split(r"(?<=[.!?])\s+", prose.strip()):
                first = re.match(r"(?:\\[a-zA-Z]+\{[^}]*\}\s*)*([A-Z][a-z]+)", sentence)
                word = first.group(1) if first else None
                if word in ("Furthermore", "Moreover") and last_opener in ("Furthermore", "Moreover"):
                    self.hit("consecutive-connective", "local", "paper-language", loc, text,
                             "Furthermore / Moreover 连续出现")
                last_opener = word
                if kind == "abstract" and sentence.strip():
                    abstract_sentences.append((loc, sentence))

            in_list = any(e in LIST_ENVS for e in envs)
            if kind in ("intro", "abstract") and not in_list:
                for match in REF_RE.finditer(text):
                    label = match.group(2)
                    context = text[max(0, match.start() - 16): match.start()]
                    if re.match(r"(sec|thm|prop|lem|eq|app|def|cor|alg)", label) or \
                            re.search(r"(Section|Sec\.|Theorem|Proposition|Lemma|Eq\.|Equation|Appendix)~?\s*$", context):
                        self.hit("intro-ref", "local", "paper-opening", loc, match.group(0),
                                 "摘要或引言引用了章节、定理或公式")
                symbolic = [m for m in maths if re.search(r"[A-Za-z\\]", m)]
                if symbolic:
                    self.hit("intro-math", "local", "paper-opening", loc, " ".join(symbolic),
                             "摘要或引言出现数学符号")
            if kind == "method":
                self.method_digits(loc, text, math_only=False)

    def wrap_hit(self, wrap, loc, text, what):
        if wrap["chars"] <= wrap["limit"]:
            self.hit("wrap-float", "clarity", "paper-typesetting", loc, text,
                     f"{wrap['env']}（{wrap['loc']}）之后约 {wrap['chars']} 字符处出现{what}，"
                     "绕排不缩窄它，需在渲染页确认是否重叠")

    def method_digits(self, loc, text, math_only):
        cleaned = strip_nonnumeric_args(text)
        if math_only:
            segments = [("math", cleaned)]
        else:
            prose, maths = prose_part(cleaned)
            segments = [("prose", prose)] + [("math", m) for m in maths]
        found = []
        for where, segment in segments:
            for match in re.finditer(r"(?<![A-Za-z\\])\d+(?:\.\d+)?", segment):
                value = match.group(0)
                if where == "math":
                    if value in ("0", "1", "2"):
                        continue
                    after = segment[match.end():]
                    coefficient = re.match(r"(?:\\[,;:! ]|\s)*(?:[A-Za-z(]|\\[A-Za-z])", after)
                    if coefficient and not re.match(r"\s*\\(?:times|cdot)\s*\d", after):
                        continue  # a coefficient written before a symbol, such as 4\,\tilde p
                found.append(value)
        if found:
            self.hit("method-digit", "clarity", "paper-method", loc, text,
                     f"方法部分出现数字 {', '.join(sorted(set(found)))}")

    def check_abstract(self, sentences):
        with_numbers = [(loc, s) for loc, s in sentences if re.search(r"\d", strip_nonnumeric_args(s))]
        if len(with_numbers) > 1:
            loc, sentence = with_numbers[1]
            self.hit("abstract-numbers", "local", "paper-opening", loc, sentence,
                     f"摘要中有 {len(with_numbers)} 句含数字，默认只保留一句主结果")

    def check_tables(self):
        shapes = []
        for table in self.tables:
            body = "\n".join(table["lines"])
            top = body.find("\\toprule")
            mid = body.find("\\midrule")
            if top < 0 or mid < 0:
                continue
            header = body[top + len("\\toprule"): mid]
            depth, rows, i = 0, 0, 0
            while i < len(header):
                ch = header[i]
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                elif header.startswith("\\\\", i) and depth == 0:
                    rows += 1
                    i += 1
                i += 1
            stacks = re.findall(r"\\(?:shortstack|makecell|thead)(?:\[[^\]]*\])?\{([^{}]*)\}", header)
            stacked = len(stacks)
            extra = max((s.count("\\\\") for s in stacks), default=0)
            rules = len(re.findall(r"\\cmidrule", header))
            name = table["float_label"] or table["loc"]
            if stacked and "\\multirow" in header:
                self.hit("table-multirow", "local", "paper-visuals", (table["loc"], ""), name,
                         f"表头显示 {rows + extra} 行，含 {stacked} 个堆叠单元，\\multirow 按逻辑行数定位，跨行的列名会偏高")
            if not table["appendix"]:
                shapes.append((name, table["loc"], rows, rows + extra, rules))
        groups = {}
        for name, _, _, shown, _ in shapes:
            groups.setdefault(shown, []).append(name)
        if len(groups) > 1:
            summary = "；".join(f"显示 {shown} 行：{', '.join(names)}" for shown, names in sorted(groups.items()))
            self.hit("table-header-mismatch", "local", "paper-visuals", (shapes[0][1], ""),
                     f"{len(shapes)} 个表，表头显示行数有 {len(groups)} 种",
                     f"{summary}。只比较正文中的表；承担相同角色的表若分在不同组，需统一")

    def check_bib(self):
        for name in self.bib_files:
            path = resolve(self.base_dir, name if name.endswith(".bib") else name + ".bib")
            try:
                with open(path, encoding="utf-8", errors="replace") as handle:
                    content = handle.read()
            except OSError:
                print(f"warning: cannot read bib file {path}", file=sys.stderr)
                continue
            rel = os.path.relpath(path, self.base_dir)
            entries = list(re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", content))
            for i, entry in enumerate(entries):
                key = entry.group(2)
                if entry.group(1).lower() in ("string", "preamble", "comment"):
                    continue
                if key not in self.cited and not self.args.all_bib:
                    continue
                stop = entries[i + 1].start() if i + 1 < len(entries) else len(content)
                for field in re.finditer(r"(?:^|[,{\s])(\w+)\s*=\s*", content[entry.end():stop]):
                    offset = entry.end() + field.start(1)
                    number = content.count("\n", 0, offset) + 1
                    line = content[offset: content.find("\n", offset) if "\n" in content[offset:] else stop]
                    name_l = field.group(1).lower()
                    if name_l in ("note", "annote", "urldate", "timestamp", "biburl", "bibsource", "addendum"):
                        self.hit("bib-field", "local", "paper-typesetting", (rel, number), line,
                                 f"{key}: 字段 {name_l}，确认是否为非正式备注或时间戳")
                    if name_l == "year":
                        year = re.match(r"\{?\"?(\d{4})", content[entry.end() + field.end():stop])
                        if year and int(year.group(1)) < 2000:
                            self.hit("bib-old", "info", "paper-opening", (rel, number), line,
                                     f"{key}: {year.group(1)} 年，确认是否为领域经典")
                    if name_l == "author":
                        value = content[entry.end() + field.end():stop].split("\n", 1)[0]
                        if re.search(r"\band others\b", value):
                            self.hit("bib-others", "local", "paper-typesetting", (rel, number), line,
                                     f"{key}: 作者列表用 and others 截断")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("main", help="root .tex file of the manuscript")
    parser.add_argument("--format", choices=("tsv", "json"), default="tsv")
    parser.add_argument("--only", help="comma-separated check names to keep")
    parser.add_argument("--method-titles", help="comma-separated section titles to treat as the method")
    parser.add_argument("--wrap-chars", type=int, default=1500,
                        help="source characters after a wrapped float within which display math, a list or "
                             "a heading is reported (default 1500; 70 per line when the float gives a line count)")
    parser.add_argument("--all-bib", action="store_true", help="check every bib entry, not only cited ones")
    args = parser.parse_args()

    if not os.path.isfile(args.main):
        print(f"error: {args.main} is not a file", file=sys.stderr)
        return 2
    base_dir = os.path.dirname(os.path.abspath(args.main))
    lines = []
    load(os.path.abspath(args.main), base_dir, set(), lines)
    scanner = Scanner(args, lines, base_dir)
    scanner.run()

    if args.format == "json":
        json.dump(scanner.hits, sys.stdout, ensure_ascii=False, indent=1)
        sys.stdout.write("\n")
    else:
        for h in scanner.hits:
            print("\t".join([h["check"], h["tier"], h["owner"], h["location"], h["excerpt"], h["message"]]))

    print(f"scanned {len(lines)} lines from {len({l[0] for l in lines})} files", file=sys.stderr)
    for loc, title, kind in scanner.sections:
        print(f"section {kind:<11} {title} ({loc})", file=sys.stderr)
    counts = {}
    for h in scanner.hits:
        counts[h["check"]] = counts.get(h["check"], 0) + 1
    for check, count in sorted(counts.items()):
        print(f"hits {check}: {count}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
