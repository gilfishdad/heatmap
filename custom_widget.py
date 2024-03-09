#this code works great.  its possible too much memory is used
#on this particular machine so when it is running it cannot run another cell

import ipywidgets as widgets
from IPython.display import display, clear_output
from ipywidgets import HBox, Label

class CustomDataFrameWidget:
    def __init__(self, dataframe_class):
        self.dataframe_class = dataframe_class
        self.slider = widgets.IntSlider(
            value=0,
            min=0,
            max=len(dataframe_class.df)-1,
            step=1,
            description='Index:',
            continuous_update=False
        )
        self.output = widgets.Output()
        self.slider.observe(self.on_value_change, names='value')
        display(self.slider, self.output)
        
    def on_value_change(self, change):
        with self.output:
            clear_output()  # Clear the previous output
            index = change['new']
            data = self.dataframe_class.df.iloc[index]
            for col, val in data.items():
                # Set the width to approximately 100px, adjust as needed for your font/display
                text_widget_layout = widgets.Layout(width='100px')
                text_widget = widgets.Text(value=str(val), disabled=True, layout=text_widget_layout)  # Text widget for the value
                label_widget = Label(col)  # Label widget for the column name
                hbox = HBox([text_widget, label_widget])  # Place value (text widget) to the left of the label
                display(hbox)

# Assuming `dataframe_class` is an instance of CustomDataFrame
# Example usage:
widget = CustomDataFrameWidget(dataframe_class)
