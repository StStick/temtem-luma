import math

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import streamlit as st

st.set_page_config(page_title="Probabilité de Luma", layout="wide")
st.title("Probabilité de Luma")


def format_time(seconds):
    if seconds < 60:
        return f"{seconds:.1f} s"
    elif seconds < 3600:
        m = int(seconds // 60)
        s = round(seconds % 60)
        return f"{m}min {s}s" if s else f"{m}min"
    else:
        h = int(seconds // 3600)
        m = round((seconds % 3600) / 60)
        return f"{h}h {m}min" if m else f"{h}h"


col_params, col_chart = st.columns([1, 2.5])

with col_params:
    st.subheader("Paramètres")

    n = st.number_input(
        "n  (probabilité de base = 1/n)", min_value=2, value=2000, step=1
    )

    freq = st.radio(
        "Animations",
        options=["Sans  —  10 / min", "Avec  —  6 / min"],
        index=0,
        horizontal=True,
    )
    interval_s = 60 / 10 if freq.startswith("S") else 60 / 6

    taux = st.slider(
        "Taux d'apparition (%)", min_value=1, max_value=100, value=100, step=1
    )

    mult = st.number_input(
        "Multiplicateur  × (1/n)", min_value=0.0, value=1.0, step=0.5, format="%.2f"
    )

    st.divider()
    st.subheader("Résultats")

    p = min(1.0, mult / n * (taux / 100))

    if p <= 0:
        st.warning("Probabilité nulle, vérifie les paramètres.")
        st.stop()

    e_trials = 1 / p
    e_time_s = e_trials * interval_s

    m1, m2, m3 = st.columns(3)
    m1.metric("Proba / essai", f"{p * 100:.2f}%")
    m2.metric("Espérance (essais)", str(round(e_trials)))
    m3.metric("Espérance (temps)", format_time(e_time_s))

with col_chart:
    st.subheader("Probabilité cumulée d'avoir eu un luma au bout de x secondes")

    max_k = math.ceil(math.log(0.001) / math.log(1 - p))
    ks = np.arange(1, max_k + 1)
    times_s = ks * interval_s
    cum_p = (1 - (1 - p) ** ks) * 100

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(times_s, cum_p, color="#378ADD", linewidth=2)
    ax.fill_between(times_s, cum_p, alpha=0.08, color="#378ADD")

    ref_levels = [(0.50, "#E24B4A"), (0.90, "#BA7517"), (0.99, "#3B6D11")]
    for ref, color in ref_levels:
        k_ref = math.ceil(math.log(1 - ref) / math.log(1 - p))
        t_ref = k_ref * interval_s
        ax.axhline(ref * 100, linestyle="--", linewidth=1.2, color=color)
        ax.annotate(
            f"{int(ref * 100)}% → {format_time(t_ref)}",
            xy=(times_s[-1], ref * 100),
            xytext=(-6, 6),
            textcoords="offset points",
            ha="right",
            va="bottom",
            fontsize=9,
            color=color,
        )

    ax.set_xlabel("Temps (secondes)", fontsize=11)
    ax.set_ylabel("Probabilité cumulée (%)", fontsize=11)
    ax.set_ylim(0, 102)
    ax.set_xlim(0, times_s[-1])
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.grid(True, alpha=0.2)
    fig.tight_layout()

    st.pyplot(fig)
