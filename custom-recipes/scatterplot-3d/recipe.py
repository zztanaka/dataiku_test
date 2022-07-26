import dataiku
from dataiku.customrecipe import *
import pandas as pd, numpy as np

from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype

from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
import io


### READ PLUGIN INPUTS ###

# Retrieve input and output dataset names
input_dataset_name = get_input_names_for_role('input_dataset')[0]
output_folder_name = get_output_names_for_role('main_output')[0]

# Retrieve mandatory user-defined parameters
plot_title = get_recipe_config().get('plot_title', "Scatter Plot Title")
    
x_axis = get_recipe_config().get('x_axis')
y_axis = get_recipe_config().get('y_axis')
z_axis = get_recipe_config().get('z_axis')

# Retrieve optional user-defined parameters
filter_column = get_recipe_config().get('filter_column')
filter_value = get_recipe_config().get('filter_value')

# Read input dataset as dataframe
input_dataset = dataiku.Dataset(input_dataset_name)
df = input_dataset.get_dataframe()


### ERROR CHECKING OF USER INPUTS ###

# Check that x, y and z axis correspond to column names
if (x_axis not in df.columns) or (y_axis not in df.columns) or (z_axis not in df.columns):
    raise KeyError("X-axis, Y-axis, and Z-axis parameters must be columns in the input dataset.")
    
# Check that x, y, and z axis columns contain numeric values
if (not is_numeric_dtype(df[x_axis])) or (not is_numeric_dtype(df[y_axis])) or (not is_numeric_dtype(df[z_axis])):
    raise ValueError("X-axis, Y-axis, and Z-axis columns should only contain numeric values.")

# Check that the filter column is part of the dataframe (if defined)
if (filter_column != '') and (filter_column not in df.columns):
    raise KeyError("If defined, the filter column parameter must be a column in the input dataset.")
    
    
### GENERATE 3D SCATTER PLOT ###

# Filter values in dataset (if filter_column is defined)
if filter_column != '':
    df = df[df[filter_column].astype(str) == str(filter_value)] # force a string comparison

# Determine average z-axis value, for overlapping x-axis and y-axis values
df_avg_purchase = df[[x_axis, y_axis, z_axis]].groupby(by=[x_axis, y_axis], as_index=False).mean()

# Construct scatter plot 
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

xs = df_avg_purchase[x_axis]
ys = df_avg_purchase[y_axis]
zs = df_avg_purchase[z_axis]

ax.set_xlabel(x_axis)
ax.set_ylabel(y_axis)
ax.set_zlabel(z_axis)
ax.set_title(plot_title)

ax.scatter(xs, ys, zs)


### SAVE SCATTER PLOT TO FOLDER ###

folder_for_plots = dataiku.Folder(output_folder_name)

buffer = io.BytesIO()
plt.savefig(buffer, format="png")
folder_for_plots.upload_stream(plot_title + ".png", buffer.getvalue())