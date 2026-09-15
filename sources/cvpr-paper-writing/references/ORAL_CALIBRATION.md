# 代码与执行反馈研究：工作量校准

更新：2026-09-15。以下“已确认”来自论文、补充材料及官方会议资料；“研究判断”为案例分析，不代表会议评审规则。较新的 CVPR 广度研究另见 `CVPR_ORAL_TASTE.md`。

## VideoCoCo 的实际复杂度

**已确认。** 对应论文为 [VideoCoCo: Code-as-CoT for Physically-Consistent Video Generation via an Agentic Dual-Engine System，arXiv:2607.27380v2](https://arxiv.org/html/2607.27380v2)，2026-08-08 修订。arXiv 未标注会议录用，不能作为 oral 身份样本。

正文 §3 的系统为：文本→coding agent→Blender 程序→白模视频；instruction agent 根据文本与白模编写外观指令；OmniWeaving editor 根据两者输出视频。代码角色不训练。数据集含 3000 个 draft–instruction–target 三元组，Seedance 2.0 每条生成一次目标视频。训练仅适配 editor，比较不训练、LoRA、全参数微调。正文没有策略 RL、自博弈或语义反馈搜索。

评测是 PhyGenBench（mechanics、optics、thermal、material）和 VBench-2.0 的三个物理维度子集。PhyGenBench 平均值：原模型 0.475；不训练的完整流水线 0.506；LoRA 0.558。该消融区分流水线与 editor 适配，尚未分别隔离代码表示、白模条件和编辑指令的作用。LoRA rank、训练步数、GPU 型号数量和时长未报告。因而能据此约束组件与数据量，不能据此承诺相同 GPU 成本。[论文 §3–4](https://arxiv.org/html/2607.27380v2#S3)

## VISPROG：覆盖不同任务的程序接口

**身份已确认。** CVPR 2023 官方程序手册第 63 页列为 `Oral-Award-Thu`，15:20 演讲；官方另授予 Best Paper。[会议手册](https://media.icml.cc/Conferences/CVPR2023/CVPR_2023_MainConference_ProgramGuide.pdf#page=63)、[获奖公告](https://cvpr.thecvf.com/Conferences/2023/BestPaperAwards)

**已确认。** GPT-3 从少量指令—程序示例生成模块调用，所有预训练模型冻结。20 个模块复用 OWL-ViT、DSFD、MaskFormer、CLIP、ViLT、Stable Diffusion 及 Python 操作。程序执行记录形成可检查的视觉解释。[论文 §3](https://openaccess.thecvf.com/content/CVPR2023/papers/Gupta_Visual_Programming_Compositional_Visual_Reasoning_Without_Training_CVPR_2023_paper.pdf)

真实评测覆盖四类任务：GQA 组合问答、NLVRv2 图像对推理、自建知识标注、自建图像编辑。GQA 为按问题类型抽样的子集；NLVRv2 在 250 条开发样本选提示，再测完整 public test。知识标注含 46 张图、100 条指令、253 个物体；编辑含 65 张图、107 条指令。另有约 100 个样本/任务的错误归因及人工修改指令后的结果。GQA 的 50.5 对比 ViLT 的 47.8 使用五次投票；NLVRv2 62.4 同样使用五次投票。这里存在明确采样成本，论文未给出完整 API/GPU 预算。[论文 §4–5](https://openaccess.thecvf.com/content/CVPR2023/papers/Gupta_Visual_Programming_Compositional_Visual_Reasoning_Without_Training_CVPR_2023_paper.pdf)

## ViperGPT：从图像定位扩展到视频推理

**身份已确认。** ICCV 2023 官方日程在 10 月 5 日 16:30–18:00 `Orals` 中列出该文，地点 Paris Sud。官方程序手册同样列出。[官方日程](https://iccv2023.thecvf.com/main.conference.program-107.php)、[程序手册](https://iccv2023.thecvf.com/telechargements/fichiers/1696500277.iccv23.program.booklet.updated.pdf)

**已确认。** Codex 根据 Python API 文档生成程序，调用冻结的 GLIP-L、X-VLM、MiDaS、BLIP-2 Flan-T5 XXL 与 GPT-3；用 Python 原生控制流执行，无任务微调。主实验为四类任务、五个命名数据集：RefCOCO/RefCOCO+ 定位、GQA 组合问答、OK-VQA 知识问答、NExT-QA 视频因果/时序问答。视频扩展复用图像模型并增加 VideoSegment 接口。NExT-QA 报告完整集合和 hard split，不能只以优势更大的 hard split 代表全体。[论文 §3–4、附录 A](https://arxiv.org/pdf/2303.08128)

其机制实验固定已生成程序，将某一模块输出替换为无信息默认值，测量准确率变化；同时检查感知模块和 Python 操作。另有超出基准的查询、附加情境条件示例。训练新增成本为零，完整推理/API预算未报告。[论文 §5](https://arxiv.org/pdf/2303.08128)

## Visual Program Distillation：搜索与蒸馏已经成立的近邻

**身份已确认。** CVPR 2024 官方页面明确标记 `Oral`，属于 `Orals 3B Vision, Language, and Reasoning`。[官方 oral 页面](https://cvpr2023.thecvf.com/virtual/2024/oral/32045)

**已确认。** PaLM-2 为每题采样多个程序，执行后按照答案过滤，把执行轨迹转成自然语言 CoT，再用答案损失和解释损失 LoRA 微调 PaLI-3 5B / PaLI-X 55B。有标签时过滤答案正确性；无标签时取评分最高的可执行程序，不能把这一分支称为已验证正确。[论文 §3](https://openaccess.thecvf.com/content/CVPR2024/papers/Hu_Visual_Program_Distillation_Distilling_Tools_and_Programmatic_Reasoning_into_Vision-Language_CVPR_2024_paper.pdf)

通用模型评测含八个命名基准：VQAv2、GQA、OK-VQA、A-OKVQA、TallyQA、TextVQA、POPE、MMBench；A-OKVQA 与 TallyQA 各有两种口径，不能将其全部计作独立数据集。另有 Hateful Memes 迁移、四个数据集的专用微调，以及 600 条样本、每条三位标注者的人工解释评价。自身 Instruct 对照保持数据、训练参数和步数一致；PaLI-X 的 GQA 增益为 1.6 点，TallyQA complex 为 1.2 点，MMBench 为 1.2 点。[论文 §4–5](https://openaccess.thecvf.com/content/CVPR2024/papers/Hu_Visual_Program_Distillation_Distilling_Tools_and_Programmatic_Reasoning_into_Vision-Language_CVPR_2024_paper.pdf)

通用微调 rank=8、batch=128、8000 步；55B 使用 128 TPU-v3 约两天，5B 使用 32 TPU-v4 约 20 小时，另有专用微调成本。300 题测时在相同 128 TPU-v5 条件下，程序生成与执行平均 8.9 秒，蒸馏模型 0.8 秒。GPU 等效成本未报告，不作换算。[补充材料 §C.3–C.4](https://openaccess.thecvf.com/content/CVPR2024/supplemental/Hu_Visual_Program_Distillation_CVPR_2024_supplemental.pdf)
