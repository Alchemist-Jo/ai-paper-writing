#!/usr/bin/env python3
"""Deterministic checks for paper figures. Python standard library plus Poppler tools.

  figure_audit.py drawio FIG.drawio [--insert-width-pt W] [--caption-pt 9]
      Inventory of one draw.io file: labels, fonts, sizes, colors, strokes, decoration,
      raster images and code-like labels. With --insert-width-pt, sizes are converted to
      printed points at the inserted width and compared with the caption size.

  figure_audit.py diff OLD.drawio NEW.drawio
      Content equality for a style-only edit: cell ids, labels, element kinds, the cells each
      arrow connects (inferred from its end points when the arrow is not attached), and
      visibility. Line-break changes are listed but do not count as content changes.

  figure_audit.py pdf FIG.pdf [--insert-width-pt W] [--caption-pt 9]
      Exported figure: font embedding and Type 3 fonts, raster images and their resolution
      at the inserted size, and approximate printed text sizes from glyph boxes.

  figure_audit.py style A.drawio B.drawio ...
      Style across figures, per role (frame, card, text, arrow, line): font sizes, stroke
      widths, corner sizes and fills with counts, plus font families and one-file accents.

Every result is a candidate. Confirm it on the rendered page before acting on it.
"""
import argparse
import base64
import collections
import html
import re
import statistics
import subprocess
import sys
import urllib.parse
import xml.etree.ElementTree as ET
import zlib

LOW_RATIO = 0.70          # text below this fraction of the caption size is reported
GLYPH_BOX = 1.15          # glyph-box height divided by font size, typical for text fonts
CODE_LIKE = re.compile(
    r"\b[a-z][a-z0-9]*_[a-z0-9_]+\b"          # snake_case identifiers
    r"|\b[a-z]+[A-Z]\w*\("                    # camelCase calls
    r"|\w\([^)]*=[^)]*\)"                     # calls with keyword arguments
    r"|(^|\s)#\s|//"                          # code comments
    r"|\.(py|json|yaml|yml|csv|txt|pt|ckpt)\b"  # file names
    r"|\b(True|False|None|null)\b"
    r"|\b[tfn]/[tfn]\b"                       # flag abbreviations such as t/f
)
DECOR = {"shadow": "shadow", "glass": "glass effect", "sketch": "sketch style", "comic": "comic style"}
NEUTRAL = {"none", "default", "#ffffff", "#fff", "inherit", ""}
SNAP = 10.0               # canvas units within which a free arrow end counts as touching a cell


# ------------------------------------------------------------------ draw.io parsing

def load_pages(path):
    root = ET.parse(path).getroot()
    pages = []
    diagrams = root.findall("diagram") if root.tag == "mxfile" else []
    if root.tag == "mxGraphModel":
        pages.append(("page-1", root))
    for i, d in enumerate(diagrams):
        model = d.find("mxGraphModel")
        if model is None and (d.text or "").strip():
            raw = base64.b64decode(d.text.strip())
            xml = urllib.parse.unquote(zlib.decompress(raw, -15).decode("utf-8"))
            model = ET.fromstring(xml)
        if model is not None:
            pages.append((d.get("name") or f"page-{i + 1}", model))
    return pages


def parse_style(s):
    out = {}
    for part in (s or "").split(";"):
        if not part:
            continue
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = v.strip()
        else:
            out.setdefault("_base", part.strip())
    return out


def label_lines(v):
    v = re.sub(r"<br\s*/?>|</div>|</p>", "\n", v or "", flags=re.I)
    v = re.sub(r"<[^>]+>", "", v)
    v = html.unescape(v).replace("\xa0", " ")
    lines = (re.sub(r"[ \t\r\f\v]+", " ", line).strip() for line in v.split("\n"))
    return "\n".join(line for line in lines if line)


def strip_label(v):
    return label_lines(v).replace("\n", " ")


def num(v):
    """Normalize a numeric style value, so 1, 1.0 and 0.99999 compare equal."""
    try:
        return f"{float(v):.2f}".rstrip("0").rstrip(".")
    except (TypeError, ValueError):
        return str(v)


def cells_of(model):
    """Yield (id, element, style dict, label, geometry) for each mxCell, including UserObject wrappers."""
    root = model.find("root")
    if root is None:
        return
    for el in root:
        cell, value = el, el.get("value")
        if el.tag in ("UserObject", "object"):
            inner = el.find("mxCell")
            if inner is None:
                continue
            cell, value = inner, el.get("label", value)
        if cell.tag != "mxCell":
            continue
        cid = el.get("id") or cell.get("id")
        yield cid, cell, parse_style(cell.get("style")), value or "", cell.find("mxGeometry")


