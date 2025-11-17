# pepe_plotly_theme.py
from __future__ import annotations
from typing import Iterable, Optional, Sequence
import plotly.graph_objects as go
import plotly.io as pio


# Standard journal column widths (in inches)
SINGLE_COLUMN = 3.3  # inches (max 3.5 for single column)
DOUBLE_COLUMN = 7.0  # inches

DPI = 400  # Standard for publication
SINGLE_COLUMN_PX = int(SINGLE_COLUMN * DPI)  # 990 px
DOUBLE_COLUMN_PX = int(DOUBLE_COLUMN * DPI)  # 2100 px

# ---------- Template ----------
def register_template(
    *,
    name: str = "pepe",
    font_family: str = "CMU Sans Serif, IBM Plex Sans, Roboto, Helvetica, sans-serif",
    font_size: int = 10,
    gridcolor: str = "rgba(117, 141, 153, 0.2)",  # Light version of #758D99
    plot_bgcolor: str = "white",
    paper_bgcolor: str = "white",
    colorway: Sequence[str] = (
        "#0C5DA5", "#00B945", "#FF9500", "#FF2C00", "#845B97",
        "#474747", "#9e9e9e", "#9A607F",
    ),
) -> str:
    tmpl = go.layout.Template(
        layout=go.Layout(
            font=dict(family=font_family, size=font_size, color="#758D99"),
            colorway=list(colorway),
            plot_bgcolor=plot_bgcolor,
            paper_bgcolor=paper_bgcolor,
            margin=dict(l=60, r=10, t=40, b=50),  # Tighter margins
            # height=400, 
            width=SINGLE_COLUMN_PX,  # Default to single column
            legend=dict(
                x=0.01, y=0.99, 
                bgcolor="rgba(0,0,0,0)",  # Transparent background
                bordercolor="rgba(0,0,0,0)",  # No border (frameon=False)
                borderwidth=0,
                font=dict(size=10)
            ),
            xaxis=dict(
                showgrid=False,  # No grid by default
                gridcolor=gridcolor, 
                zeroline=False,
                showline=True, 
                linecolor="#758D99", 
                linewidth=0.5,
                mirror=False,  # Only bottom spine
                ticks="inside", 
                tickcolor="#758D99",
                tickwidth=0.5,
                ticklen=3,
                automargin=True, 
                title_standoff=10, 
                exponentformat="power",
                tickfont=dict(size=10, color="#758D99"),
                title=dict(font=dict(size=11, color="#758D99")),
            ),
            yaxis=dict(
                showgrid=False,  # No grid by default
                gridcolor=gridcolor, 
                zeroline=False,
                showline=True, 
                linecolor="#758D99", 
                linewidth=0.5,
                mirror=False,  # Only left spine
                ticks="inside", 
                tickcolor="#758D99",
                tickwidth=0.5,
                ticklen=3,
                automargin=True, 
                title_standoff=10, 
                exponentformat="power",
                tickfont=dict(size=10, color="#758D99"),
                title=dict(font=dict(size=11, color="#758D99")),
            ),
        )
    )
    # Default trace tweaks
    tmpl.data.scatter = [go.Scatter(
        marker=dict(size=3, line=dict(color="white", width=0.5)),
        line=dict(width=1),
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
    format: str = "pdf",
    filename: str = "plot",
    scale: int = 1,
):
    """
    Set global Plotly defaults for all .show() calls.
    In particular, makes the modebar download button export PDF by default.
    Scale is set to 1 since we're already sizing at target DPI.
    """
    pio.renderers.default = pio.renderers.default  # ensure current renderer stays
    pio.renderers[pio.renderers.default].config = {
        "toImageButtonOptions": {
            "format": format,
            "filename": filename,
            "scale": scale,
        }
    }
