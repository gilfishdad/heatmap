from bokeh.models import Slider, Column
from bokeh.plotting import curdoc, figure
from bokeh.models.widgets import Button, DataTable, TableColumn, Div
from bokeh.layouts import column, row
import pandas as pd

import pandas as pd
import numpy as np

# Create a DataFrame with 12 columns and 1000 rows, filled with random integers from 0 through 4
df = pd.DataFrame(np.random.randint(0, 5, size=(1000, 12)))

mapping = {
    0: 'Unavailable',
    1: 'Pass',
    2: 'Degraded',
    3: 'Fail',
    4: 'Unknown'
}

# Apply the mapping to the entire DataFrame
df_mapped = df.applymap(lambda x: mapping[x])


# Sample DataFrame setup
#data = {
 #   0: ['Unavailable', 'Unknown'],
#    1: ['Degraded', 'Unavailable'],
#    2: ['Fail', 'Fail'],
#    3: ['Pass', 'Unknown'],
#    # Add the rest of your data here
#}
df = df_mapped

# Map status to colors
status_to_color = {
    'Pass': 'success',
    'Fail': 'danger',
    'Degraded': 'warning',
    'Unavailable': 'primary',
    'Unknown': 'default',
}

# Create a slider to select rows
slider = Slider(start=0, end=len(df) - 1, value=0, step=1, title="Row Selector")

# Function to update button colors based on the selected row
def update(attr, old, new):
    row = slider.value
    for i, button in enumerate(buttons):
        status = df.iloc[row, i]
        button.label = f'Column {i}: {status}'  # Update label with status
        button.button_type = status_to_color.get(status, 'default')

# Initialize buttons
buttons = [Button(label=f'Column {i}: {df.iloc[0, i]}', button_type=status_to_color.get(df.iloc[0, i], 'default')) for i in range(len(df.columns))]

# Attach the update function to the slider
slider.on_change('value', update)

# Layout setup
layout = column(slider, *buttons)

# Add layout to the current document
curdoc().add_root(layout)