def page_cells(model):
    cells = {}
    for cid, cell, st, value, geo in cells_of(model):
        cells[cid] = dict(cell=cell, style=st, raw=value, label=strip_label(value), lines=label_lines(value),
                          geo=geo, parent=cell.get("parent"), vertex=cell.get("vertex") == "1",
                          edge=cell.get("edge") == "1")
    return cells


def absolute_box(cid, cells, cache):
    if cid in cache:
        return cache[cid]
    c = cells.get(cid)
    if c is None or c["geo"] is None or not c["vertex"]:
        cache[cid] = None
        return None
    g = c["geo"]
    x, y = float(g.get("x", 0)), float(g.get("y", 0))
    w, h = float(g.get("width", 0)), float(g.get("height", 0))
    if g.get("relative") == "1":
        cache[cid] = None
        return None
    parent = cells.get(c["parent"])
    if parent is not None and parent["vertex"]:
        pb = absolute_box(c["parent"], cells, cache)
        if pb:
            x, y = x + pb[0], y + pb[1]
    cache[cid] = (x, y, w, h)
    return cache[cid]


def content_width(cells):
    cache, xs = {}, []
    for cid in cells:
        b = absolute_box(cid, cells, cache)
        if b and b[2] > 0:
            xs.append((b[0], b[0] + b[2]))
    if not xs:
        return 0.0
    return max(r for _, r in xs) - min(l for l, _ in xs)


def font_runs(c):
    """(family, size) pairs used by one cell's label: the cell style plus inline HTML spans."""
    st, raw = c["style"], c["raw"]
    fam = st.get("fontFamily", "Helvetica (default)")
    size = st.get("fontSize")
    size = float(size) if size else None
    runs = [(fam, size)]
    for m in re.finditer(r"font-family:\s*['\"]?([^;'\"]+)", html.unescape(raw)):
        runs.append((m.group(1).split(",")[0].strip(), None))
    for m in re.finditer(r"font-size:\s*([\d.]+)\s*(px|pt)?", raw):
        runs.append((None, float(m.group(1))))
    for m in re.finditer(r"<font[^>]*face=\"([^\"]+)\"", raw):
        runs.append((m.group(1), None))
    return runs


def colors_of(st):
    out = []
    for k in ("fillColor", "strokeColor", "fontColor", "gradientColor", "labelBackgroundColor"):
        v = st.get(k, "").lower()
        if v and v not in NEUTRAL:
            out.append((k, v))
    return out


def draws_stroke(c):
    st = c["style"]
    if st.get("strokeColor", "").lower() == "none" or st.get("_base") == "text" or st.get("shape") == "image":
        return False
    return c["edge"] or c["vertex"]


def has_arrow(c):
    st = c["style"]
    return c["edge"] and (st.get("endArrow", "classic") != "none" or st.get("startArrow", "none") != "none")


def role(c, parents):
    st = c["style"]
    if c["edge"]:
        return "arrow" if has_arrow(c) else "line"
    if not c["vertex"]:
        return None
    if st.get("dashed") == "1" or c["cell"].get("id") in parents:
        return "frame"
    filled = st.get("fillColor", "").lower() not in ("", "none")
    if draws_stroke(c) or filled:
        return "card"
    return "text" if c["label"] else None


def seen_fill(st):
    """A cell's fill as seen over white, after fillOpacity and opacity; None when unfilled."""
    fill = st.get("fillColor", "").lower()
    m = re.fullmatch(r"#([0-9a-f]{6}|[0-9a-f]{3})", fill)
    if not m:
        return None
    h = m.group(1) if len(m.group(1)) == 6 else "".join(ch * 2 for ch in m.group(1))
    alpha = float(st.get("fillOpacity", 100)) / 100 * float(st.get("opacity", 100)) / 100
    rgb = (round(int(h[i:i + 2], 16) * alpha + 255 * (1 - alpha)) for i in (0, 2, 4))
    return "#" + "".join(f"{v:02x}" for v in rgb)


