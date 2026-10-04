"""Reusable Smith chart renderer based on Python and Matplotlib."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
import cmath
import math

import matplotlib.pyplot as plt
import numpy as np


@dataclass
class SmithPoint:
    name: str
    gamma: complex
    kind: str = "gamma"


class SmithChart:
    """Draw Smith-chart grids and reusable teaching annotations."""

    GRID_PRESETS = {
        "sparse": {
            "real": (0, 0.5, 1, 2, 5),
            "imag": (0.5, 1, 2, 5),
        },
        "standard": {
            "real": (0, 0.2, 0.5, 1, 2, 5),
            "imag": (0.2, 0.5, 1, 2, 5),
        },
        "dense": {
            "real": (0, 0.1, 0.2, 0.3, 0.5, 0.7, 1, 1.5, 2, 3, 5, 10),
            "imag": (0.1, 0.2, 0.3, 0.5, 0.7, 1, 1.5, 2, 3, 5, 10),
        },
    }

    def __init__(
        self,
        show_impedance: bool = True,
        show_admittance: bool = False,
        resistance_values: Iterable[float] | None = None,
        reactance_values: Iterable[float] | None = None,
        conductance_values: Iterable[float] | None = None,
        susceptance_values: Iterable[float] | None = None,
        figsize: tuple[float, float] | None = (8, 8),
        width_px: int | None = None,
        height_px: int | None = None,
        dpi: int = 160,
        grid_density: str = "auto",
        show_scale_labels: bool = True,
        grid_linewidth: float = 0.9,
        label_fontsize: float | None = None,
        overlay_scale: float = 1.35,
    ) -> None:
        self.show_impedance = show_impedance
        self.show_admittance = show_admittance
        self.dpi = dpi
        self.figsize = self._resolve_figsize(figsize, width_px, height_px, dpi)
        self.width_px = int(round(self.figsize[0] * dpi))
        self.height_px = int(round(self.figsize[1] * dpi))
        self.grid_density = self._resolve_density(grid_density)
        preset = self.GRID_PRESETS[self.grid_density]

        self.resistance_values = tuple(resistance_values) if resistance_values is not None else preset["real"]
        self.reactance_values = tuple(reactance_values) if reactance_values is not None else preset["imag"]
        self.conductance_values = tuple(conductance_values) if conductance_values is not None else preset["real"]
        self.susceptance_values = tuple(susceptance_values) if susceptance_values is not None else preset["imag"]
        self.show_scale_labels = show_scale_labels
        self.grid_linewidth = grid_linewidth
        self.label_fontsize = label_fontsize or self._automatic_label_fontsize()
        if overlay_scale <= 0:
            raise ValueError("overlay_scale must be positive")
        self.overlay_scale = float(overlay_scale)

        self.fig, self.ax = plt.subplots(figsize=self.figsize, dpi=dpi)
        self.points: dict[str, SmithPoint] = {}
        self._configure_axes()
        self.draw_grid()

    @staticmethod
    def _resolve_figsize(
        figsize: tuple[float, float] | None,
        width_px: int | None,
        height_px: int | None,
        dpi: int,
    ) -> tuple[float, float]:
        if dpi <= 0:
            raise ValueError("dpi must be positive")
        if width_px is not None or height_px is not None:
            width = width_px or height_px
            height = height_px or width_px
            if width is None or height is None or width <= 0 or height <= 0:
                raise ValueError("width_px and height_px must be positive")
            return width / dpi, height / dpi
        if figsize is None or figsize[0] <= 0 or figsize[1] <= 0:
            raise ValueError("figsize must contain positive values")
        return figsize

    def _resolve_density(self, grid_density: str) -> str:
        if grid_density not in {"auto", "sparse", "standard", "dense"}:
            raise ValueError("grid_density must be auto, sparse, standard, or dense")
        if grid_density != "auto":
            return grid_density
        shortest_side = min(self.width_px, self.height_px)
        if shortest_side < 700:
            return "sparse"
        if shortest_side < 1400:
            return "standard"
        return "dense"

    def _automatic_label_fontsize(self) -> float:
        shortest_side = min(self.width_px, self.height_px)
        if shortest_side < 700:
            return 7.0
        if shortest_side < 1400:
            return 8.5
        return 10.0

    @staticmethod
    def z_to_gamma(z: complex) -> complex:
        if abs(z + 1) < 1e-14:
            raise ValueError("z = -1 makes the reflection coefficient undefined")
        return (z - 1) / (z + 1)

    @staticmethod
    def y_to_gamma(y: complex) -> complex:
        if abs(y) < 1e-14:
            return complex(1, 0)
        return SmithChart.z_to_gamma(1 / y)

    def _configure_axes(self) -> None:
        self.ax.set_aspect("equal", adjustable="box")
        self.ax.set_xlim(-1.32, 1.32)
        self.ax.set_ylim(-1.32, 1.32)
        self.ax.axis("off")

    def draw_grid(self) -> "SmithChart":
        self.ax.add_patch(
            plt.Circle((0, 0), 1, fill=False, color="#111111", lw=max(1.8, self.grid_linewidth * 1.9))
        )
        self.ax.plot([-1, 1], [0, 0], color="#111111", lw=max(1.15, self.grid_linewidth * 1.25))

        if self.show_impedance:
            self._draw_family(
                self.resistance_values,
                self.reactance_values,
                transform=self.z_to_gamma,
                color="#4A4A4A",
                linestyle="-",
                alpha=0.78,
                linewidth=self.grid_linewidth,
            )
            if self.show_scale_labels:
                self._draw_real_scale_labels(
                    self.resistance_values,
                    transform=self.z_to_gamma,
                    color="#000000",
                    rotation=90,
                    vertical_offset=0.055,
                )
                self._draw_imag_scale_labels(
                    self.reactance_values,
                    transform=self.z_to_gamma,
                    color="#000000",
                    family="impedance",
                )

        if self.show_admittance:
            self._draw_family(
                self.conductance_values,
                self.susceptance_values,
                transform=self.y_to_gamma,
                color="#2474B5",
                linestyle=(0, (5, 3)),
                alpha=0.80,
                linewidth=self.grid_linewidth,
            )
            if self.show_scale_labels:
                self._draw_real_scale_labels(
                    self.conductance_values,
                    transform=self.y_to_gamma,
                    color="#000000",
                    rotation=-90,
                    vertical_offset=-0.055,
                )
                self._draw_imag_scale_labels(
                    self.susceptance_values,
                    transform=self.y_to_gamma,
                    color="#000000",
                    family="admittance",
                )
        return self

    def _draw_family(
        self,
        real_values,
        imag_values,
        transform,
        color,
        linestyle,
        alpha,
        linewidth,
    ) -> None:
        sweep = np.linspace(-150, 150, 5000)
        for real in real_values:
            values = real + 1j * sweep
            gammas = np.array([transform(complex(value)) for value in values])
            mask = np.abs(gammas) <= 1.00001
            self.ax.plot(
                gammas.real[mask],
                gammas.imag[mask],
                color=color,
                ls=linestyle,
                lw=linewidth,
                alpha=alpha,
            )

        sweep_real = np.linspace(0, 150, 5000)
        for imag in imag_values:
            for sign in (1, -1):
                values = sweep_real + 1j * sign * imag
                gammas = np.array([transform(complex(value)) for value in values])
                mask = np.abs(gammas) <= 1.00001
                self.ax.plot(
                    gammas.real[mask],
                    gammas.imag[mask],
                    color=color,
                    ls=linestyle,
                    lw=linewidth,
                    alpha=alpha,
                )

    def _draw_real_scale_labels(
        self,
        values,
        transform,
        color: str,
        rotation: float,
        vertical_offset: float,
    ) -> None:
        for value in values:
            gamma = transform(complex(value, 0))
            self.ax.text(
                gamma.real,
                vertical_offset,
                f"{value:g}",
                fontsize=self.label_fontsize,
                color=color,
                rotation=rotation,
                rotation_mode="anchor",
                ha="center",
                va="center",
                zorder=6,
                clip_on=False,
            )

    def _draw_imag_scale_labels(
        self,
        values,
        transform,
        color: str,
        family: str,
    ) -> None:
        """Place signed imaginary-family labels outside the Smith-chart boundary."""
        rotation = 90 if family == "impedance" else -90
        base_radius = 1.075 if family == "impedance" else 1.235
        minimum_angle = {
            "sparse": math.radians(11.0),
            "standard": math.radians(8.5),
            "dense": math.radians(6.5),
        }[self.grid_density]
        radial_step = {
            "sparse": 0.075,
            "standard": 0.068,
            "dense": 0.060,
        }[self.grid_density]
        occupied_angles: list[list[float]] = []

        candidates = []
        for value in values:
            for sign in (1, -1):
                signed_value = sign * value
                gamma = transform(complex(0.0, signed_value))
                candidates.append((cmath.phase(gamma), signed_value))

        for angle, signed_value in sorted(candidates, key=lambda item: item[0]):
            layer = 0
            while True:
                if layer == len(occupied_angles):
                    occupied_angles.append([])
                if all(abs(cmath.phase(cmath.exp(1j * (angle - other)))) >= minimum_angle for other in occupied_angles[layer]):
                    occupied_angles[layer].append(angle)
                    break
                layer += 1

            radius = base_radius + layer * radial_step
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            prefix = "+" if signed_value > 0 else "-"
            self.ax.text(
                x,
                y,
                f"{prefix}{abs(signed_value):g}",
                fontsize=max(6.5, self.label_fontsize - 0.8),
                color=color,
                rotation=rotation,
                rotation_mode="anchor",
                ha="center",
                va="center",
                zorder=7,
                clip_on=False,
                bbox={"boxstyle": "square,pad=0.28", "facecolor": "white", "edgecolor": "#555555", "linewidth": 0.65, "alpha": 0.92},
            )

    def add_gamma(self, gamma: complex, label: str | None = None, **style: Any) -> str:
        gamma = complex(gamma)
        if abs(gamma) > 1.000001:
            raise ValueError("Passive Smith-chart points require |gamma| <= 1")
        name = label or f"P{len(self.points) + 1}"
        defaults = {"s": 54 * self.overlay_scale, "color": "#C62828", "zorder": 7}
        defaults.update(style)
        self.ax.scatter([gamma.real], [gamma.imag], **defaults)
        self.points[name] = SmithPoint(name=name, gamma=gamma)
        if label:
            self.add_label(name, label)
        return name

    def add_impedance(self, r: float, x: float, label: str | None = None, **style: Any) -> str:
        name = self.add_gamma(self.z_to_gamma(complex(r, x)), label, **style)
        self.points[name].kind = "impedance"
        return name

    def add_admittance(self, g: float, b: float, label: str | None = None, **style: Any) -> str:
        name = self.add_gamma(self.y_to_gamma(complex(g, b)), label, **style)
        self.points[name].kind = "admittance"
        return name

    def add_label(self, point: str | complex, text: str, dx: float = 0.035, dy: float = 0.035, **style: Any) -> None:
        gamma = self._resolve(point)
        defaults = {"fontsize": max(9, self.label_fontsize) * self.overlay_scale, "color": "#111111", "fontweight": "semibold", "zorder": 8}
        defaults.update(style)
        self.ax.text(gamma.real + dx, gamma.imag + dy, text, **defaults)

    def add_line(self, start: str | complex, end: str | complex, arrow: bool = False, **style: Any) -> None:
        first, second = self._resolve(start), self._resolve(end)
        defaults = {"color": "#D35400", "lw": 1.9 * self.overlay_scale, "zorder": 6}
        defaults.update(style)
        if arrow:
            self.ax.annotate(
                "",
                xy=(second.real, second.imag),
                xytext=(first.real, first.imag),
                arrowprops={"arrowstyle": "-|>", "mutation_scale": 13 * self.overlay_scale, **defaults},
            )
        else:
            self.ax.plot([first.real, second.real], [first.imag, second.imag], **defaults)

    def draw_swr_circle(self, point: str | complex, **style: Any) -> None:
        radius = abs(self._resolve(point))
        defaults = {"fill": False, "color": "#8E44AD", "lw": 1.65 * self.overlay_scale, "ls": "-."}
        defaults.update(style)
        self.ax.add_patch(plt.Circle((0, 0), radius, **defaults))

    def flip_to_admittance(self, point: str, label: str | None = None, connect: bool = True) -> str:
        source = self._resolve(point)
        target = -source
        new_name = label or f"{point}'"
        self.add_gamma(target, new_name, color="#2474B5", marker="s")
        self.points[new_name].kind = "admittance"
        if connect:
            self.add_line(point, new_name, color="#2474B5", ls="--", lw=1.35 * self.overlay_scale)
        return new_name

    def move_wavelength(
        self,
        start: str,
        distance: float,
        toward_generator: bool = True,
        label: str | None = None,
        draw_arc: bool = True,
    ) -> str:
        gamma = self._resolve(start)
        direction = -1 if toward_generator else 1
        delta = direction * 4 * math.pi * distance
        target = gamma * cmath.exp(1j * delta)
        name = label or f"{start}_{'G' if toward_generator else 'L'}_{distance:g}lambda"
        if draw_arc and abs(gamma) > 0:
            theta0 = cmath.phase(gamma)
            theta = np.linspace(theta0, theta0 + delta, max(40, int(abs(delta) * 90)))
            arc = abs(gamma) * np.exp(1j * theta)
            self.ax.plot(arc.real, arc.imag, color="#009688", lw=2.0 * self.overlay_scale, zorder=6)
            self.ax.annotate(
                "",
                xy=(arc.real[-1], arc.imag[-1]),
                xytext=(arc.real[-3], arc.imag[-3]),
                arrowprops={"arrowstyle": "-|>", "mutation_scale": 12 * self.overlay_scale, "color": "#009688", "lw": 2.0 * self.overlay_scale},
            )
        self.add_gamma(target, name, color="#009688")
        return name

    def execute(self, operations: list[dict[str, Any]]) -> "SmithChart":
        dispatch = {
            "impedance": lambda op: self.add_impedance(op["r"], op["x"], op.get("label"), **op.get("style", {})),
            "admittance": lambda op: self.add_admittance(op["g"], op["b"], op.get("label"), **op.get("style", {})),
            "gamma": lambda op: self.add_gamma(complex(op["gamma"]), op.get("label"), **op.get("style", {})),
            "label": lambda op: self.add_label(op["point"], op["text"], **op.get("style", {})),
            "line": lambda op: self.add_line(op["start"], op["end"], op.get("arrow", False), **op.get("style", {})),
            "swr": lambda op: self.draw_swr_circle(op["point"], **op.get("style", {})),
            "flip": lambda op: self.flip_to_admittance(op["point"], op.get("label"), op.get("connect", True)),
            "move": lambda op: self.move_wavelength(op["start"], op["distance"], op.get("toward_generator", True), op.get("label"), op.get("draw_arc", True)),
        }
        for operation in operations:
            kind = operation.get("type")
            if kind not in dispatch:
                raise ValueError(f"Unsupported operation type: {kind}")
            dispatch[kind](operation)
        return self

    def _resolve(self, point: str | complex) -> complex:
        if isinstance(point, str):
            if point not in self.points:
                raise KeyError(f"Unknown point: {point}")
            return self.points[point].gamma
        return complex(point)

    def save(self, path: str | Path, transparent: bool = False, tight: bool = True) -> Path:
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        if output.suffix.lower() not in {".png", ".svg", ".pdf"}:
            raise ValueError("Output format must be PNG, SVG, or PDF")
        self.fig.savefig(output, transparent=transparent, bbox_inches="tight" if tight else None)
        return output

    def close(self) -> None:
        plt.close(self.fig)
