# cp1am/interactive/cp1plot.py
"""
cp1 optional functions for interactive plots and maps
"""

__version__ = "2024.11.0"

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
from IPython.display import display, Markdown
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from ..cp1am import cp_bool2pos2ind, cp_profileval, cp_profilz

def cp_ductplot(qindprof, dfin, dfcalc, dfident, CPC):
    """Plots vertical N/M profiles with duct for a given profile index"""
    mi1, _, _ = cp_bool2pos2ind(dfident, mask_ind=[qindprof])

    # Vérifie si mi1 n'est pas uniquement faux
    if not mi1.any():
        warnings.warn(f"{qindprof} is not an index of the dataframe")
        return
    dfduct = dfident.loc[mi1, :]
    zzc = dfident.loc[mi1, "Z3"].values
    z13 = dfident.loc[mi1, "Z2"].values
    zz0 = dfident.loc[mi1, "Z1"].values
    Mzc = dfident.loc[mi1, "M3"].values
    M13 = dfident.loc[mi1, "M2"].values
    Mz0 = dfident.loc[mi1, "M1"].values

    # Calcul des Nxx
    Nzc = Mzc - 0.157 * zzc
    N13 = M13 - 0.157 * z13
    Nz0 = Mz0 - 0.157 * zz0

    mi0, _, _ = cp_bool2pos2ind(dfin, mask_ind=[qindprof])
    zlmo = dfcalc.loc[mi0, "lmo"].values

    z, pz, ez, esz, thz, tkz, qz, hrz, Nz, Mz = cp_profileval(
        z=cp_profilz(nbpts=50, zmax=100), dfin=dfin, df=dfcalc, C=CPC, mask=mi0
    )

    # Create the figure
    fig = go.Figure()

    # Plot Nz and MZ vs z
    fig.add_trace(
        go.Scatter(
            x=Nz,
            y=z,
            mode="lines+markers",
            name="Nz",
            marker=dict(color="blue", symbol="circle"),
            line=dict(color="blue"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=Mz,
            y=z,
            mode="lines+markers",
            name="Mz",
            marker=dict(color="lightgreen", symbol="x"),
            line=dict(color="lightgreen"),
        )
    )

    # Plot Nzc and Mzc vs zcc in red
    fig.add_trace(
        go.Scatter(
            x=Nzc,
            y=zzc,
            mode="markers",
            name="Nzc",
            marker=dict(color="red", symbol="circle", size=10),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=Mzc,
            y=zzc,
            mode="markers",
            name="Mzc",
            marker=dict(color="red", symbol="x", size=10),
        )
    )

    # Adding h13 and lmo horizontal lines
    fig.add_hline(
        y=z13.item(),
        line=dict(color="navy", dash="dash"),
        name="H1/3",
        annotation_text="H1/3",
        annotation_position="top left",
    )
    fig.add_hline(
        y=abs(zlmo).item(),
        line=dict(color="green", dash="dash"),
        name="lmo",
        annotation_text="lmo",
        annotation_position="top left",
    )

    # Add dummy traces for h13 and lmo to include them in the legend
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="lines",
            line=dict(color="navy", dash="dash"),
            name="H1/3",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="lines",
            line=dict(color="green", dash="dash"),
            name="lmo",
        )
    )

    # Update layout
    fig.update_layout(
        title="Nz and Mz as a function of altitude z",
        xaxis_title="Refraction Indices N(z) and M(z)",
        yaxis_title="Altitude z [m] above sea level",
        legend_title="Legend",
        template="plotly_white",
    )

    # Show the plot
    fig.show()

    return


def cp_formulae():
    # LaTeX formula
    # from IPython.display import display, Markdown
    # display(Markdown(formulae['1']))
    formulae = {
        "1": {
            "formula": r"$$\phi_h = \phi_m = f(\zeta) = 1 + \frac{6\zeta}{1 + \zeta}$",
            "author": "Kondo",
            "year": 1995,
        },  # phih=phim (cas stable)
        "2": {
            "formula": r"$\psi_h = \psi_m = -6 \ln(1 + \zeta)$"
        },  # psih = psim (cas stable)
        "3": {
            "formula": r"$\text{hr}_0 = 100 \times \left(1 - (5.37 \times 10^{-4} \times S_A)\right)$"
        },
        "4": {"formula": r"$ $"},
        "5": {"formula": r"$ $"},
        "6": {"formula": r"$ $"},
        "7": {"formula": r"$ $"},
        "8": {"formula": r"$ $"},
        "9": {
            "formula": r"$\text{BRN} = \text{Ri}_b = \frac{g \cdot z_1 \cdot (\theta_{v1} - \theta_{v0})}{\left(\frac{\theta_{v1} + \theta_{v0}}{2}\right) \cdot v_1^2}$"
        },
    }
    return formulae


def cp_displayformulae(formulae, qformulae=None, details=False):
    # If qformulae is None, display all formulae
    if qformulae is None:
        qformulae = formulae.keys()

    # Display each formula with its corresponding number, author, and year on a single line
    for num in qformulae:
        if num in formulae:
            details_dict = formulae[num]
            line = f'[{num}]\t{details_dict["formula"]}'
            if details:
                if "author" in details_dict and details_dict["author"]:
                    line += f'\t[{details_dict["author"]}'
                    if "year" in details_dict and details_dict["year"]:
                        line += f'-{details_dict["year"]}'
                    line += "]"
            display(Markdown(line))