def background(cid, cells, cache):
    """Seen fill of the smallest filled shape under the center of a cell, or white."""
    b = absolute_box(cid, cells, cache)
    if not b:
        return "#ffffff"
    x, y, best = b[0] + b[2] / 2, b[1] + b[3] / 2, None
    for other, o in cells.items():
        fill = seen_fill(o["style"]) if other != cid else None
        ob = absolute_box(other, cells, cache) if fill else None
        if ob and ob[0] <= x <= ob[0] + ob[2] and ob[1] <= y <= ob[1] + ob[3]:
            if best is None or ob[2] * ob[3] < best[0]:
                best = (ob[2] * ob[3], fill)
    return best[1] if best else "#ffffff"


def hidden(cid, cells, cache):
    c, st = cells[cid], cells[cid]["style"]
    if c["cell"].get("visible") == "0" or st.get("opacity") == "0":
        return True
    if c["edge"] and st.get("strokeColor", "").lower() == "none":
        return True
    if c["label"]:
        font = st.get("fontColor", "").lower()
        fill = seen_fill(st) or background(cid, cells, cache)
        if st.get("textOpacity") == "0" or st.get("noLabel") == "1" or font == "none":
            return True
        if font and contrast(font, fill) < 1.5:
            return True
    return False


def contrast(a, b):
    """WCAG contrast ratio of two hex colors; 1 means identical, 21 is black on white."""
    def lum(h):
        m = re.fullmatch(r"#([0-9a-f]{6}|[0-9a-f]{3})", h)
        if not m:
            return None
        h = m.group(1) if len(m.group(1)) == 6 else "".join(ch * 2 for ch in m.group(1))
        rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        rgb = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in rgb]
        return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
    la, lb = lum(a), lum(b)
    if la is None or lb is None:
        return 21.0
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def endpoints(cid, cells, cache):
    """Cells an arrow connects: its source and target, or else the smallest drawn shape near each
    free end, falling back to a text-only cell when no shape is near."""
    c = cells[cid]
    ends = []
    for attr, point in (("source", "sourcePoint"), ("target", "targetPoint")):
        if c["cell"].get(attr):
            ends.append(c["cell"].get(attr))
            continue
        p = c["geo"].find(f"mxPoint[@as='{point}']") if c["geo"] is not None else None
        if p is None:
            ends.append("?")
            continue
        x, y = float(p.get("x", 0)), float(p.get("y", 0))
        pb = absolute_box(c["parent"], cells, cache)
        if pb:
            x, y = x + pb[0], y + pb[1]
        best = {}  # smallest box near the end, separately for drawn shapes and for text-only cells
        for other, o in cells.items():
            b = absolute_box(other, cells, cache)
            if not b or b[2] <= 0 or b[3] <= 0:
                continue
            if b[0] - SNAP <= x <= b[0] + b[2] + SNAP and b[1] - SNAP <= y <= b[1] + b[3] + SNAP:
                group = "shape" if draws_stroke(o) or o["style"].get("fillColor", "").lower() not in ("", "none") \
                    or o["style"].get("shape") == "image" else "text"
                if group not in best or b[2] * b[3] < best[group][0]:
                    best[group] = (b[2] * b[3], other)
        pick = best.get("shape") or best.get("text")
        ends.append(pick[1] if pick else "?")
    return tuple(ends)


def is_accent(hexcolor):
    """True for saturated mid-lightness colors; pale tints and greys are excluded."""
    m = re.fullmatch(r"#([0-9a-f]{6})", hexcolor)
    if not m:
        return False
    r, g, b = (int(m.group(1)[i:i + 2], 16) / 255 for i in (0, 2, 4))
    hi, lo = max(r, g, b), min(r, g, b)
    light = (hi + lo) / 2
    if hi == lo or light > 0.85:
        return False
    sat = (hi - lo) / (1 - abs(2 * light - 1))
    return sat > 0.25


# ------------------------------------------------------------------ commands

