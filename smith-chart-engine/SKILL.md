---
name: smith-chart-engine
description: 当需要为射频通信电路、传输线教学、阻抗/导纳换算、匹配习题、PPT 插图或学习通资源创建、标注、调整尺寸或导出史密斯圆图时使用本技能。它提供一个可复用的 Python + Matplotlib 引擎，支持实线阻抗网格、可选虚线导纳网格、旋转刻度标注、随图片尺寸自动调整网格密度、点/线/弧操作、等驻波比圆、按波长移动，以及 PNG/SVG/PDF 导出。
agent_created: true
---

# 史密斯圆图引擎

## 概述

用确定性的 Python 代码生成可复用的史密斯圆图基图与教学标注。阻抗圆用实线绘制，可选导纳网格用蓝色虚线渲染，网格线族数量随图片尺寸自动变化。

## 工作流程

1. 确认所需的网格图层、图片尺寸、归一化数值、标注内容与输出格式。
2. 从 `src/smith_chart_engine` 导入 `SmithChart`，或用 `pip install -e .` 安装本包。
3. 需要精确控制出图尺寸时，设置 `width_px`、`height_px` 与 `dpi`。
4. 除非任务明确要求稀疏（sparse）、标准（standard）、密集（dense）或自定义网格，否则保持 `grid_density="auto"`。
5. 当用户添加的点、标注、线段、箭头、驻波圆或移动弧需要更醒目时，设置 `overlay_scale`；演示场景保持默认 `1.35` 即可。
6. 添加点、标注、线段、箭头、驻波圆、翻转或按波长移动。
7. 仅以 PNG、SVG 或 PDF 格式保存。
8. 可编辑的教学图优先用 SVG，PPT 或学习通上传优先用 PNG。

## 网格密度自动调整

根据图片较短的像素边选择网格线族：

- 小于 700 px 用稀疏（sparse）网格。
- 700 px 至 1400 px（不含）用标准（standard）网格。
- 大于等于 1400 px 用密集（dense）网格。

图片越大，电阻/电抗与电导/电纳线族越多；图片越小，线族越少以保持清晰。若显式传入 `resistance_values`、`reactance_values`、`conductance_values` 或 `susceptance_values`，则保留手动设置，不自动覆盖。

## 刻度标注规范

- 所有刻度文字均为黑色。
- 阻抗实部与虚部刻度均向右旋转 90 度。
- 导纳实部与虚部刻度均向左旋转 90 度。
- 阻抗实轴刻度放在横轴上方，导纳实轴刻度放在横轴下方。
- 虚部刻度仅显示带正负号数值（如 `+0.5`、`-0.5`），不加 `x` 或 `b` 前缀。
- 所有虚部刻度置于史密斯圆外侧。
- 自动检测角度间距不足，将重叠的虚部刻度分配到额外的径向层。
- 每个虚部刻度外加白底细灰边方框。
- 小图时随网格密度一同减少刻度数量。

## 快速开始

```python
from smith_chart_engine import SmithChart

chart = SmithChart(
    show_impedance=True,
    show_admittance=True,
    width_px=1800,
    height_px=1800,
    dpi=180,
    grid_density="auto",
)
chart.add_impedance(1, 1, label="A")
chart.draw_swr_circle("A")
chart.flip_to_admittance("A", label="A'")
chart.save("smith.svg")
chart.close()
```

## 任务清单接口

当另一个技能或自动化任务需要以类 JSON 操作清单调用时，使用 `execute()`。

```python
chart.execute([
    {"type": "impedance", "r": 1, "x": 1, "label": "A"},
    {"type": "swr", "point": "A"},
    {"type": "move", "start": "A", "distance": 0.125, "toward_generator": True, "label": "B"},
    {"type": "line", "start": "A", "end": "B", "arrow": True},
])
```

## 坐标约定

- 阻抗按归一化 `z = r + jx` 处理。
- 导纳按归一化 `y = g + jb` 处理。
- 阻抗换算：`Gamma = (z - 1) / (z + 1)`。
- 导纳换算：`z = 1 / y`。
- 向信号源方向（toward_generator）的正波长距离对应反射系数平面上顺时针旋转。
- 旋转角度为 `4*pi*l/lambda`，因为反射系数相位随电长度变化两倍。

## 资源

- 完整尺寸、密度、方法与操作说明见 `references/api_reference.md`。
- 运行 `examples/teaching_demo.py` 查看 1800×1800 密集网格教学示例。
- 发布改动前请运行测试套件。
