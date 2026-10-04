# API Reference

## SmithChart constructor

### Grid layers

- `show_impedance=True`: draw the solid impedance grid.
- `show_admittance=False`: draw the dashed admittance grid when enabled.
- `show_scale_labels=True`: show normalized resistance, conductance, reactance, and susceptance scale numbers.
- Render all scale text in black.
- Rotate impedance real and imaginary scale numbers right by 90 degrees; place real-axis numbers above the horizontal axis.
- Rotate admittance real and imaginary scale numbers left by 90 degrees; place real-axis numbers below the horizontal axis.
- Show imaginary-family labels as signed values such as `+0.5` and `-0.5`, without `x` or `b` prefixes.
- Place all imaginary-family labels outside the Smith-chart boundary and stagger neighboring radii to reduce overlap.
- Draw a square white box with a thin gray border around each imaginary-family label.
- Automatically detect labels with insufficient angular spacing and move them to additional radial layers, with spacing adapted to sparse, standard, and dense grids.

### Image size

- `figsize=(8, 8)`: set the Matplotlib canvas in inches.
- `width_px` and `height_px`: set the requested canvas size in pixels. These values take precedence over `figsize`.
- `dpi=160`: convert between pixel and inch dimensions and control raster output resolution.

Example:

```python
chart = SmithChart(width_px=1800, height_px=1800, dpi=180)
```

### Automatic grid density

Set `grid_density="auto"` to select the number of grid-line families from the shorter image side:

- Below 700 px: `sparse` grid.
- From 700 px to below 1400 px: `standard` grid.
- At least 1400 px: `dense` grid.

Set `grid_density` to `sparse`, `standard`, or `dense` to force a preset. A larger image therefore receives more resistance, reactance, conductance, and susceptance lines, while a smaller image receives fewer lines.

Manually specified values always override their corresponding automatic preset:

```python
chart = SmithChart(
    width_px=1800,
    height_px=1800,
    resistance_values=(0, 0.25, 0.5, 1, 2, 4, 8),
)
```

### Styling

- `grid_linewidth=0.9`: control impedance and admittance grid line width.
- `label_fontsize=None`: select label size automatically from output dimensions; supply a number to override it.
- `overlay_scale=1.35`: uniformly enlarge user-added points, labels, line segments, arrows, movement arcs, and SWR circles. Explicit values supplied through `style` remain higher priority.

## Point methods

- `add_impedance(r, x, label=None, **style)`
- `add_admittance(g, b, label=None, **style)`
- `add_gamma(gamma, label=None, **style)`
- `add_label(point, text, dx=0.035, dy=0.035, **style)`

## Drawing methods

- `add_line(start, end, arrow=False, **style)`
- `draw_swr_circle(point, **style)`
- `flip_to_admittance(point, label=None, connect=True)`
- `move_wavelength(start, distance, toward_generator=True, label=None, draw_arc=True)`

## Batch operations

Supported `type` values for `execute()`:

- `impedance`: requires `r`, `x`; optional `label`, `style`.
- `admittance`: requires `g`, `b`; optional `label`, `style`.
- `gamma`: requires `gamma`; optional `label`, `style`.
- `label`: requires `point`, `text`; optional `style`.
- `line`: requires `start`, `end`; optional `arrow`, `style`.
- `swr`: requires `point`; optional `style`.
- `flip`: requires `point`; optional `label`, `connect`.
- `move`: requires `start`, `distance`; optional `toward_generator`, `label`, `draw_arc`.

## Export

Call `save(path)` with `.png`, `.svg`, or `.pdf`. Call `close()` after export in batch workflows.
