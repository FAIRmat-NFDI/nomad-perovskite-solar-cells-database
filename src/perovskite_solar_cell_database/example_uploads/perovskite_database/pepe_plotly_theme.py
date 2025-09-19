# pepe_plotly_theme.py
from __future__ import annotations
from typing import Iterable, Optional, Sequence
import plotly.graph_objects as go
import plotly.io as pio

# ---------- Template ----------
def register_template(
    *,
    name: str = "pepe",
    font_family: str = "Arial",
    font_size: int = 18,
    gridcolor: str = "lightgray",
    plot_bgcolor: str = "white",
    paper_bgcolor: str = "white",
    colorway: Sequence[str] = (
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
        "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    ),
) -> str:
    tmpl = go.layout.Template(
        layout=go.Layout(
            font=dict(family=font_family, size=font_size),
            colorway=list(colorway),
            plot_bgcolor=plot_bgcolor,
            paper_bgcolor=paper_bgcolor,
            margin=dict(l=50, r=50, t=60, b=60),
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

# ---------- Helper: generic scatter ----------
def scatter_plot(
    x: Iterable, y: Iterable, *,
    name: str = "Data",
    text: Optional[Sequence[str]] = None,
    x_title: Optional[str] = None,
    y_title: Optional[str] = None,
    x_log: bool = False,
    y_log: bool = False,
    x_range: Optional[Sequence[float]] = None,
    y_range: Optional[Sequence[float]] = None,
    width: int = 800,
    height: int = 500,
    size: int = 10,
    opacity: float = 0.9,
    color: Optional[str] = None,
    template: Optional[str] = "pepe",   # <- ensure our template is used
    x_nticks: Optional[int] = 5,
    y_nticks: Optional[int] = 5,
    showlegend: bool = True,
) -> go.Figure:
    fig = go.Figure()
    fig.update_layout(width=width, height=height, template=template, showlegend=showlegend)

    fig.add_trace(go.Scatter(
        x=list(x), y=list(y),
        mode="markers", name=name,
        marker=dict(size=size, color=color, line=dict(color="black", width=1)),
        opacity=opacity, text=list(text) if text is not None else None,
    ))

    # Force axis styling (even if another template was active earlier)
    fig.update_xaxes(
        title=x_title, nticks=x_nticks,
        showline=True, linecolor="black", linewidth=1,
        mirror=True, ticks="inside", tickcolor="black",
        showgrid=True, gridcolor="lightgray", zeroline=False,
    )
    fig.update_yaxes(
        title=y_title, nticks=y_nticks,
        showline=True, linecolor="black", linewidth=1,
        mirror=True, ticks="inside", tickcolor="black",
        showgrid=True, gridcolor="lightgray", zeroline=False,
    )

    if x_log: fig.update_xaxes(type="log")
    if y_log: fig.update_yaxes(type="log")
    if x_range is not None: fig.update_xaxes(range=list(x_range))
    if y_range is not None: fig.update_yaxes(range=list(y_range))

    return fig

import plotly.io as pio


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