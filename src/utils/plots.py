import numpy as np
import matplotlib.pyplot as plt


def cum_hist(data, column, hist_bins = 30, hist_density = False):
    # Sample data

    df = data[column]
    df = df.dropna()

    # Calculate histogram
    hist, bin_edges = np.histogram(df, bins=hist_bins, density=hist_density)

    # Calculate cumulative percentage
    cumulative_percentage = np.cumsum(hist) / sum(hist) * 100

    # Create main histogram
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.bar(bin_edges[:-1], hist, width=np.diff(bin_edges), edgecolor='black', align='edge')
    if hist_density == True:
        ax1.set_ylabel('Density', color='blue')
    else:
        ax1.set_ylabel('Frequency ', color='blue')

    # Create secondary axis for cumulative percentage
    ax2 = ax1.twinx()
    ax2.plot(bin_edges[:-1], cumulative_percentage, color='red', marker='o', ms=4)
    ax2.set_ylabel('Cumulative Percentage (%)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # Display the plot
    plt.show()