def cmd_drawio(a):
    for name, model in load_pages(a.file):
        cells = page_cells(model)
        labelled = {k: c for k, c in cells.items() if c["label"]}
        width = content_width(cells)
        scale = a.insert_width_pt / width if a.insert_width_pt and width else None
        print(f"== {a.file} [{name}]")
        print(f"cells {len(cells)}, vertices {sum(c['vertex'] for c in cells.values())}, "
              f"edges {sum(c['edge'] for c in cells.values())}, labels {len(labelled)}, "
              f"content width {width:.0f} units"
              + (f", printed scale {scale:.4f} pt/unit" if scale else ""))

        fams, sizes, unset, small = collections.Counter(), collections.Counter(), [], []
        for cid, c in labelled.items():
            runs = font_runs(c)
            for fam, _ in runs:
                if fam:
                    fams[fam] += 1
            label_sizes = [s for _, s in runs if s] or []
            if not label_sizes:
                unset.append(cid)
            for s in label_sizes:
                sizes[s] += 1
            if scale and label_sizes:
                pt = min(label_sizes) * scale
                if pt < LOW_RATIO * a.caption_pt:
                    small.append((pt, cid, c["label"]))
        print("fonts: " + ", ".join(f"{f} x{n}" for f, n in fams.most_common()))
        line = []
        for s, n in sorted(sizes.items()):
            t = f"{s:g}"
            if scale:
                t += f" ({s * scale:.1f} pt, {100 * s * scale / a.caption_pt:.0f}% of caption)"
            line.append(f"{t} x{n}")
        print("sizes: " + "; ".join(line))
        if unset:
            print(f"size unset (draw.io default applies): {len(unset)} labels, e.g. {', '.join(unset[:5])}")
        if small:
            print(f"small text: {len(small)} of {len(labelled)} labels below {LOW_RATIO:.0%} of the caption "
                  f"({LOW_RATIO * a.caption_pt:.1f} pt); smallest:")
            for pt, cid, lab in sorted(small)[:6]:
                print(f"  {pt:.1f} pt  {cid}  \"{lab[:60]}\"")

        code = [(cid, c["label"]) for cid, c in labelled.items() if CODE_LIKE.search(c["label"])]
        for cid, lab in code:
            print(f"code-like label: {cid}  \"{lab[:80]}\"")

        decor = collections.Counter()
        raster, svg = [], 0
        for cid, c in cells.items():
            st = c["style"]
            for k, desc in DECOR.items():
                if st.get(k) == "1":
                    decor[desc] += 1
            if st.get("gradientColor", "none").lower() not in NEUTRAL:
                decor["gradient fill"] += 1
            img = st.get("image", "")
            if img.startswith("data:image/svg") or img.lower().endswith(".svg"):
                svg += 1
            elif img:
                raster.append(cid)
        for d, n in decor.items():
            print(f"decoration: {d} on {n} cells")
        if raster:
            print(f"raster images: {len(raster)} ({', '.join(raster[:8])})")
        if svg:
            print(f"svg images: {svg}")

        pal = collections.Counter(v for c in cells.values() for _, v in colors_of(c["style"]))
        print(f"colors ({len(pal)}): " + ", ".join(f"{v} x{n}" for v, n in pal.most_common()))
        sw = collections.Counter(num(c["style"].get("strokeWidth", "1")) for c in cells.values()
                                 if draws_stroke(c))
        arcs = collections.Counter(c["style"].get("arcSize", "-") for c in cells.values()
                                   if c["style"].get("rounded") == "1" and c["vertex"])
        dashed = sum(1 for c in cells.values() if c["edge"] and c["style"].get("dashed") == "1")
        print("stroke widths (drawn strokes): " + ", ".join(f"{k} x{n}" for k, n in sorted(sw.items(), key=lambda kv: float(kv[0]))))
        if arcs:
            print("corner arcSize: " + ", ".join(f"{k} x{n}" for k, n in sorted(arcs.items())))
        print(f"dashed edges: {dashed}")


def kind(c):
    st = c["style"]
    return ("edge" if c["edge"] else "vertex" if c["vertex"] else "other",
            st.get("shape", st.get("_base", "")), st.get("dashed", "0"),
            st.get("startArrow", ""), st.get("endArrow", ""))


def page_maps(path):
    """Per page: cells, the cells each arrow connects, and hidden cells, keyed by (page, id)."""
    cells, ends, hide = {}, {}, set()
    for i, (_, model) in enumerate(load_pages(path)):
        page, cache = page_cells(model), {}
        for k, c in page.items():
            cells[(i, k)] = c
            if has_arrow(c):
                ends[(i, k)] = endpoints(k, page, cache)
            if hidden(k, page, cache):
                hide.add((i, k))
    return cells, ends, hide


