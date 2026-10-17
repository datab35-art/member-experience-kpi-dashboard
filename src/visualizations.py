"""Visualization helpers for the KPI dashboard."""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np


def plot_kpi_tiles(kpis: dict, title="Executive KPI Dashboard"):
    """Render KPI summary tiles in a grid layout."""
    n = len(kpis)
    cols = 4
    rows = (n + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(18, 4.5 * rows))
    fig.suptitle(title, fontsize=16, fontweight="bold", y=1.02)

    if rows == 1:
        axes = [axes]

    flat_axes = [ax for row in axes for ax in (row if hasattr(row, "__len__") else [row])]

    for idx, (label, (value, color)) in enumerate(kpis.items()):
        ax = flat_axes[idx]
        ax.text(0.5, 0.55, value, transform=ax.transAxes, fontsize=30,
                fontweight="bold", ha="center", va="center", color=color)
        ax.text(0.5, 0.2, label, transform=ax.transAxes, fontsize=11,
                ha="center", va="center", color="#555555")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=False,
                                   edgecolor="#DDDDDD", linewidth=2, transform=ax.transAxes))

    for idx in range(len(kpis), len(flat_axes)):
        flat_axes[idx].axis("off")

    plt.tight_layout()
    return fig


def plot_monthly_trends(monthly_df, metrics, titles=None, figsize=(16, 10)):
    """Plot monthly trend lines for multiple metrics."""
    n = len(metrics)
    cols = 2
    rows = (n + 1) // 2

    fig, axes = plt.subplots(rows, cols, figsize=figsize)
    axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

    for idx, metric in enumerate(metrics):
        ax = axes[idx]
        ax.plot(monthly_df["month"], monthly_df[metric], marker="o",
                linewidth=2, markersize=5, color="#4C72B0")
        ax.fill_between(range(len(monthly_df)), monthly_df[metric],
                        alpha=0.1, color="#4C72B0")
        title = titles[idx] if titles else metric.replace("_", " ").title()
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.set_xlabel("")
        ax.tick_params(axis="x", rotation=45)
        ax.grid(axis="y", alpha=0.3)

    for idx in range(len(metrics), len(axes)):
        axes[idx].axis("off")

    plt.tight_layout()
    return fig


def plot_regional_comparison(regional_df, metric, title=None, color_positive="#27AE60"):
    """Horizontal bar chart comparing a metric across regions."""
    fig, ax = plt.subplots(figsize=(10, 5))

    sorted_df = regional_df.sort_values(metric)
    overall_mean = sorted_df[metric].mean()
    colors = [color_positive if v >= overall_mean else "#E74C3C" for v in sorted_df[metric]]

    ax.barh(sorted_df["region"], sorted_df[metric], color=colors, edgecolor="black", alpha=0.85)
    ax.axvline(overall_mean, color="gray", linestyle="--", alpha=0.7, label=f"Avg: {overall_mean:.2f}")
    ax.set_title(title or metric.replace("_", " ").title(), fontsize=13, fontweight="bold")
    ax.legend()

    for i, v in enumerate(sorted_df[metric]):
        ax.text(v + 0.005, i, f"{v:.2f}", va="center", fontsize=9)

    plt.tight_layout()
    return fig


def plot_channel_mix(df, title="Interaction Channel Mix"):
    """Pie chart + bar chart showing channel distribution."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    channel_counts = df["channel"].value_counts()
    axes[0].pie(channel_counts.values, labels=channel_counts.index, autopct="%1.1f%%",
                colors=sns.color_palette("muted", len(channel_counts)), startangle=90)
    axes[0].set_title("Channel Distribution", fontsize=13, fontweight="bold")

    monthly_channel = df.groupby(["month", "channel"]).size().unstack(fill_value=0)
    monthly_channel.plot(kind="bar", stacked=True, ax=axes[1],
                         color=sns.color_palette("muted", len(channel_counts)))
    axes[1].set_title("Monthly Channel Volume", fontsize=13, fontweight="bold")
    axes[1].set_xlabel("")
    axes[1].tick_params(axis="x", rotation=45)
    axes[1].legend(title="Channel", bbox_to_anchor=(1.05, 1), loc="upper left")

    plt.tight_layout()
    return fig


def plot_satisfaction_distribution(df):
    """Distribution of satisfaction scores with category breakdown."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].hist(df["satisfaction_score"], bins=20, edgecolor="black", alpha=0.7, color="#4C72B0")
    axes[0].set_title("Satisfaction Score Distribution", fontsize=13, fontweight="bold")
    axes[0].set_xlabel("Score (1-10)")
    axes[0].set_ylabel("Count")
    axes[0].axvline(df["satisfaction_score"].mean(), color="red", linestyle="--",
                    label=f'Mean: {df["satisfaction_score"].mean():.1f}')
    axes[0].legend()

    cat_sat = df.groupby("contact_reason")["satisfaction_score"].mean().sort_values()
    bar_colors = ["#E74C3C" if v < 6.5 else "#F39C12" if v < 7.0 else "#27AE60" for v in cat_sat.values]
    axes[1].barh(cat_sat.index, cat_sat.values, color=bar_colors, edgecolor="black")
    axes[1].set_title("Avg Satisfaction by Contact Reason", fontsize=13, fontweight="bold")
    axes[1].set_xlabel("Mean Score")
    for i, v in enumerate(cat_sat.values):
        axes[1].text(v + 0.02, i, f"{v:.1f}", va="center", fontweight="bold")

    plt.tight_layout()
    return fig
