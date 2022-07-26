# Code for custom code recipe scatterplot-3d (imported from a Python recipe)

# To finish creating your custom recipe from your original PySpark recipe, you need to:
#  - Declare the input and output roles in recipe.json
#  - Replace the dataset names by roles access in your code
#  - Declare, if any, the params of your custom recipe in recipe.json
#  - Replace the hardcoded params values by acccess to the configuration map

# See sample code below for how to do that.
# The code of your original recipe is included afterwards for convenience.
# Please also see the "recipe.json" file for more information.

# import the classes for accessing DSS objects from the recipe
import dataiku
# Import the helpers for custom recipes
from dataiku.customrecipe import *

# Inputs and outputs are defined by roles. In the recipe's I/O tab, the user can associate one
# or more dataset to each input and output role.
# Roles need to be defined in recipe.json, in the inputRoles and outputRoles fields.

# To  retrieve the datasets of an input role named 'input_A' as an array of dataset names:
input_A_names = get_input_names_for_role('input_A_role')
# The dataset objects themselves can then be created like this:
input_A_datasets = [dataiku.Dataset(name) for name in input_A_names]

# For outputs, the process is the same:
output_A_names = get_output_names_for_role('main_output')
output_A_datasets = [dataiku.Dataset(name) for name in output_A_names]


# The configuration consists of the parameters set up by the user in the recipe Settings tab.

# Parameters must be added to the recipe.json file so that DSS can prompt the user for values in
# the Settings tab of the recipe. The field "params" holds a list of all the params for wich the
# user will be prompted for values.

# The configuration is simply a map of parameters, and retrieving the value of one of them is simply:
my_variable = get_recipe_config()['parameter_name']

# For optional parameters, you should provide a default value in case the parameter is not present:
my_variable = get_recipe_config().get('parameter_name', None)

# Note about typing:
# The configuration of the recipe is passed through a JSON object
# As such, INT parameters of the recipe are received in the get_recipe_config() dict as a Python float.
# If you absolutely require a Python int, use int(get_recipe_config()["my_int_param"])


#############################
# Your original recipe
#############################

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
import io

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Read recipe inputs
ecommerce_transactions_with_ip_prepared = dataiku.Dataset("ecommerce_transactions_with_ip_prepared")
df = ecommerce_transactions_with_ip_prepared.get_dataframe()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Filter to only US records
df_usa = df[df["MerchantIP_country"] == "United States"]

# Determine average purchase amount, per customer age and purchase hour
df_avg_purchase = df[["PurchaseHour", "CustomerAge", "OrderTotal"]].groupby(by=["PurchaseHour",
                                                                                "CustomerAge"], as_index=False).mean()

# Scatter plot of avg purchase amount, per customer age and purchase hour
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

xs = df_avg_purchase["PurchaseHour"]
ys = df_avg_purchase["CustomerAge"]
zs = df_avg_purchase["OrderTotal"]

ax.set_xlabel('Purchase Hour')
ax.set_ylabel('Customer Age')
ax.set_zlabel('Avg Order Total')
ax.set_title("US Transactions Only")

ax.scatter(xs, ys, zs)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Save scatter plot to folder
folder_for_plots = dataiku.Folder("MIrujfBg")

buffer = io.BytesIO()
plt.savefig(buffer, format="png")
folder_for_plots.upload_stream("US Transactions Only.png", buffer.getvalue())