---
name: smith-chart-engine
description: This skill should be used when creating, annotating, resizing, or exporting Smith charts for RF communication circuits, transmission-line teaching, impedance/admittance conversion, matching exercises, PPT figures, or LearningTong resources. It provides a reusable Python and Matplotlib engine with solid impedance grids, optional dashed admittance grids, rotated scale labels, image-size-aware automatic grid density, point/line/arc operations, SWR circles, wavelength movement, and PNG/SVG/PDF export.
agent_created: true
---

# Smith Chart Engine

## Overview

Generate reusable Smith-chart base figures and teaching annotations with deterministic Python code. Keep impedance circles solid, render the optional admittance grid with dashed blue lines, and automatically change the number of grid-line families according to image dimensions.

## Workflow

1. Confirm the requested grid layers, image dimensions, normalized values, annotations, and output format.
2. Import `SmithChart` from `src/smith_chart_engine` or install the package with `pip install -e .`.
3. Set `width_px`, `height_px`, and `dpi` when an exact image size is required.
4. Keep `grid_density="auto"` unless the task explicitly requires sparse, standard, dense, or custom grid values.
5. Set `overlay_scale` when user-added points, labels, lines, arrows, SWR circles, or movement arcs need stronger visual emphasis. Keep the default `1.35` for presentation-friendly output.
6. Add points, labels, lines, arrows, SWR circles, rotations, or wavelength movements.
7. Save only as PNG, SVG, or PDF.
7. Prefer SVG for editable teaching graphics and PNG for PPT or LearningTong uploads.

## Automatic Grid Density

Select grid families from the shorter pixel dimension:

- Use a sparse family below 700 px.
- Use a standard family from 700 px to below 1400 px.
- Use a dense family at 1400 px or above.

Increase image size to add resistance/reactance and conductance/susceptance line families. Decrease image size to remove minor line families and preserve readability. Preserve explicitly supplied `resistance_values`, `reactance_values`, `conductance_values`, or `susceptance_values` instead of replacing them automatically.

## Scale-label Convention

- Render all scale text in black.
- Rotate both impedance real and imaginary scale numbers right by 90 degrees.
- Rotate both admittance real and imaginary scale numbers left by 90 degrees.
- Place impedance real-axis numbers above the horizontal axis and admittance real-axis numbers below it.
- Show imaginary-family labels only as signed values such as `+0.5` and `-0.5`, without `x` or `b` prefixes.
- Place all imaginary-family labels outside the Smith-chart boundary.
- Detect insufficient angular spacing automatically and distribute overlapping imaginary labels across additional radial layers.
- Draw a square white box with a thin gray border around each imaginary label.
- Reduce the number of labels together with the grid density on small images.

## Quick Start

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

## Task-list Interface

Use `execute()` when another Skill or automated task needs a JSON-like operation list.

```python
chart.execute([
    {"type": "impedance", "r": 1, "x": 1, "label": "A"},
    {"type": "swr", "point": "A"},
    {"type": "move", "start": "A", "distance": 0.125, "toward_generator": True, "label": "B"},
    {"type": "line", "start": "A", "end": "B", "arrow": True},
])
```

## Coordinate Conventions

- Treat impedance as normalized `z = r + jx`.
- Treat admittance as normalized `y = g + jb`.
- Convert impedance with `Gamma = (z - 1) / (z + 1)`.
- Convert admittance through `z = 1 / y`.
- Interpret positive wavelength distance toward the generator as clockwise rotation on the reflection-coefficient plane.
- Rotate by `4*pi*l/lambda`, because reflection-coefficient phase changes by twice the electrical line length.

## Resources

- Read `references/api_reference.md` for complete sizing, density, method, and operation details.
- Run `examples/teaching_demo.py` for a dense 1800 x 1800 teaching example.
- Run the test suite before distributing changes.
