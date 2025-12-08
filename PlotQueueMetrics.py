import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────────────────────────────────────
# 1) Set Seaborn/Matplotlib theme to a grey‐background style and enable LaTeX math
# ─────────────────────────────────────────────────────────────────────────────
sns.set_theme(
    style="darkgrid",
    rc={
        # Use a light grey figure background and a slightly darker grey axes background
        "figure.facecolor": "#FFFFFF",
        "axes.facecolor":   "#c0c0c0",
        "axes.edgecolor":   "white",
        "axes.labelcolor":  "black",
        "xtick.color":      "black",
        "ytick.color":      "black",
        "text.usetex":      False,       # We don't need full LaTeX, but mathtext will handle subscripts
        "font.family":      "serif",     # Optional: choose a serif font for nicer math rendering
        "mathtext.fontset": "dejavuserif"
    }
)

# Ensure output directory exists
os.makedirs(".", exist_ok=True)


# ─────────────────────────────────────────────────────────────────────────────
# 2) Prepare the “corrected” queue‐size data (no infinities), kept intact
# ─────────────────────────────────────────────────────────────────────────────
queue_stats = [
    # λ = 2
    {"N": 2**10, "lambda": 2, "q1_mean": 0.0838,   "q1_max": 9,    "q1_std": 0.4567,  "q2_mean": 0.091,   "q2_max": 7,   "q2_std": 0.4969},
    {"N": 2**12, "lambda": 2, "q1_mean": 2.9479,   "q1_max": 49,   "q1_std": 5.7177,  "q2_mean": 2.5298,  "q2_max": 46,  "q2_std": 5.0784},
    {"N": 2**14, "lambda": 2, "q1_mean": 2074.335, "q1_max": 4306, "q1_std": 1257.4831,"q2_mean": 2120.8615,"q2_max":4506,"q2_std":1228.0157},
    # λ = 4
    {"N": 2**10, "lambda": 4, "q1_mean": 0.2043,   "q1_max": 11,   "q1_std": 0.7569,  "q2_mean": 0.1868,  "q2_max": 9,   "q2_std": 0.7344},
    {"N": 2**12, "lambda": 4, "q1_mean": 533.9378, "q1_max": 1079,"q1_std": 287.1645,"q2_mean": 529.1269,"q2_max":965,"q2_std":268.6873},
    {"N": 2**14, "lambda": 4, "q1_mean": 3036.6731,"q1_max": 6269,"q1_std": 1798.1319,"q2_mean": 3052.7743,"q2_max":6153,"q2_std":1701.4278},
    # λ = 8
    {"N": 2**10, "lambda": 8, "q1_mean": 0.0994,   "q1_max": 9,    "q1_std": 0.5385,  "q2_mean": 0.0513,  "q2_max": 7,   "q2_std": 0.3653},
    {"N": 2**12, "lambda": 8, "q1_mean": 12.9341,  "q1_max": 69,   "q1_std": 13.5799, "q2_mean": 5.7663,  "q2_max": 42,  "q2_std": 7.0196},
    {"N": 2**14, "lambda": 8, "q1_mean": 3742.9461,"q1_max": 7482,"q1_std": 2109.5577,"q2_mean": 1840.0973,"q2_max":3784,"q2_std":1033.0671},
]

df_queue = pd.DataFrame(queue_stats)
# Map 1024→ "$2^{10}$", 4096→ "$2^{12}$", 16384→ "$2^{14}$"
power_labels = {
    2**10: r"$2^{10}$",
    2**12: r"$2^{12}$",
    2**14: r"$2^{14}$"
}
df_queue["N_label"] = df_queue["N"].map(power_labels)


