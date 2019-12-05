"""Visualize the final bpi dataset.
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from bld.project_paths import project_paths_join as ppj

# Import dataset bpi_final
bpi_final = pd.read_csv(ppj("OUT_DATA", "bpi_final.csv"))

# Replace -100 for nan's. Preparing for regplots
for BPI in bpi_final.loc[:, "bpiA":"bpiE"]:
    bpi_final[BPI] = bpi_final[BPI].replace(-100, np.nan)

# Create two lists and an empty correlations list to fill
subscales = ["antisocial", "headstrong", "hyperactive", "anxiety", "peer"]
bpi_measures = bpi_final.loc[:, "bpiA":"bpiE"].columns.tolist()
correlation_vector = list()

# Append correlations of each BPI & subscale to empty list, correlation_vector
for BPI, subscale in zip(bpi_measures, subscales):
    a = round(bpi_final[BPI].corr(bpi_final[subscale]), 3)
    correlation_vector.append(a)

# Make all font and axes "bold" for upcoming plots
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"

# Define figure "fig" and 5 subplots "axes", with 9 inches width, 13 in. height
fig, axes = plt.subplots(5, figsize=(9, 13))

# PLot correlations to each subplot, ax. Using axes.flatten() makes it iterable
for ax, correlation in zip(axes.flatten(), correlation_vector):
    ax.text(
        0.85,
        0.85,
        "ρ: {}".format(correlation),
        rotation=0,
        size=10,
        weight="bold",
        ha="left",
        va="center",
        transform=ax.transAxes,
    )

# Define space between plots, make title, and background color
fig.subplots_adjust(hspace=1)
fig.suptitle("Correlations between BPI and Normalized Subscales", fontsize=24)
fig.set_facecolor("xkcd:mint green")

# Toss each subplot into regplot plotting means
for ax, subscale, BPI in zip(axes.flatten(), subscales, bpi_measures):
    sns.regplot(
        bpi_final[BPI],
        bpi_final[subscale],
        x_estimator=np.mean,
        ax=ax,
        truncate=True,
        ci=95,
    )

# Save figure
fig.savefig(ppj("OUT_FIGURES", "bpi_subscales_regplot.png"))


###############################################################################
#
# Task 11
#
###############################################################################

# Select subscales for heatmap.
subscale_corr = ["hyperactive", "anxiety", "peer"]

# Create a container that stores all variables we will visualize in the heatmap.
bpi_merged = pd.read_csv(ppj("OUT_DATA", "bpi_merged.csv"))
container_corr = []
merge_column_names = list(bpi_merged.columns.values)

# Store variables in container.
for subscale in subscale_corr:
    for item in merge_column_names:
        if item.startswith(subscale):
            container_corr.append(item)

# Store correlations of relevant variables in dataframe.
corr = bpi_final[container_corr].corr()

# Define size of figure.
fig, ax = plt.subplots(figsize=(20, 16))

# Design mask for heatmap function to hide self correlations and double values.
noself = np.zeros_like(corr)
noself[np.triu_indices_from(noself)] = True

# Generate heatmap.
plot = sns.heatmap(
    corr,
    cmap="RdBu_r",
    center=0,
    vmin=0,
    vmax=0.5,
    mask=noself,
    linewidths=0.2,
    annot=True,
    fmt=".2f",
)

# Set title.
plot.set_title("Correlation: Hyperactivity, Anxiety and Peer Characteristics")

# Save heatmap as png-file.
plt.savefig(ppj("OUT_FIGURES", "heatmap.png"), format="png")
