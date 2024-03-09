import pandas as pd
import random
import ipywidgets as widgets
from IPython.display import display, clear_output
from ipywidgets import HBox, Label, Layout

class CustomDataFrame:
    def __init__(self, num_rows):
        """Initialize the DataFrame with dynamically generated columns and fill with random integers."""
        self.columns = self.generate_columns()
        self.df = pd.DataFrame(columns=self.columns)
        self.fill_random_integers(num_rows)
        self.init_widget()

    def generate_columns(self):
        """Generates column names based on predefined criteria."""
        columns = []
        for i in range(8):  # Numbers from 0 to 7
            for j in range(4):  # Adjusted for numbers from 0 to 3, to match the requirement to [7,3]
                columns.append(self.generate_string(i, j))
        return columns

    @staticmethod
    def generate_string(num1, num2):
        """Generates a single column name with random keys and underscores."""
        initial_part = f"[{num1}]{random.choice(keys)}[{num2}]"
        while len(initial_part) <= 64:
            if random.choice([True, False]):
                initial_part = random.choice(keys) + "_" + initial_part
            else:
                initial_part = initial_part + "_" + random.choice(keys)
        return initial_part

    def fill_random_integers(self, num_rows):
        """Fill the DataFrame with random integers for each column."""
        data = [{col: random.randint(0, 9) for col in self.columns} for _ in range(num_rows)]
        self.df = pd.DataFrame(data)
        
    def init_widget(self):
        """Initialize and display a widget for browsing dataframe rows."""
        slider = widgets.IntSlider(
            value=0,
            min=0,
            max=len(self.df)-1,
            step=1,
            description='Index:',
            continuous_update=False
        )
        output = widgets.Output()

        def on_value_change(change):
            with output:
                clear_output()  # Clear the previous output
                index = change['new']
                data = self.df.iloc[index]
                for col, val in data.items():
                    text_widget_layout = Layout(width='100px')  # Define layout for text widget
                    text_widget = widgets.Text(value=str(val), disabled=True, layout=text_widget_layout)
                    label_widget = Label(col)
                    hbox = HBox([text_widget, label_widget])  # Place value (text widget) to the left of the label
                    display(hbox)

        slider.observe(on_value_change, names='value')
        
        # Display the widgets
        display(slider, output)
        # Trigger the display update for the initial row
        on_value_change({'new': slider.value})

# Dictionary keys (as per the original code context)
keys = [
    "static", "dynamic", "function", "functional",
    "operational", "spacial", "polar", "horizontal",
    "vertical", "frequency"
]

# Example usage
dataframe_class = CustomDataFrame(num_rows=10)
# The widget will be displayed automatically upon instance creation
