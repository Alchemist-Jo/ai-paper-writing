# 按当前产物组织工作

选择一个主要目标，完成用户要求的整体范围；完整论文重构可以连续包含分析、组织和写作，不要求用户逐轮授权。以下文件均相对于本文件；源文件节号以原始标题为准，完整阅读指定小节，不能以索引替代正文。

| 当前任务 | 执行动作与产物 | 深读材料 |
| --- | --- | --- |
| 中心主张与全文结构 | 从完整结果建立主张证据关系，再确定问题、方法、结果与贡献顺序 | architecture-and-language 全文；anatomy/docs/iclr-full-paper-blueprint.md §1、§4、§6、§19、§20 |
| 方法与理论 | 输入、状态、变换、输出；假设、推导、可观察预测与实测对应 | 同蓝图 §8、§9、§10、§15、§16 |
| 实验设计 | 每项实验写比较、控制、指标、预算及不同结果改变的结论 | 同蓝图 §11；anatomy/reports/statistical_analysis_250.md §六、§七；相关 CVPR 案例 |
| 已有结果分析 | 保留完整范围，识别异质性、规模关系、交互、失败与成本 | 同统计报告 §七、§九、§十；同蓝图 §12、§13、§19 |
| 新颖性核查 | 精确重叠、技术差异和区分证据 | 同蓝图 §7；最接近的一手论文；需要时读取旧 closure-kit 的 Prompt F |
| 独立审查 | 对具体命题提供可核验问题、影响和修改；没有问题时明确说明 | 同蓝图 §21；当前稿件和原始证据。可用独立子 agent 时使用全新上下文；工具不可用时明确为当前上下文审查 |
| 重复讨论收敛 | 关闭无新证据的意见，给出下一项能改变结论的行动 | evidence-contract；需要时读取旧 closure-kit 的 Prompt H |
| 摘要/引言/相关工作 | 按功能顺序写出指定章节 | 同蓝图 §5/§6/§7；anatomy/docs/writing-playbook.md 对应 §3/§4/§5 |
| 方法/理论/结果/消融 | 先证据与对象，后连贯段落 | 同蓝图 §9/§10/§12/§13；同 writing-playbook §6/§7/§9/§10 |
| Discussion/结论/附录 | 回收已有发现、范围与复现材料 | 同蓝图 §14、§17；同统计报告 §十、§十一 |
| 示例风格模仿 | 获取原文、段落功能映射、图表视觉规格、用项目证据重建 | reference-imitation 全文；实际示范论文相应完整章节；样本的 reading 与 visual audit |
| 图表与 caption | 为主张确定图表职责、统计编码、caption、可编辑源码 | figures-and-tables 全文；anatomy/reports/visual_design_analysis_250.md 相关完整章节及 CSV |

上表 `anatomy/` 指 skill 根目录的 `sources/anatomy/`，从本文件访问为 `../sources/anatomy/`。旧 closure-kit 位于 `../sources/iclr-paper-writing/references/closure-kit.md`。蓝图与旧 prompts 中固定句数、图表数、页数、流程阶段和机械评分不具有执行约束；按当前 references 改写。

原有 A-I 的有效研究问题已纳入这些产物路线。不要在交付正文前复制整套契约或要求用户学习 prompt 编号。仅生成本轮需要的工作记录，避免每次写一句 caption 都创建整套文档。
