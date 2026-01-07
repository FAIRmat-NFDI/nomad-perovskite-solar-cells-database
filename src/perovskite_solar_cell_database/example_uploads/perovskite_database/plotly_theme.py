from __future__ import annotations
from collections.abc import Iterable, Sequence
from typing import Optional

import plotly.graph_objects as go
import plotly.io as pio


# ---------- Color Definitions (Single Source of Truth) ----------
# Default colorway for all plots
DEFAULT_COLORWAY = (
    '#1f77b4',
    '#ff0e5a',
    '#e9c821',
    '#86d9ea',
    '#ff9408',
    '#ba78d6',
    '#4cd8a5',
    '#7f7f7f',
    '#bcbd22',
    '#17becf',
)


def get_model_colors(colorway: Sequence[str] | None = None) -> dict[str, str]:
    """
    Get model color mapping from colorway.

    This is the single source of truth for model colors.
    All model colors should be obtained from this function.

    Args:
        colorway: Optional colorway sequence. If None, uses DEFAULT_COLORWAY.

    Returns:
        Dictionary mapping model display names to hex colors.
    """
    if colorway is None:
        colorway = DEFAULT_COLORWAY

    colorway_list = list(colorway)

    return {
        'GPT-5 Mini': colorway_list[0],
        'GPT-5': colorway_list[1],
        'GPT-4.1': colorway_list[2],
        'GPT-4o': colorway_list[3],
        'Claude Sonnet 4': colorway_list[4],
        'Claude Opus 4': colorway_list[5],
        'Claude Opus 4.1': colorway_list[6],
        'Consensus': colorway_list[7],
    }


# ---------- Template ----------
def register_template(  # noqa: PLR0913
    *,
    name: str = 'pepe',
    font_family: str = 'Arial',
    font_size: int = 18,
    gridcolor: str = 'lightgray',
    plot_bgcolor: str = 'rgba(0,0,0,0)',
    paper_bgcolor: str = 'rgba(0,0,0,0)',
    colorway: Sequence[str] | None = None,
) -> str:
    """
    Register a Plotly template with Nature-compatible styling.

    Args:
        name: Template name
        font_family: Font family for all text
        font_size: Base font size
        gridcolor: Grid line color
        plot_bgcolor: Plot background color
        paper_bgcolor: Paper/outer background color
        colorway: Color sequence for traces. If None, uses DEFAULT_COLORWAY.

    Returns:
        Template name
    """
    if colorway is None:
        colorway = DEFAULT_COLORWAY
    tmpl = go.layout.Template(
        layout=go.Layout(
            font=dict(family=font_family, size=font_size),
            colorway=list(colorway),
            plot_bgcolor=plot_bgcolor,
            paper_bgcolor=paper_bgcolor,
            margin=dict(l=50, r=50, t=60, b=60),
            # Set width to ~7.2 inches at 100 dpi (Nature two-column width)
            width=720,
            legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0.6)'),
            xaxis=dict(
                showgrid=True,
                gridcolor=gridcolor,
                zeroline=False,
                showline=True,
                linecolor='black',
                linewidth=1,
                mirror=True,
                ticks='inside',
                tickcolor='black',
                automargin=True,
                title_standoff=10,
                exponentformat='power',
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor=gridcolor,
                zeroline=False,
                showline=True,
                linecolor='black',
                linewidth=1,
                mirror=True,
                ticks='inside',
                tickcolor='black',
                automargin=True,
                title_standoff=10,
                exponentformat='power',
            ),
        )
    )
    # Default trace tweaks
    tmpl.data.scatter = [
        go.Scatter(
            marker=dict(line=dict(color='black', width=1)),
            line=dict(width=2),
        )
    ]
    pio.templates[name] = tmpl
    pio.templates.default = name
    return name


# Export model colors for use in notebooks
MODEL_COLORS = get_model_colors()


def set_defaults(
    format: str = 'svg',
    filename: str = 'plot',
    scale: int = 1,
):
    """
    Set global Plotly defaults for all .show() calls.
    In particular, makes the modebar download button export SVG.
    """
    pio.renderers.default = pio.renderers.default  # ensure current renderer stays
    pio.renderers[pio.renderers.default].config = {
        'toImageButtonOptions': {
            'format': format,
            'filename': filename,
            'scale': scale,
        }
    }