# ─────────────────────────────────────────────────────────────────────────────
# 3) Prepare the “corrected” latency data (in ms), also with λ = 8 intact.
# ─────────────────────────────────────────────────────────────────────────────
latency_stats = [
    # λ = 2
    {
        "N": 2**10,  "lambda": 2,
        "q1_mean":   70.0845211,  "q1_median": 53.189,   "q1_75pct": 87.888,   "q1_max": 383.973,  "q1_std":  48.928405,
        "q2_mean":   72.5836585,  "q2_median": 54.367,   "q2_75pct": 94.623,   "q2_max": 379.732,  "q2_std":  51.241789,
    },
    {
        "N": 2**12,  "lambda": 2,
        "q1_mean":   1066.285633, "q1_median":713.855,  "q1_75pct":1624.165, "q1_max":4928.233, "q1_std":  938.359679,
        "q2_mean":   966.5093875, "q2_median":624.626,  "q2_75pct":1515.412, "q2_max":4620.687, "q2_std":  899.089605,
    },
    {
        "N": 2**14,  "lambda": 2,
        "q1_mean":   429271.122,  "q1_median":432158.371,"q1_75pct":633400.761, "q1_max":838071.100, "q1_std": 244281.6842,
        "q2_mean":   411753.2814, "q2_median":408826.507,"q2_75pct":575795.115, "q2_max":838685.951, "q2_std": 219765.8365,
    },
    # λ = 4
    {
        "N": 2**10, "lambda": 4,
        "q1_mean":   77.9343784,  "q1_median":56.683,   "q1_75pct":100.080,  "q1_max":425.463,  "q1_std":  58.1693483,
        "q2_mean":   73.5078555,  "q2_median":53.476,   "q2_75pct": 95.086,  "q2_max":396.559,  "q2_std":  56.4927798,
    },
    {
        "N": 2**12, "lambda": 4,
        "q1_mean":   274480.1515, "q1_median":279514.819,"q1_75pct":428358.440, "q1_max":536960.003,"q1_std": 162548.2787,
        "q2_mean":   280350.1975, "q2_median":265798.858,"q2_75pct": 90912.669, "q2_max":537579.324,"q2_std": 34324.65259,
    },
    {
        "N": 2**14, "lambda": 4,
        "q1_mean":   274480.1515, "q1_median":279514.819,"q1_75pct":428358.440, "q1_max":536960.003,"q1_std": 162548.2787,
        "q2_mean":   280350.1975, "q2_median":265798.858,"q2_75pct":416929.311, "q2_max":537579.324,"q2_std": 138150.3112,
    },
    # λ = 8
    {
        "N": 2**10,  "lambda": 8,
        "q1_mean":   58.1316867,  "q1_median":37.79,   "q1_75pct": 74.645, "q1_max":386.036,  "q1_std":  44.2091043,
        "q2_mean":   59.2888295,  "q2_median":38.09,   "q2_75pct": 77.146, "q2_max":427.311,  "q2_std":  47.5759819,
    },
    {
        "N": 2**12,  "lambda": 8,
        "q1_mean":   1992.522032, "q1_median":1840.946,"q1_75pct":2920.602,"q1_max":6426.305,  "q1_std": 1435.452999,
        "q2_mean":   1879.010596, "q2_median":1644.536,"q2_75pct":2789.733,"q2_max":6144.572,  "q2_std": 1431.167321,
    },
    {
        "N": 2**14,  "lambda": 8,
        "q1_mean":   354416.754,  "q1_median":364107.726,"q1_75pct":524149.095,"q1_max":669616.370, "q1_std": 193531.4049,
        "q2_mean":   326499.4408, "q2_median":328795.892,"q2_75pct":482676.386,"q2_max":668060.092, "q2_std": 185847.8914,
    },
]

df_latency = pd.DataFrame(latency_stats)
df_queue["N_label"]   = df_queue["N"].map(power_labels)
df_latency["N_label"] = df_latency["N"].map(power_labels)

# Convert latency from milliseconds → seconds
for col in [
    "q1_mean","q1_median","q1_75pct","q1_max","q1_std",
    "q2_mean","q2_median","q2_75pct","q2_max","q2_std"
]:
    df_latency[col] = df_latency[col] / 1000.0


