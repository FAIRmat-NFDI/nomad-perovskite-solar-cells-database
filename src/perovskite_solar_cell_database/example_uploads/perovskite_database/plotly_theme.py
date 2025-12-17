# pepe_plotly_theme.py
from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Optional

import plotly.graph_objects as go
import plotly.io as pio


# ---------- Template ----------
def register_template(  # noqa: PLR0913
    *,
    name: str = "pepe",
    font_family: str = "Arial",
    font_size: int = 18,
    gridcolor: str = "lightgray",
    plot_bgcolor: str = "rgba(0,0,0,0)",
    paper_bgcolor: str = "rgba(0,0,0,0)",
    colorway: Sequence[str] = (
        "#1f77b4", "#ff0e5a", "#e9c821", "#86d9ea", "#ff9408",
        "#ba78d6", "#4cd8a5", "#7f7f7f", "#bcbd22", "#17becf",
    ),
) -> str:
    tmpl = go.layout.Template(
        layout=go.Layout(
            font=dict(family=font_family, size=font_size),
            colorway=list(colorway),
            plot_bgcolor=plot_bgcolor,
            paper_bgcolor=paper_bgcolor,
            margin=dict(l=50, r=50, t=60, b=60),
            # height=400, 
            width=700,
            legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.6)"),
            xaxis=dict(
                showgrid=True, gridcolor=gridcolor, zeroline=False,
                showline=True, linecolor="black", linewidth=1,
                mirror=True, ticks="inside", tickcolor="black",
                automargin=True, title_standoff=10, exponentformat="power",
            ),
            yaxis=dict(
                showgrid=True, gridcolor=gridcolor, zeroline=False,
                showline=True, linecolor="black", linewidth=1,
                mirror=True, ticks="inside", tickcolor="black",
                automargin=True, title_standoff=10, exponentformat="power",
            ),
        )
    )
    # Default trace tweaks
    tmpl.data.scatter = [go.Scatter(
        marker=dict(line=dict(color="black", width=1)),
        line=dict(width=2),
    )]
    pio.templates[name] = tmpl
    pio.templates.default = name
    return name


def set_defaults(
    format: str = "svg",
    filename: str = "plot",
    scale: int = 1,
):
    """
    Set global Plotly defaults for all .show() calls.
    In particular, makes the modebar download button export SVG.
    """
    pio.renderers.default = pio.renderers.default  # ensure current renderer stays
    pio.renderers[pio.renderers.default].config = {
        "toImageButtonOptions": {
            "format": format,
            "filename": filename,
            "scale": scale,
        }
    }
