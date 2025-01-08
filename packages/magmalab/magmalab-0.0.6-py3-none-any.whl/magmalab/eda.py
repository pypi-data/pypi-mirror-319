import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from plunge import scatterplot
from sklearn import metrics

from scipy.stats import pearsonr
from sklearn import metrics

def xlim(ax):
    return ax.get_xlim()

def ylim(ax):
    return ax.get_ylim()


# Mapping of string identifiers to metric functions
metric_functions = {
    'R²': metrics.r2_score,
    'RSE': lambda y_test, y_pred: np.sqrt(np.sum((y_test - y_pred)**2) / (len(y_test) - 2)),
    'MAE': metrics.mean_absolute_error,
    'MAPE': metrics.mean_absolute_percentage_error,
    'MSE': lambda y_test, y_pred: metrics.root_mean_squared_error(y_test, y_pred)**2,
    'RMSE': metrics.root_mean_squared_error,
    'MSLE': lambda y_test, y_pred: metrics.root_mean_squared_log_error(y_test, y_pred)**2,
    'RMSLE': metrics.root_mean_squared_log_error,
    'Pearson': lambda y_test, y_pred: pearsonr(y_test, y_pred)[0]
}

def calculate_metrics(y_test: np.ndarray, y_pred: np.ndarray, metric_names):
    """
    Calculate specified metrics based on provided metric names.

    Parameters:
    - y_test (np.ndarray): True values.
    - y_pred (np.ndarray): Predicted values.
    - metric_names (List[str]): List of metric names to calculate.

    Returns:
    - Dict[str, float]: Dictionary with metric names as keys and calculated values as values.
    """
    results = {}
    for name in metric_names:
        if name in metric_functions:
            try:
                result = metric_functions[name](y_test, y_pred)
                results[name] = result
            except ValueError as e:
                results[name] = f"Error: {e}"
        else:
            results[name] = "Metric not available"
    return results



def PredictionError(y_test, y_pred, metric_names=None, ax=None, cdot='forestgreen', cline = 'red'):
    """
    Generates a prediction error plot with user-selected metrics displayed as text.
    
    Parameters:
    - y_test: Array of true values.
    - y_pred: Array of predicted values.
    - metric_names: List of metric names to display in the plot text.
    - ax: Matplotlib axis to plot on. Creates a new axis if None.
    - color: Color of the regression plot.
    
    Returns:
    - The axis with the plot.
    """
    # Set default metrics if none are provided
    if metric_names is None:
        metric_names = ['MAE', 'MSE', 'RMSE', 'Pearson']

    # Calculate the specified metrics
    metrics_results = calculate_metrics(y_test, y_pred, metric_names)

    # Prepare plot
    ax = plt.subplots()[1] if not ax else ax
    sns.regplot(x=y_test, y=y_pred, color=cdot,ax=ax)
    
    # Diagonal reference line for perfect predictions
    ax.plot(xlim(ax), xlim(ax), linestyle = '--', color = cline)

    # Generate text for metrics to display
    metric_text = "\n  " + f'N: {len(y_test)}\n  ' + "\n  ".join([f"{name}: {value:.2f}" if isinstance(value, float) else f"{name}: {value}" for name, value in metrics_results.items()])
    ax.text(s=metric_text, x=xlim(ax)[0], y=ylim(ax)[1], fontsize=10, ha='left', va='top')

    # Customize axis labels and title
    ax.set_title(f'Prediction Error')
    ax.set_xlabel('True Value')
    ax.set_ylabel('Predicted Value')

    return ax


def boxplots(df, cols, hue, nrows, ncols, figsize, wspace = 0.4, hspace = 0.4, title = None, y_title = 1, fontsize_title = 16, fontsize_label = 14, fontsize_count = 12, palette = 'tab10', background_colors = False, legend = True):
    # Creating Figure
    fig, axs = plt.subplots(nrows, ncols, figsize = figsize)
    fig.subplots_adjust(wspace = wspace, hspace = hspace)
    fig.suptitle(title, y = y_title, fontsize = fontsize_title)

    # Preparing the Data (filtering NaNs once)
    data = df[cols + [hue]].dropna(subset = [hue]).sort_values(by = hue)

    # Iterating over the Axis
    for i, (x, ax) in enumerate(zip(cols, axs.ravel())):
        # Filtering for non-null x values
        x_data = data.dropna(subset = [x])

        # Creating the Axis
        sns.boxplot(data = x_data, x = x, y = hue, hue = hue, palette = palette, legend = legend, orient = 'h', ax = ax)

        # Labels and Limits
        ax.set_xlabel(x, fontsize = fontsize_label)
        ax.set_ylabel(None)
        ax.tick_params(axis = 'x', labelsize = fontsize_count)
        ax.tick_params(axis = 'y', labelsize = fontsize_count)

        # Create a secondary y-axis for sample counts
        ax2 = ax.twinx()
        ax2.set_ylim(ax.get_ylim())

        # Count samples and set y-ticks for the secondary axis
        sample_counts = x_data[hue].value_counts().sort_index()
        ax2.set_yticks(ax.get_yticks())
        ax2.set_yticklabels(sample_counts, fontsize = fontsize_count)

        if background_colors:
            ax.set_facecolor(background_colors[i])

    return fig, axs