# ─────────────────────────────────────────────────────────────────────────────
# 4a) Plot queue‐size metrics (mean, max, std)
#     For λ=2 and λ=4, title = "(λ = 2)" or "(λ = 4)".
#     For λ=8, title = "(λ₁ = 4, λ₂ = 2)" and filename "…_lambda_4_2.svg".
# ─────────────────────────────────────────────────────────────────────────────
def plot_queue_metric(metric_key, ylabel, filename_prefix):
    palette = sns.color_palette("deep", 2)  # index 0 = Queue1, index 1 = Queue2
    for lam in [2, 4, 8]:
        subset = df_queue[df_queue["lambda"] == lam]
        q1 = subset[f"q1_{metric_key}"]
        q2 = subset[f"q2_{metric_key}"]

        fig, ax = plt.subplots(figsize=(6, 4))
        idx = np.arange(len(subset))
        w = 0.35

        ax.bar(idx,          q1, width=w, color=palette[0], edgecolor="black", label="Client 1")
        ax.bar(idx + w,      q2, width=w, color=palette[1], edgecolor="black", label="Client 2")

        ax.set_xticks(idx + w / 2)
        ax.set_xticklabels(subset["N_label"], fontsize=12)
        ax.set_xlabel(r"Number of Pairs ($N$)", fontsize=12)
        ax.set_ylabel("Number of SubTokens", fontsize=12)
        plt.yscale("log", base=2) 

        if lam == 8:
            title = rf"{ylabel} ($\lambda_1 = 4,\,\lambda_2 = 2$)"
            fname = f"{filename_prefix}_lambda_4_2.pdf"
        else:
            title = rf"{ylabel} ($\lambda = {lam}$)"
            fname = f"{filename_prefix}_lambda_{lam}.pdf"

        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.legend(frameon=False, fontsize=11)

        plt.tight_layout()
        fig.savefig(fname, format="pdf")
        plt.close(fig)
        print(f"Saved → {fname}")


plot_queue_metric("mean", "Mean Queue Size",    "queue_mean")
plot_queue_metric("max",  "Max Queue Size",     "queue_max")
plot_queue_metric("std",  "Std Dev of Q Size",  "queue_std")


# ─────────────────────────────────────────────────────────────────────────────
# 4b) Plot latency metrics (mean, median, 75th‐pct, max, std) in seconds.
#     Same λ labeling logic as above.
# ─────────────────────────────────────────────────────────────────────────────
def plot_latency_metric(metric_key, ylabel, filename_prefix):
    palette = sns.color_palette("deep", 2)
    for lam in [2, 4, 8]:
        subset = df_latency[df_latency["lambda"] == lam]
        q1 = subset[f"q1_{metric_key}"]
        q2 = subset[f"q2_{metric_key}"]

        fig, ax = plt.subplots(figsize=(6, 4))
        idx = np.arange(len(subset))
        w = 0.35

        ax.bar(idx,     q1, width=w, color=palette[0], edgecolor="black", label="Client 1")
        ax.bar(idx + w, q2, width=w, color=palette[1], edgecolor="black", label="Client 2")

        ax.set_xticks(idx + w / 2)
        ax.set_xticklabels(subset["N_label"], fontsize=12)
        ax.set_xlabel(r"Number of Pairs ($N$)", fontsize=12)
        ax.set_ylabel("Latency (s)", fontsize=12)
        plt.yscale("log", base=2) 
        if lam == 8:
            title = rf"{ylabel} ($\lambda_1 = 4,\,\lambda_2 = 2$)"
            fname = f"{filename_prefix}_lambda_4_2.pdf"
        else:
            title = rf"{ylabel} ($\lambda = {lam}$)"
            fname = f"{filename_prefix}_lambda_{lam}.pdf"

        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.legend(frameon=False, fontsize=11)

        plt.tight_layout()
        fig.savefig(fname, format="pdf")
        plt.close(fig)
        print(f"Saved → {fname}")


plot_latency_metric("mean",   "Mean Latency (s)",            "mean_latency")
plot_latency_metric("median", "Median Latency (s)",          "median_latency")
plot_latency_metric("75pct",  "75th‐Percentile Latency (s)",  "75pct_latency")
plot_latency_metric("max",    "Max Latency (s)",             "max_latency")
plot_latency_metric("std",    "Std Dev of Latency (s)",      "std_latency")
