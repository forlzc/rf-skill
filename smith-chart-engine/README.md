# Smith Chart Engine

> 可复用的史密斯圆图 Python/Matplotlib 绘制引擎，面向《射频通信电路》教学、PPT 插图、学习通资源与自动化出题。

A reusable Python/Matplotlib Smith-chart engine for RF communication circuit teaching, PPT figures, LearningTong resources, exercises, and other automated Skills.

## 功能 Features

- **阻抗网格**：实线绘制；支持按图片尺寸自动增减圆族密度。
- **导纳网格**：蓝色虚线，可开关（`show_admittance`）；与阻抗网格叠加。
- **刻度标注**：阻抗、导纳实部分置横轴上下两侧；实部与虚部刻度均旋转 90°（阻抗向右、导纳向左），虚部刻度置于圆外并带白底灰框，自动避让重叠。
- **尺寸自适应**：`width_px` / `height_px` / `dpi` 控制出图尺寸；大图自动增加网格线族数量，小图自动减少，保持清晰可读。
- **用户标注放大**：`overlay_scale` 统一放大点、标签、线段、箭头、驻波圆与移动弧，便于课堂展示。
- **坐标点**：归一化阻抗 `z = r + jx`、导纳 `y = g + jb`、反射系数 `Γ` 三类点。
- **图形操作**：标签、线段、箭头、等驻波比圆（SWR 圆）、阻抗↔导纳 180° 翻转、沿等 |Γ| 圆按波长移动。
- **任务清单接口**：`execute()` 接受 JSON 式操作列表，供其他 Skill / Agent 直接调用。
- **输出格式**：PNG、SVG、PDF。

## 安装 Install

```bash
python -m pip install -e .
```

依赖：`matplotlib`、`numpy`。

## 快速开始 Quick Start

```python
from smith_chart_engine import SmithChart

chart = SmithChart(
    show_impedance=True,
    show_admittance=True,
    width_px=1800,
    height_px=1800,
    dpi=180,
    grid_density="auto",
    overlay_scale=1.35,
)
chart.add_impedance(1, 1, label="A")
chart.draw_swr_circle("A")
chart.flip_to_admittance("A", label="A'")
chart.move_wavelength("A", 0.125, toward_generator=True, label="B")
chart.add_line("A", "B", arrow=True)
chart.save("smith_chart.svg")
chart.close()
```

运行完整教学示例（密集网格 1800×1800）：

```bash
python examples/teaching_demo.py
```

## 任务清单接口 Task-list Interface

```python
chart.execute([
    {"type": "impedance", "r": 1, "x": 1, "label": "A"},
    {"type": "swr", "point": "A"},
    {"type": "move", "start": "A", "distance": 0.125, "toward_generator": True, "label": "B"},
    {"type": "line", "start": "A", "end": "B", "arrow": True},
])
```

## 常用参数 Common Parameters

| 参数 | 说明 |
| --- | --- |
| `show_impedance` / `show_admittance` | 阻抗网格 / 导纳网格开关 |
| `width_px`, `height_px`, `dpi` | 出图尺寸控制 |
| `grid_density` | `"auto"` / `"sparse"` / `"standard"` / `"dense"` / 自定义数值列表 |
| `overlay_scale` | 用户标注放大倍数（默认 1.35） |
| `show_scale_labels` | 是否显示刻度数字（默认 True） |

更多接口与参数见 [`SKILL.md`](SKILL.md) 与 [`references/api_reference.md`](references/api_reference.md)。

## 测试 Tests

```bash
pytest
```

## 协作 GitHub Collaboration

Fork 仓库、新建特性分支、为改动补充测试后提交 Pull Request。适合后续扩展：单支节匹配、双支节匹配、匹配路径搜索、外围波长刻度、动画 GIF/MP4 等。

## 许可 License

MIT License.
