# Smith Chart Engine

A reusable Python/Matplotlib Smith-chart engine designed for RF communication circuit teaching, PPT figures, LearningTong resources, exercises, and other automated Skills.

## Features

- Solid impedance grid
- Optional dashed admittance grid
- Normalized impedance, admittance, and reflection-coefficient points
- Labels, line segments, and arrows
- Constant-VSWR circles
- 180-degree impedance/admittance rotation
- Wavelength movement along a constant-reflection-magnitude circle
- Task-list `execute()` interface for other Skills
- PNG, SVG, and PDF output

## Install

```bash
python -m pip install -e .
```

## Example

```python
from smith_chart_engine import SmithChart

chart = SmithChart(show_impedance=True, show_admittance=True)
chart.add_impedance(r=1, x=1, label="A")
chart.draw_swr_circle("A")
chart.flip_to_admittance("A", label="A'")
chart.move_wavelength("A", 0.125, toward_generator=True, label="B")
chart.save("smith_chart.svg")
chart.close()
```

Run the complete example:

```bash
python examples/teaching_demo.py
```

Run tests:

```bash
pytest
```

## GitHub collaboration

Fork the repository, create a feature branch, add tests for changed behavior, and submit a pull request. Suitable future additions include single-stub matching, double-stub matching, matching-path search, outer wavelength scales, and animation.

## License

MIT License.
