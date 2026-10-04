# API 参考

## SmithChart 构造函数

### 网格图层

- `show_impedance=True`：绘制实线阻抗网格。
- `show_admittance=False`：启用时绘制虚线导纳网格。
- `show_scale_labels=True`：显示归一化电阻、电导、电抗与电纳刻度数字。
- 所有刻度文字为黑色。
- 阻抗实部与虚部刻度向右旋转 90 度；实轴刻度置于横轴上方。
- 导纳实部与虚部刻度向左旋转 90 度；实轴刻度置于横轴下方。
- 虚部刻度仅显示带正负号数值（如 `+0.5`、`-0.5`），不加 `x` 或 `b` 前缀。
- 所有虚部刻度置于史密斯圆外侧，相邻径向错开以减少重叠。
- 每个虚部刻度外加白底细灰边方框。
- 自动检测角度间距不足的刻度，将其移到额外径向层，层间距随稀疏/标准/密集网格调整。

### 图片尺寸

- `figsize=(8, 8)`：以英寸设置 Matplotlib 画布。
- `width_px` 与 `height_px`：以像素设置画布尺寸，优先级高于 `figsize`。
- `dpi=160`：在像素与英寸间换算，并控制位图输出分辨率。

示例：

```python
chart = SmithChart(width_px=1800, height_px=1800, dpi=180)
```

### 网格密度自动调整

设置 `grid_density="auto"`，依据图片较短边选择网格线族数量：

- 小于 700 px：稀疏（sparse）网格。
- 700 px 至 1400 px（不含）：标准（standard）网格。
- 大于等于 1400 px：密集（dense）网格。

显式设置 `grid_density` 为 `sparse`、`standard` 或 `dense` 可强制使用预设。因此图片越大电阻、电抗、电导、电纳线越多，图片越小线越少。

手动指定的数值始终覆盖对应的自动预设：

```python
chart = SmithChart(
    width_px=1800,
    height_px=1800,
    resistance_values=(0, 0.25, 0.5, 1, 2, 4, 8),
)
```

### 样式

- `grid_linewidth=0.9`：控制阻抗与导纳网格线宽。
- `label_fontsize=None`：依据输出尺寸自动选择字号；传入数字可覆盖。
- `overlay_scale=1.35`：统一放大用户添加的点、标注、线段、箭头、移动弧与驻波圆；通过 `style` 显式传入的值优先级更高。

## 点的方法

- `add_impedance(r, x, label=None, **style)`：添加阻抗点（归一化 `z = r + jx`）。
- `add_admittance(g, b, label=None, **style)`：添加导纳点（归一化 `y = g + jb`）。
- `add_gamma(gamma, label=None, **style)`：按反射系数直接添加点。
- `add_label(point, text, dx=0.035, dy=0.035, **style)`：为点或坐标添加文字标注。

## 绘制方法

- `add_line(start, end, arrow=False, **style)`：连接两点，可加箭头。
- `draw_swr_circle(point, **style)`：绘制等驻波比圆（`|Γ| = 常数`）。
- `flip_to_admittance(point, label=None, connect=True)`：阻抗↔导纳 180 度翻转，并可选连线。
- `move_wavelength(start, distance, toward_generator=True, label=None, draw_arc=True)`：沿等 `|Γ|` 圆按波长移动，可画弧与箭头。

## 批量操作

`execute()` 支持的 `type` 取值：

- `impedance`（阻抗点）：必填 `r`、`x`；可选 `label`、`style`。
- `admittance`（导纳点）：必填 `g`、`b`；可选 `label`、`style`。
- `gamma`（反射系数点）：必填 `gamma`；可选 `label`、`style`。
- `label`（文字标注）：必填 `point`、`text`；可选 `style`。
- `line`（线段/箭头）：必填 `start`、`end`；可选 `arrow`、`style`。
- `swr`（驻波圆）：必填 `point`；可选 `style`。
- `flip`（阻抗导纳翻转）：必填 `point`；可选 `label`、`connect`。
- `move`（按波长移动）：必填 `start`、`distance`；可选 `toward_generator`、`label`、`draw_arc`。

## 导出

调用 `save(path)`，扩展名支持 `.png`、`.svg`、`.pdf`。批量流程导出后调用 `close()`。
