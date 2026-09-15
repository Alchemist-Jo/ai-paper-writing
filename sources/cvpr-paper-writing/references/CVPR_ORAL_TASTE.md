# CVPR oral 的研究广度：统一表示、任务关系与证据完整性

## 1. Oral 身份

| 论文 | 官方安排 |
| --- | --- |
| RandAR: Decoder-only Autoregressive Visual Generation in Random Orders | CVPR 2025，6 月 13 日，Oral Session 1A: Image & Video Synthesis，第 5 篇 |
| VGGT: Visual Geometry Grounded Transformer | CVPR 2025，6 月 13 日，Oral Session 2A: 3D Computer Vision，第 5 篇；Best Paper |
| Efficiently Reconstructing Dynamic Scenes One D4RT at a Time | CVPR 2026，6 月 5 日，Oral Session 2D: Spatio-Temporal Reconstruction，第 2 篇；Best Paper |

来源：[CVPR 2025 官方程序册](https://media.eventhosts.cc/Conferences/CVPR2025/CVPR_main_conf_2025.pdf)、[2025 官方获奖名单](https://cvpr.thecvf.com/Conferences/2025/BestPapersDemos)、[CVPR 2026 官方程序册](https://media.eventhosts.cc/Conferences/CVPR2026/CVPR_main_conf_2026_15.pdf)、[2026 官方获奖说明](https://cvpr.thecvf.com/Conferences/2026/News/Best_Papers)。程序册可直接按论文名称检索。

## 2. RandAR：训练原则变化产生多类能力

**已确认。**核心操作为随机排列图像 token，并在待预测位置前插入位置指令 token，沿用标准 decoder-only 自回归架构。生成、并行解码、局部编辑、外扩、分辨率外推和特征提取共享该模型。实验包含 ImageNet 生成与线性探测、SPair-71k 对应匹配；同配置光栅顺序基线、位置指令消融、模型规模及解码步数变化提供机制证据。343M、775M、1.4B 三种规模训练 300 epochs，约 360K iterations，batch size 1024。[CVPR 正文，§3–4](https://openaccess.thecvf.com/content/CVPR2025/papers/Pang_RandAR_Decoder-only_Autoregressive_Visual_Generation_in_Random_Orders_CVPR_2025_paper.pdf)

**证据细节。**重新遍历图像时，SPair-71k 的 RandAR 特征 PCK 从 22.1 升至 31.3；光栅顺序模型对应结果从 24.5 降至 3.6。该实验将生成顺序与特征用途联系起来。高分辨率外推还使用分层顺序及 spatial context guidance；外推中的高频结构是作者展示的失败类型。论文披露了推理延迟，本文未找到可直接换算的训练 GPU·小时。[作者全文，§4 及补充实验](https://arxiv.org/html/2412.01827v2)、[作者项目页](https://rand-ar.github.io/)

**研究判断。**RandAR 的说服力来自一个可追踪的变量关系：训练中解除固定顺序限制，推理时才能重新选择已知位置与待预测位置。编辑、外扩、并行解码分别检查这一自由度的不同用途；特征实验进一步检查生成模型是否学习到了可复用的图像信息。这种广度具有明确的内部关系。

两套命名数据集已经支撑了较广的论文范围，说明 oral 的完整性没有固定 benchmark 数量。真正影响判断的是：主张中不同能力是否被直接检验，应用差异是否来自同一个方法属性，以及关键替代解释是否有实验区分。

## 3. VGGT：共享学习需要证明任务之间的关系

**已确认。**VGGT 使用交替的帧内与全局注意力，共享骨干预测相机、深度、点图及跟踪特征。主要评测覆盖 CO3Dv2/Re10K 相机位姿、DTU 多视角深度、ETH3D 点图、ScanNet-1500 匹配；另以微调后的模型评估 GSO 新视角合成与 TAP-Vid 动态跟踪。[CVPR 正文，§3–4](https://openaccess.thecvf.com/content/CVPR2025/papers/Wang_VGGT_Visual_Geometry_Grounded_Transformer_CVPR_2025_paper.pdf)

**证据细节。**ETH3D 点图误差在联合监督时为 0.709，删除相机、深度、跟踪监督后分别为 0.834、0.727、0.790；相同参数量的注意力结构比较进一步检验骨干设计。1.2B 模型训练 160K iterations，使用 64 张 A100、9 天，训练来源列出 17 项。作者明确记录鱼眼/全景图、极端旋转及显著非刚性运动限制。新视角合成和动态跟踪经过额外适配及训练。[作者全文，§3.4、§4.5–5](https://arxiv.org/html/2503.11651v1)

**研究判断。**这篇论文将一个领域的相关输出共同建模，并给出了“共同学习是否有用”的直接证据。删除其他任务监督造成点图误差上升，比“一个模型拥有四个输出头”更能说明统一训练的研究价值。下游适配则回答共享表示能否继续使用。

## 4. D4RT：接口定义直接决定任务覆盖

**已确认。**D4RT 编码视频后，以查询 `(u,v,t_src,t_tgt,t_cam)` 预测一个三维点；改变源帧、目标时间和参考相机，得到深度、动态轨迹、点云及相机参数。查询独立通过 cross-attention 解码。训练使用 1B 编码器、144M 解码器，48 帧、256×256 输入，2048 查询；11 个公开数据源加内部数据，500K steps，64 TPU chips，略超 2 天。[CVPR 正文，§2、§4](https://openaccess.thecvf.com/content/CVPR2026/papers/Zhang_Efficiently_Reconstructing_Dynamic_Scenes_One_D4RT_at_a_Time_CVPR_2026_paper.pdf)

**证据细节。**评测包括 TAPVid-3D 的相机/世界坐标跟踪，Sintel/ScanNet 点云，Sintel/ScanNet/KITTI/Bonn 深度及 Sintel/ScanNet/Re10K 位姿。消融覆盖局部 RGB patch、编码器规模、辅助损失及公开数据训练。局部 patch 使 Sintel 深度 AbsRel 从 0.366 降至 0.302，位姿 ATE 从 0.173 降至 0.091。效率曲线与全像素跟踪展示共同检验查询设计的用途。[CVPR 正文，表 3–9](https://openaccess.thecvf.com/content/CVPR2026/papers/Zhang_Efficiently_Reconstructing_Dynamic_Scenes_One_D4RT_at_a_Time_CVPR_2026_paper.pdf)

长视频展示使用重叠分段与 Sim(3) 对齐。高分辨率实验区分增加查询密度与使用原分辨率 RGB patch；仅提高查询密度时高频细节仍有限。本文未在已核验正文及附录中找到独立的系统性失败分类。[作者全文，附录 B–D](https://arxiv.org/html/2512.08924v2)

**研究判断。**D4RT 的中心贡献可直接写成输入与输出的数学定义。各任务是同一组变量的不同取值方式，这让覆盖范围可以从接口推导。稀疏监督、计算量随查询数量变化、跨参考坐标输出和全像素追踪又分别验证了接口的训练、效率、表示及应用价值。

它特别适合校准“把一个方向做扎实”的含义：方法主体保持集中，论文把这一主体的精度、效率、覆盖范围、可扩展性及关键实现选择逐项落实为证据。辅助损失、数据处理和可视化工作依然很多；这些实际投入应当计入研究工作量。