def histplot(data, x, ax = False, fontsize = 8, color = 'royalblue', gap = 1):
    ax = plt.subplots()[1] if not ax else ax
    stats = 'N: {} \nM: {:.2f} \nx̄: {:.2f} \nσ: {:.2f} \ncv: {:.2f} \n'.format(
            data[x].dropna().shape[0], 
            data[x].median(),
            data[x].mean(),
            data[x].std(),
            data[x].std()/data[x].mean() if data[x].mean() != 0 else 0)
    ax = sns.histplot(data = data, x = x, kde = True, color = color, ax = ax)
    ax.set_title(ax.get_xlabel(), fontsize = fontsize)
    ax.set_xlabel(None)
    ax.set_ylabel('Quantidade', fontsize = fontsize)
    ax.set_xlim(ax.get_xlim()[0], ax.get_xlim()[1]*gap)
    ax.text(s = stats, x = ax.get_xlim()[1], y = ax.get_ylim()[1]*0.99, fontsize = fontsize, ha='right', va='top')

class Correlation():
    def __init__(self, data, round = 2):
        self.data = data
        self.corr = data.corr(numeric_only=True)
        self.cmap = sns.diverging_palette(10, 150, n=1000, center='light') 
        self.fmt = f".{round}f"

    def Heatmap(self, figsize, fontsize, ticksfontsize):
        ax = sns.heatmap(data=self.corr, vmin=-1, vmax=1, annot=True, cmap=self.cmap, fmt = self.fmt, xticklabels=self.corr.columns, yticklabels=self.corr.columns, annot_kws={"size": ticksfontsize})
        ax.figure.set_size_inches(figsize)
        ax.set_title('Matriz de Correlação', fontdict={'fontsize':fontsize}, pad=16)
        ax.set_xticklabels(ax.get_xticklabels(), fontsize = ticksfontsize, rotation=-75)
        ax.set_yticklabels(ax.get_yticklabels(), fontsize = ticksfontsize)
        return ax

    def Columns(self, colsX, colsY, lim = 0.5, figsize = (5, 6), wspace = 4):
        fig, axs = plt.subplots(1, len(colsY), figsize=figsize)   
        fig.subplots_adjust(hspace=0.3, wspace=wspace)
        for col, ax in zip(colsY, axs.ravel()):
            dados = self.data[list(set(colsX + [col]))].corr(numeric_only = True)
            data = dados[col].sort_values(ascending = False)[1:]
            cell = data[(data < -lim) | (data > lim)].to_frame()
            sns.heatmap(cell, vmin=-1, vmax=1, annot=True, cmap=self.cmap, fmt = self.fmt, cbar = False, ax = ax)
            ax.set_title(col, fontsize = 14, y = 1.02)
        return fig, ax
    
    def GroupQuerry(self, group1, group2, lim = 0.2, rotation = 0, ax = None):
        if ax is None:
            fig, ax = plt.subplots()

        c = self.corr.loc[group1, group2].stack().reset_index().rename(columns={'level_0': 'Variable 1', 'level_1': 'Variable 2', 0: 'Correlation'})
        c = c[c['Variable 1'] < c['Variable 2']]
        c = c.query('Correlation > abs(@lim) or Correlation < -abs(@lim)').sort_values(by = 'Correlation', ascending = False)
        c['Not Null Samples'] = c.apply(lambda row: self.data[row[['Variable 1', 'Variable 2']]].dropna().shape[0], axis = 1)

        sns.heatmap(c[['Correlation']], vmin = -1, vmax = 1, annot = True, cmap = self.cmap, fmt = self.fmt, cbar = False, ax = ax)

        ax_ = ax.twinx()
        ax_.set_ylim(ax.get_ylim())
        ax_.set_yticks(ax.get_yticks())

        ax.set_yticklabels(c['Variable 1'] + " / " + c['Variable 2'], rotation = rotation)
        ax_.set_yticklabels(c['Not Null Samples'], rotation = rotation)

    def getTopCorrelations(self, col, qtd):
        data = self.corr[col].abs().sort_values(ascending=False).dropna()[1:qtd+1]
        return list(data.index)

def main_correlations(df, feed, mineralogy):
    corr = Correlation(df[feed + mineralogy])
    abs_corr_matrix = corr.corr.abs()
    np.fill_diagonal(abs_corr_matrix.values, 0)
    top_10_filtered_corrs = abs_corr_matrix.unstack().sort_values(ascending=False).head(40).index[::2]

    fig, axs = plt.subplots(5, 4, figsize=(20, 20))
    fig.subplots_adjust(wspace = 0.45, hspace = 0.45)
    for ax, (col1, col2) in zip(axs.ravel(), top_10_filtered_corrs):
        if col1 in mineralogy and col2 in mineralogy:
            color = 'indianred'
        elif col1 in feed and col2 in feed:
            color = 'skyblue'
        else:
            color = 'orange' 
        scatterplot(df = df, x = col1, y = col2, ax = ax, fontsize=18, color = color)
    return fig, axs