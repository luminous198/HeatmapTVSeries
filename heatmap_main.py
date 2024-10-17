import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.patches import Ellipse


def create_heatmap(data, figsize=(10, 8), bg_color='black', text_color='white',
                   value_font_size=14, value_font_weight='bold',
                   show_colorbar=False, x_labels=None, y_labels=None,
                   xaxis_text_color="white", yaxis_text_color="white",
                   value_figure_type="rectangle",
                   value_figure_params={"padding": 0.05, "rounding_size": 0.2, "length": 0.8, "height": 0.8},
                   xaxis_text_fontweight="bold", yaxis_text_fontweight="bold",
                   xaxis_text_fontsize=12, yaxis_text_fontsize=14,
                   value_color_map="Greens", heatmap_kwargs={}):
    """
    Create a customizable heatmap with specified shapes for the values.

    Parameters
    ----------
    data : list of list
        2D data for the heatmap. Each inner list represents a row of values.

    figsize : tuple, optional
        Specifies the size of the figure in inches. Default is (10, 8).

    bg_color : str, optional
        Background color of the figure and axes. Default is 'black'.

    text_color : str, optional
        Color of the text displayed on the heatmap. Default is 'white'.

    value_font_size : int, optional
        Font size of the text annotations inside the shapes. Default is 14.

    value_font_weight : str, optional
        Font weight of the text annotations inside the shapes. Can be 'normal' or 'bold'. Default is 'bold'.

    value_color_map : str, optional
        Colormap used for coloring the shapes in the heatmap. Default is 'Greens'.

    show_colorbar : bool, optional
        Determines whether to display the color bar alongside the heatmap. Default is False.

    x_labels : list of str, optional
        Custom labels for the x-axis. Default is None, which generates default labels.

    y_labels : list of str, optional
        Custom labels for the y-axis. Default is None, which generates default labels.

    xaxis_text_color : str, optional
        Color of the x-axis text labels. Default is 'white'.

    yaxis_text_color : str, optional
        Color of the y-axis text labels. Default is 'white'.

    value_figure_type : str, optional
        Type of shape used to represent values in the heatmap. Can be 'rectangle' or 'ellipse'. Default is 'rectangle'.

    value_figure_params : dict, optional
        Parameters for the shape used to represent values. Contains:
        - padding : float
            Padding around the shape. Default is 0.05.
        - rounding_size : float
            Radius of the corners for rectangles. Default is 0.2 (not applicable if shape is ellipse).
        - width : float
            Width of the ellipse. Must be specified if value_figure_type is 'ellipse'.
        - height : float
            Height of the ellipse. Must be specified if value_figure_type is 'ellipse'.

    xaxis_text_fontweight : str, optional
        Font weight of the x-axis text labels. Default is 'bold'.

    yaxis_text_fontweight : str, optional
        Font weight of the y-axis text labels. Default is 'bold'.

    xaxis_text_fontsize : int, optional
        Font size of the x-axis text labels. Default is 12.

    yaxis_text_fontsize : int, optional
        Font size of the y-axis text labels. Default is 14.
    """

    xlen = len(data)
    ylen = len(data[0])

    # Use a mask to remove all color values when plotting the heatmap
    mask = np.ones_like(data, dtype=bool)

    # Set up the figure
    fig, ax = plt.subplots(figsize=figsize)

    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    # Create the heatmap without gridlines (linewidths=0)
    sns.heatmap(data, annot=False, cmap=None, mask=mask, linewidths=0, cbar=show_colorbar, ax=ax, **heatmap_kwargs)

    # Set axis labels
    ax.set_xticklabels(x_labels if x_labels else [f"S{i + 1}" for i in range(ylen)], fontsize=xaxis_text_fontsize,
                       fontweight=xaxis_text_fontweight, color=xaxis_text_color)
    ax.xaxis.set_ticks_position('top')
    ax.set_yticklabels(y_labels if y_labels else [f"E{i + 1}" for i in range(xlen)], fontsize=yaxis_text_fontsize,
                       rotation=0, fontweight=yaxis_text_fontweight, color=yaxis_text_color)

    # Add shaded rounded rectangles in place of each heatmap square
    for i in range(xlen):
        for j in range(ylen):
            if data[i][j] != 0:
                cmaps = plt.get_cmap(value_color_map)
                color_value = cmaps(data[i][j] / np.max(data))
            else:
                color_value = "white"

            if value_figure_type == "ellipse":
                shape_value = Ellipse(
                    (j + 0.5, i + 0.5),  # Center of the ellipse
                    width=value_figure_params.get("width"),  # Width of the ellipse
                    height=value_figure_params.get("height"),  # Height of the ellipse
                    edgecolor='black',
                    facecolor=color_value,
                )
            else:
                shape_value = FancyBboxPatch(
                    (j + 0.1, i + 0.1), value_figure_params.get("length"), value_figure_params.get("height"),
                    boxstyle=f"round,pad={value_figure_params.get('padding')},rounding_size={value_figure_params.get('rounding_size')}",
                    edgecolor='black', facecolor=color_value, mutation_aspect=1
                )
            ax.add_patch(shape_value)
            # Add the text annotation inside the rounded rectangle
            if data[i][j] != 0:
                ax.text(j + 0.5, i + 0.5, f"{data[i][j]:.1f}", color=text_color, ha='center', va='center',
                        fontsize=value_font_size, fontweight=value_font_weight)

    # Display the plot
    plt.show()


data = [
    [10.0, 10.0, 9.8, 9.5, 9.6, 8.6, 9.3, 9.2],  # Episode 1
    [10.0, 8.9, 8.9, 10.0, 9.6, 8.7, 9.6, 8.7],  # Episode 2
    [8.6, 10.0, 9.2, 9.6, 10.0, 8.7, 9.0, 7.3],  # Episode 3
    [10.0, 9.7, 10.0, 9.6, 9.6, 10.0, 9.7, 5.8],  # Episode 4
    [9.5, 9.6, 9.8, 9.8, 9.6, 9.8, 9.5, 4.9],  # Episode 5
    [10.0, 10.0, 8.3, 10.0, 5.4, 8.8, 8.4, 4.8],  # Episode 6
    [10.0, 10.0, 7.7, 10.0, 8.3, 9.8, 8.7, 0.0],  # Episode 7
    [10.0, 9.2, 9.7, 9.6, 10.0, 8.5, 0, 0.0],  # Episode 8
    [10.0, 9.2, 10.0, 9.8, 9.2, 9.9, 0.0, 0.0],  # Episode 9
    [10.0, 9.2, 10.0, 9.8, 9.2, 9.9, 0.0, 0.0]  # Episode 10
]

# Call the function with parameters
create_heatmap(data, figsize=(15, 18), bg_color='black', text_color='white',
               value_font_size=35, value_font_weight='bold', value_color_map='Blues',
               show_colorbar=False,
               xaxis_text_color="white", yaxis_text_color="white",
               value_figure_type="rectangle",
               value_figure_params={"padding": 0.05, "rounding_size": 0.2, "length": 0.8, "height": 0.8},
               xaxis_text_fontweight="bold", yaxis_text_fontweight="bold",
               xaxis_text_fontsize=35, yaxis_text_fontsize=35,
               x_labels=[f"S{i + 1}" for i in range(len(data[0]))],
               y_labels=[f"E{i + 1}" for i in range(len(data))],
               heatmap_kwargs={"square": True}
               )