def cmd_diff(a):
    old, old_ends, old_hidden = page_maps(a.old)
    new, new_ends, new_hidden = page_maps(a.new)
    removed = sorted(set(old) - set(new))
    added = sorted(set(new) - set(old))
    common = set(old) & set(new)
    changed_label = [k for k in common if old[k]["label"] != new[k]["label"]]
    changed_kind = [k for k in common if kind(old[k]) != kind(new[k])]
    changed_ends = sorted(k for k in common if old_ends.get(k) != new_ends.get(k))
    now_hidden = sorted(k for k in common if k in new_hidden and k not in old_hidden)
    now_shown = sorted(k for k in common if k in old_hidden and k not in new_hidden)
    rewrapped = sorted(k for k in common if old[k]["label"] == new[k]["label"] and old[k]["lines"] != new[k]["lines"])
    ol = collections.Counter(c["label"] for c in old.values() if c["label"])
    nl = collections.Counter(c["label"] for c in new.values() if c["label"])
    print(f"cells: old {len(old)}, new {len(new)}; removed {len(removed)}, added {len(added)}")
    for k in removed:
        print(f"removed: page {k[0] + 1} {k[1]}  \"{old[k]['label'][:60]}\"")
    for k in added:
        print(f"added: page {k[0] + 1} {k[1]}  \"{new[k]['label'][:60]}\"")
    for k in sorted(changed_label):
        print(f"label changed: {k[1]}  \"{old[k]['label'][:50]}\" -> \"{new[k]['label'][:50]}\"")
    for k in sorted(changed_kind):
        print(f"kind changed: {k[1]}  {kind(old[k])} -> {kind(new[k])}")
    for k in changed_ends:
        o, n = old_ends.get(k, ("-", "-")), new_ends.get(k, ("-", "-"))
        print(f"arrow ends changed: {k[1]}  {o[0]} -> {o[1]}  became  {n[0]} -> {n[1]}")
    for k in now_hidden:
        print(f"now hidden: {k[1]}  \"{new[k]['label'][:50]}\"")
    for k in now_shown:
        print(f"now visible: {k[1]}  \"{new[k]['label'][:50]}\"")
    for k in rewrapped:
        print(f"line breaks changed (presentation): {k[1]}  {old[k]['lines']!r} -> {new[k]['lines']!r}")
    unresolved = sum(1 for e in new_ends.values() if "?" in e)
    print(f"arrows: {len(new_ends)} compared by the cells they connect"
          + (f", {unresolved} with an end touching no cell (check on the render)" if unresolved else ""))
    only_old, only_new = ol - nl, nl - ol
    for lab, n in only_old.items():
        print(f"label only in old (x{n}): \"{lab[:70]}\"")
    for lab, n in only_new.items():
        print(f"label only in new (x{n}): \"{lab[:70]}\"")
    equal = not (removed or added or changed_label or changed_kind or changed_ends or now_hidden
                 or now_shown or only_old or only_new)
    print("content equal: " + ("yes" if equal else "no"))


def run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, check=False).stdout
    except FileNotFoundError:
        sys.exit(f"missing tool: {cmd[0]} (install Poppler)")


