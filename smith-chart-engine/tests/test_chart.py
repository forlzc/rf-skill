from pathlib import Path

from smith_chart_engine import SmithChart


def test_z_to_gamma_center():
    assert abs(SmithChart.z_to_gamma(1 + 0j)) < 1e-12


def test_admittance_is_impedance_rotation():
    y = 1 + 1j
    assert abs(SmithChart.y_to_gamma(y) + SmithChart.z_to_gamma(y)) < 1e-12


def test_move_half_wavelength_returns_same_gamma():
    chart = SmithChart()
    chart.add_impedance(1, 1, "A")
    chart.move_wavelength("A", 0.5, label="B", draw_arc=False)
    assert abs(chart.points["A"].gamma - chart.points["B"].gamma) < 1e-12
    chart.close()


def test_pixel_size_controls_figure_size():
    chart = SmithChart(width_px=1200, height_px=900, dpi=150)
    width, height = chart.fig.get_size_inches()
    assert abs(width - 8.0) < 1e-12
    assert abs(height - 6.0) < 1e-12
    chart.close()


def test_automatic_grid_density_changes_with_size():
    small = SmithChart(width_px=500, height_px=500)
    medium = SmithChart(width_px=1000, height_px=1000)
    large = SmithChart(width_px=1800, height_px=1800)
    assert small.grid_density == "sparse"
    assert medium.grid_density == "standard"
    assert large.grid_density == "dense"
    assert len(small.resistance_values) < len(medium.resistance_values)
    assert len(medium.resistance_values) < len(large.resistance_values)
    small.close()
    medium.close()
    large.close()


def test_manual_grid_values_override_automatic_density():
    values = (0, 0.25, 1, 4)
    chart = SmithChart(width_px=1800, height_px=1800, resistance_values=values)
    assert chart.grid_density == "dense"
    assert chart.resistance_values == values
    chart.close()


def test_scale_label_rotations_colors_and_offsets():
    chart = SmithChart(show_admittance=True)
    real_labels = [text for text in chart.ax.texts if text.get_text() in {"0", "0.2", "0.5", "1", "2", "5"}]
    impedance_labels = [text for text in real_labels if round(text.get_position()[1], 3) == 0.055]
    admittance_labels = [text for text in real_labels if round(text.get_position()[1], 3) == -0.055]
    assert impedance_labels and admittance_labels
    assert all(round(text.get_rotation()) == 90 for text in impedance_labels)
    assert all(round(text.get_rotation()) in {270, -90} for text in admittance_labels)
    assert all(text.get_color() in {"#000000", "#111111"} for text in chart.ax.texts)
    chart.close()


def test_imaginary_arc_labels_are_present_rotated_and_outside():
    chart = SmithChart(show_admittance=True, grid_density="standard")
    imaginary_labels = [
        text for text in chart.ax.texts
        if text.get_text().startswith(("+", "-"))
    ]
    labels = {text.get_text() for text in imaginary_labels}
    for expected in {"+0.2", "-0.2", "+1", "-1"}:
        assert expected in labels
    assert all("x" not in text.get_text() and "b" not in text.get_text() for text in imaginary_labels)
    impedance_labels = imaginary_labels[: 2 * len(chart.reactance_values)]
    admittance_labels = imaginary_labels[2 * len(chart.reactance_values) :]
    assert impedance_labels and admittance_labels
    assert all(round(text.get_rotation()) == 90 for text in impedance_labels)
    assert all(round(text.get_rotation()) in {270, -90} for text in admittance_labels)
    assert all((text.get_position()[0] ** 2 + text.get_position()[1] ** 2) ** 0.5 > 1 for text in imaginary_labels)
    assert all(text.get_bbox_patch() is not None for text in imaginary_labels)
    assert all(text.get_bbox_patch().get_edgecolor()[-1] > 0 for text in imaginary_labels)
    chart.close()


def test_dense_imaginary_labels_use_multiple_non_overlapping_layers():
    chart = SmithChart(show_admittance=True, grid_density="dense", width_px=1800, height_px=1800)
    labels = [text for text in chart.ax.texts if text.get_text().startswith(("+", "-"))]
    radii = [round((text.get_position()[0] ** 2 + text.get_position()[1] ** 2) ** 0.5, 3) for text in labels]
    assert len(set(radii)) >= 2
    impedance_count = 2 * len(chart.reactance_values)
    impedance_radii = radii[:impedance_count]
    admittance_radii = radii[impedance_count:]
    assert min(admittance_radii) - max(impedance_radii) >= 0.12
    for index, first in enumerate(labels):
        x1, y1 = first.get_position()
        for second in labels[index + 1:]:
            x2, y2 = second.get_position()
            assert ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 > 0.025
    chart.close()


def test_overlay_scale_enlarges_user_elements():
    normal = SmithChart(show_scale_labels=False, overlay_scale=1.0)
    large = SmithChart(show_scale_labels=False, overlay_scale=1.6)
    normal.add_impedance(1, 1, "A")
    large.add_impedance(1, 1, "A")
    normal.add_line("A", 0j)
    large.add_line("A", 0j)
    normal.draw_swr_circle("A")
    large.draw_swr_circle("A")
    assert large.ax.collections[-1].get_sizes()[0] > normal.ax.collections[-1].get_sizes()[0]
    assert large.ax.lines[-1].get_linewidth() > normal.ax.lines[-1].get_linewidth()
    assert large.ax.patches[-1].get_linewidth() > normal.ax.patches[-1].get_linewidth()
    assert large.ax.texts[-1].get_fontsize() > normal.ax.texts[-1].get_fontsize()
    normal.close()
    large.close()


def test_save_png(tmp_path: Path):
    chart = SmithChart(show_admittance=True, width_px=1000, height_px=1000)
    chart.add_impedance(1, 1, "A")
    output = chart.save(tmp_path / "chart.png")
    assert output.exists() and output.stat().st_size > 1000
    chart.close()
