from pathlib import Path
from smith_chart_engine import SmithChart

output = Path(__file__).resolve().parent / "smith_chart_teaching_demo_v6.png"
chart = SmithChart(
    show_impedance=True,
    show_admittance=False,
    width_px=1800,
    height_px=1800,
    dpi=180,
    grid_density="auto",
    show_scale_labels=True,
    grid_linewidth=1.05,
    overlay_scale=1.55,
)
chart.execute([
    {"type": "impedance", "r": 1, "x": 1, "label": "A"},
    {"type": "swr", "point": "A"},
    {"type": "flip", "point": "A", "label": "A'"},
    {"type": "move", "start": "A", "distance": 0.125, "toward_generator": True, "label": "B"},
    {"type": "line", "start": "A", "end": "B", "arrow": True},
])
chart.save(output)
print(f"density={chart.grid_density}")
print(f"impedance_real_lines={len(chart.resistance_values)}")
print(f"impedance_reactance_levels={len(chart.reactance_values)}")
print(f"scale_labels={len(chart.ax.texts)}")
print(output)
chart.close()