def cmd_pdf(a):
    info = run(["pdfinfo", a.file])
    m = re.search(r"Page size:\s+([\d.]+) x ([\d.]+)", info)
    if not m:
        sys.exit(f"cannot read {a.file}")
    w = float(m.group(1))
    scale = a.insert_width_pt / w if a.insert_width_pt else 1.0
    print(f"== {a.file}: {w:.0f} x {float(m.group(2)):.0f} pt"
          + (f", inserted at {a.insert_width_pt:.0f} pt, scale {scale:.3f}" if a.insert_width_pt else ""))

    lines = run(["pdffonts", a.file]).splitlines()[2:]
    seen = set()
    for ln in lines:
        parts = ln.split()
        if len(parts) < 5:
            continue
        name = re.sub(r"^[A-Z]{6}\+", "", parts[0])
        emb_idx = next((i for i, p in enumerate(parts) if p in ("yes", "no")), None)
        ftype = " ".join(parts[1:emb_idx - 1]) if emb_idx else "?"
        emb = parts[emb_idx] if emb_idx else "?"
        if (name, ftype) in seen:
            continue
        seen.add((name, ftype))
        flags = []
        if emb == "no":
            flags.append("NOT EMBEDDED")
        if "Type 3" in ftype:
            flags.append("Type 3")
        print(f"font: {name}  {ftype}" + (f"  [{', '.join(flags)}]" if flags else ""))

    imgs = run(["pdfimages", "-list", a.file]).splitlines()[2:]
    ppis = []
    for ln in imgs:
        parts = ln.split()
        if len(parts) >= 13 and parts[2] == "image":
            try:
                ppis.append(float(parts[12]) / scale)
            except ValueError:
                pass
    if ppis:
        print(f"raster images: {len(ppis)}, lowest resolution at inserted size {min(ppis):.0f} ppi")

    words = re.findall(r'yMin="([\d.]+)" xMax="[\d.]+" yMax="([\d.]+)">([^<]*)</word>',
                       run(["pdftotext", "-bbox", a.file, "-"]))
    sizes = [((float(y1) - float(y0)) / GLYPH_BOX * scale, html.unescape(t)) for y0, y1, t in words]
    if not sizes:
        print("text: none found (outlined text or raster only)")
        return
    vals = sorted(s for s, _ in sizes)
    p10 = vals[max(0, len(vals) // 10 - 1)]
    print(f"text: {len(vals)} words, approximate printed size min {vals[0]:.1f} pt, "
          f"10th percentile {p10:.1f} pt, median {statistics.median(vals):.1f} pt "
          f"(caption {a.caption_pt:g} pt)")
    small = sorted({(round(s, 1), t) for s, t in sizes if s < LOW_RATIO * a.caption_pt})
    if small:
        print(f"small text: {len(small)} distinct words below {LOW_RATIO:.0%} of the caption "
              f"({LOW_RATIO * a.caption_pt:.1f} pt); smallest: "
              + ", ".join(f"\"{t}\" ~{s:.1f} pt" for s, t in small[:6]))
    code = sorted({t for _, t in sizes if CODE_LIKE.search(t)})
    for t in code[:20]:
        print(f"code-like word: \"{t}\"")


def cmd_style(a):
    rows, pal_files = [], collections.defaultdict(set)
    fmt = lambda counter: ", ".join(f"{k} x{n}" for k, n in counter.most_common(5)) or "-"
    for f in a.files:
        fams, pal = collections.Counter(), set()
        stats = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
        for _, model in load_pages(f):
            cells = page_cells(model)
            parents = {c["parent"] for c in cells.values() if c["vertex"]}
            for c in cells.values():
                st, r = c["style"], role(c, parents)
                if c["label"]:
                    for fam, size in font_runs(c):
                        if fam:
                            fams[fam] += 1
                        if size and r:
                            stats[r]["size"][num(size)] += 1
                if not r:
                    continue
                stats[r]["n"][""] += 1
                if draws_stroke(c):
                    stats[r]["stroke"][num(st.get("strokeWidth", "1"))] += 1
                if st.get("rounded") == "1" and c["vertex"]:
                    stats[r]["arc"][st.get("arcSize", "-")] += 1
                fill = st.get("fillColor", "").lower()
                if c["vertex"] and fill not in ("", "none"):
                    alpha = float(st.get("fillOpacity", 100)) * float(st.get("opacity", 100)) / 100
                    stats[r]["fill"][fill + (f"@{num(alpha)}%" if alpha < 100 else "")] += 1
                for _, v in colors_of(st):
                    pal.add(v)
                    pal_files[v].add(f)
        rows.append((f, fams, stats, pal))
    for f, fams, stats, pal in rows:
        print(f"== {f}")
        print("  fonts: " + fmt(fams))
        for r in ("frame", "card", "text", "arrow", "line"):
            if r in stats:
                d = stats[r]
                print(f"  {r} x{d['n']['']}: sizes {fmt(d['size'])}; strokes {fmt(d['stroke'])}; "
                      f"corners {fmt(d['arc'])}; fills {fmt(d['fill'])}")
        print(f"  colors: {len(pal)}")
    all_fams = set().union(*(set(r[1]) for r in rows))
    if len(all_fams) > 1:
        print("font families across files: " + ", ".join(sorted(all_fams)))
    single = sorted(v for v, fs in pal_files.items()
                    if len(fs) == 1 and len(a.files) > 1 and is_accent(v))
    if single:
        print("accent colors used in only one file: " + ", ".join(
            f"{v} ({next(iter(pal_files[v])).rsplit('/', 1)[-1]})" for v in single))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("drawio")
    d.add_argument("file")
    d.add_argument("--insert-width-pt", type=float)
    d.add_argument("--caption-pt", type=float, default=9.0)
    df = sub.add_parser("diff")
    df.add_argument("old")
    df.add_argument("new")
    pp = sub.add_parser("pdf")
    pp.add_argument("file")
    pp.add_argument("--insert-width-pt", type=float)
    pp.add_argument("--caption-pt", type=float, default=9.0)
    s = sub.add_parser("style")
    s.add_argument("files", nargs="+")
    a = p.parse_args()
    {"drawio": cmd_drawio, "diff": cmd_diff, "pdf": cmd_pdf, "style": cmd_style}[a.cmd](a)


if __name__ == "__main__":
    main()
