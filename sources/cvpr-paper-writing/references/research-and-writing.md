# CVPR 研究与写作补充案例

## 5. 案例

### Molmo and PixMo：两阶段训练与广泛基准

CVPR 2025 官方议程将其列为 6 月 13 日 09:45，Oral Session 1B。[官方日程](https://cvpr.thecvf.com/virtual/2025/calendar?filter_events=Art+Program)

论文采用图像描述预训练和多任务微调两个主要训练阶段。主评测含 11 个基准：VQAv2、TextVQA、ChartQA、DocVQA、InfoVQA、AI2D、MMMU、MathVista、RealWorldQA、CountBenchQA、PixMo-Count；另报告指点、读钟、AndroidControl 和人工评价。数据与模型消融覆盖整套基准，计数实验进一步替换点坐标和输出顺序。其 11 项平均结果与具体能力诊断承担不同职责。[CVPR 正文，§4–6](https://openaccess.thecvf.com/content/CVPR2025/papers/Deitke_Molmo_and_PixMo_Open_Weights_and_Open_Data_for_State-of-the-Art_CVPR_2025_paper.pdf)、[作者全文，表 1–4](https://arxiv.org/html/2409.17146v2)
