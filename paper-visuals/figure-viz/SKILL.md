---
name: figure-viz
description: "Design or render research figures. Select tensor semantics, mathematical structure with TikZ, or measured data with matplotlib; route reference-image reconstruction to drawio-reconstruction."
---

# figure-viz

Select the mode that matches the requested deliverable. Read only its workflow and the references it requires. An explicit legacy name binds the corresponding mode. If the user requests several changes, apply their modes in dependency order.

| Mode | Select when | Read |
| --- | --- | --- |
| `render` | Render a research figure with TikZ or matplotlib. | [Original workflow](references/core-workflow.md) |
| `tensor` | Design tensor shapes, matrix blocks or formula semantics. | [Original workflow](modes/tensor-formula-viz/workflow.md) |

For a structural or tensor figure, read the tensor mode and then the core renderer workflow. The tensor mode owns semantics; the renderer owns export. Data-only plots load the renderer workflow and its chart-family reference. A supplied reference image requiring an editable Draw.io reconstruction uses `drawio-reconstruction`.
