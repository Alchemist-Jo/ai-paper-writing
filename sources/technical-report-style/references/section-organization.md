# 章节组织与格式偏好

本参考规定章节如何分组、命名和展开。它适用于已有中文技术报告，以及中英文 AI 技术博客、教程和课程笔记。构建新研究报告仍由 `research-report` 负责；英文投稿论文的 section conventions 仍由 `paper-polish` 负责。

## 全局原则

1. **少量大节，避免小节碎片化。** 每个主节承担一个完整问题或方法模块。只有当子问题具有独立目标、推导或证据时才创建 subsection。
2. **标题可独立理解。** 标题直接命名技术对象与该节任务，例如 `Distributional shift 及其误差累积`。不用 `从行动开始`、`雾更浓以后`、`先看数字`、`两个旋钮` 等只能依赖上下文理解的标题。
3. **一个 section 完成一条逻辑弧。** 默认顺序是：问题或缺口 → 对象与假设 → 方法或推导 → 例子、图表或实验 → 机制解释与限制 → 下一问题。
4. **标题不替代过渡。** 主节之间需要一段正文说明上一节得到什么、当前还缺什么、下一节为何出现。
5. **图表与公式归属明确。** 公式、图、表、算法放在解释它们的 section 内，不单独堆成“实验结果”“更多分析”等无任务小节。
6. **标题层级稳定。** 文档标题使用 `#`；主节使用 `##`；节内技术问题使用 `###`；只有长推导中的真正子步骤才使用 `####`。避免超过四层。

## 中文技术博客与教程

### 推荐骨架

根据内容选择 3–6 个主节，不强制凑齐：

1. **问题设定与动机**：具体场景、任务对象、已有方法的缺口。
2. **基本对象与符号**：术语框架、输入输出、假设和 running example。
3. **核心机制或推导**：每个方法模块一个完整主节；复杂推导可以按真实步骤使用少量子节。
4. **受控例子或实验**：图表、代码结果、机制解释和适用边界。
5. **方法局限与扩展**：按问题类型组织，不做方法名目录。
6. **主线收束与延伸阅读**：回到 running example，说明学习目标如何变化；延伸阅读只放链接，不伪装成练习题。

### Section 内部

- 开头一句写当前问题，不能只重复标题。
- 公式前说明计算对象和出现原因，公式后解释符号与优化意义。
- running example 贯穿同一 section，不能在每个小节重新换故事。
- 方法比较按“问题出现、方法介入、系统发生什么变化、代价是什么”组织。
- 总结段不使用分号串联方法名。回到具体例子，并用条件句说明 trade-off。

## 中文证据报告与实验总结

本 Skill 只重组已有文本，不从原始日志创建报告。若已有文档需要结构修复，优先保留 3–5 个决策导向主节：

1. **Summary**：只写改变决策的已确认结论和未证明事项。
2. **Method / 实验设置**：实际数据、方法、配置、协议和偏差。
3. **Results**：可比较结果、失败和不完整运行，避免解释混入结果表。
4. **Analysis**：机制、趋势、替代解释、trade-off 和限制。
5. **Confusions / 未决问题**：异常、冲突证据和下一项有效检查。

不要为了形式强制创建空节。没有 Confusions 时可以省略；已有报告结构明确时，默认轻改而非整篇重排。

## English AI technical blogs and tutorials

Use 3–6 main sections with the same dependency order:

1. problem and concrete constraint;
2. objects, terminology, and notation;
3. mechanism, derivation, or progressive disclosure;
4. executable or visual evidence;
5. limitations, alternative explanations, and transition;
6. recap and references when needed.

A section title names the object and operation, not a rhetorical journey. Each paragraph has one job. Do not copy blog pacing into English academic-paper sections.

## 禁止模式

- 标题下面只有一句与标题同义的正文。
- 连续多个只有一段的小节。
- `更多分析`、`一些发现`、`其他问题`、`后来`、`下一步` 等无对象标题。
- 把一个方法的 motivation、公式和结果拆到相距很远的三个小节。
- 在总结中新引入方法、数据、限制或结论。
- 标题承诺“练习题”，正文却只有链接。
- 为了维持固定模板而创建空节或重复前文。

## 最终检查

1. 只看标题树，能否复述文章的问题链？
2. 每个主节是否有独立任务和完整逻辑弧？
3. 能否合并任何两个相邻、内容过短或职责重叠的小节？
4. 每个图、表、公式和算法是否位于解释它的 section？
5. 主节之间是否说明了“已得到什么、还缺什么、为什么继续”？
6. 总结是否回收主线，而非重复方法目录？
