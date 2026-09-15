# CVPR 2025 oral：视频生成方向的完整性与工作量

核验日期：2026-09-15。本次选择三个相邻方向的主会 oral，以官方日程确认展示类型；没有将 workshop oral、highlight 或普通 poster 计入。下文关于研究设计的判断属于基于论文的分析，不能用于预测审稿结果。

## 身份核验

| 论文 | 官方 oral 安排 |
| --- | --- |
| Motion Prompting: Controlling Video Generation with Motion Trajectories | 2025-06-13，Oral Session 1A，09:00 |
| Go-with-the-Flow: Motion-Controllable Video Diffusion Models Using Real-Time Warped Noise | 同场，09:15 |
| Navigation World Models | 2025-06-14，Oral Session 4B，13:45；另获 Best Paper Honorable Mention |

来源：[CVPR 官方日程](https://cvpr.thecvf.com/virtual/2025/calendar?filter_events=Art+Program)、[官方获奖名单](https://cvpr.thecvf.com/Conferences/2025/BestPapersDemos)。Motion Prompting 另有[官方 oral 页面](https://cvpr2023.thecvf.com/virtual/2025/oral/35272)。

## Go-with-the-Flow：方法改动集中，方向覆盖充分

核心机制是按光流构造时序相关、空间保持高斯性的噪声，再微调已有视频模型。对象控制、相机控制和运动迁移共享这套表示。架构和扩散训练目标保持一致。[作者项目页](https://eyeline-labs.github.io/Go-with-the-Flow/)

已确认的实验工作包括：噪声分布与运行时间验证；视频超分和重打光；VIPSeg 对象控制；DAVIS 的 43 个视频、DL3DV 的 100 个视频、WonderJourney 的 19 个视频上的运动或相机迁移；40 人用户研究。图像质量、控制准确性、时间一致性分别测量。首帧编辑和部分三维效果的证据以定性结果为主。[CVPR 正文，§4](https://openaccess.thecvf.com/content/CVPR2025/papers/Burgert_Go-with-the-Flow_Motion-Controllable_Video_Diffusion_Models_Using_Real-Time_Warped_Noise_CVPR_2025_paper.pdf)

作者披露 CogVideoX-5B 的数据源含 400 万视频，训练 30,000 步，8 张 A100 80GB、合计 40 GPU·天；另训练 AnimateDiff 检查跨架构适用性。数据源规模不等于每个视频实际参与训练的数量。DAVIS T2V 的 CoTracker mIoU 为 0.70，低于 DMT 的 0.85；其优势有明确适用条件。[作者全文，§3.5、表 2](https://arxiv.org/html/2501.08331v5)

**研究设计判断：**这篇最值得借鉴的是实验之间的关系。分布性质解释为何能保留单帧质量；超分和重打光检验时序噪声机制；三个控制分支检验统一表示的覆盖范围；不同基座检验适用范围。每组实验回答不同的关键问题。方法复杂度集中在一个机制，实验复杂度来自将整个控制方向解释清楚。不能由“架构改动少”推断其训练成本低。

## Motion Prompting：统一控制表示必须覆盖组合与密度变化

同一组点轨迹及可见性标记可描述对象、相机、二者联合控制、运动迁移和拖拽编辑；高层操作通过 motion prompt expansion 转成轨迹，再输入单个 ControlNet。[作者项目页](https://motion-prompting.github.io/)

量化主实验使用 DAVIS，轨迹数量从 1 到 2048，分别测视觉质量和轨迹误差；用户研究使用 30 个人工输入，评估运动遵循、运动质量和视觉质量。另比较稀疏、稠密及混合轨迹训练。单轨迹条件下，其 EPE 为 14.619，DragAnything 为 9.135。正文也明确指出各方法基座不同。相机与对象联合控制等应用主要由定性结果展示。[正文，§5、表 1–3](https://arxiv.org/html/2412.02700v2)

训练使用 220 万内部视频，预计算密集轨迹；训练 70,000 步，每次随机取 1000–2000 条轨迹，复用 Lumiere 超分模型输出 80 帧视频。论文未在这些训练细节中披露可直接换算的总 GPU·小时。[CVPR 补充材料，A.1](https://openaccess.thecvf.com/content/CVPR2025/supplemental/Geng_Motion_Prompting_Controlling_CVPR_2025_supplemental.pdf)

**研究设计判断：**统一性应由输入变化与组合条件证明。若只能分别完成单对象移动和单相机移动，尚未回答两者同时出现是否仍成立。进一步的控制实验可以覆盖对象数量、控制粒度、时间约束及控制组合。宽泛任务名称不能代替这些实验变量。

## Navigation World Models：生成质量应落实到模型的实际用途

NWM 以观察和导航动作预测未来图像，用同一模型完成视频预测、独立规划、外部策略候选排序及带约束规划。其训练数据涵盖四个机器人数据集，并研究加入无动作标注的 Ego4D 视频。[CVPR 正文，§1、§3](https://openaccess.thecvf.com/content/CVPR2025/papers/Bar_Navigation_World_Models_CVPR_2025_paper.pdf)

论文评估 1–16 秒预测、RECON 上的 2 秒轨迹规划、三类动作约束以及 Go Stanford 未见环境。RECON 的规划 ATE 从 NoMaD 的 1.93 降至 1.13。加入 Ego4D 后，未见环境预测改善，已知环境预测下降。默认模型 1B，使用 64 张 H100；这些结果的主要口径是离线预测和规划，不应转述为真实机器人长期闭环部署成功。[作者全文，§4](https://arxiv.org/html/2412.03572v2)

官方代码提供训练、未来状态预测、轨迹生成与规划评估；公开 checkpoint 覆盖 50M、200M、700M、1B 参数量。[官方代码](https://github.com/facebookresearch/nwm)、[官方模型卡](https://huggingface.co/facebook/nwm)

**研究设计判断：**“世界模型”这一命题需要回答预测为何对决策有用。NWM 将生成、决策效用、约束适应、未见环境与规模变化放在同一方向内。类似研究应选择能证明表示实际价值的下游用途；若主张可控、可编辑、可解释，就应分别验证控制执行、修改后的结果以及输出与可执行状态的一致性。NWM 的训练规模不适合作为轻量项目的资源目标。
