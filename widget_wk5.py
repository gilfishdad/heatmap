import pandas as pd
import random
import panel as pn

# Ensure the Panel extension is activated
pn.extension()

# Define the mappings from numbers to words and colors
number_to_word_map = {
    0: "Unavailable",
    1: "Pass",
    2: "Degraded",
    3: "Fail",
    4: "Unknown",
    5: "NoImport",
    6: "Danger",
    7: "TotalCollapse"
}

number_to_color_map = {
    0: "white",  # Unavailable
    1: "green",  # Pass
    2: "yellow", # Degraded
    3: "red",    # Fail
    4: "grey",   # Unknown
    5: "blue",   # NoImport
    6: "purple", # Danger
    7: "black"   # TotalCollapse
}

# Dictionary keys
keys = [
    "static", "dynamic", "function", "functional",
    "operational", "spacial", "polar", "horizontal",
    "vertical", "frequency"
]

class CustomDataFrame:
    def __init__(self, num_rows):
        self.columns = self.generate_columns()
        self.df = pd.DataFrame(columns=self.columns)
        self.fill_random_integers(num_rows)

    def generate_columns(self):
        columns = []
        for i in range(8):
            for j in range(4):
                columns.append(self.generate_string(i, j))
        return columns

    @staticmethod
    def generate_string(num1, num2):
        initial_part = f"[{num1}]{random.choice(keys)}[{num2}]"
        while len(initial_part) <= 64:
            if random.choice([True, False]):
                initial_part = random.choice(keys) + "_" + initial_part
            else:
                initial_part = initial_part + "_" + random.choice(keys)
        return initial_part

    def fill_random_integers(self, num_rows):
        data = [{col: number_to_word_map[random.randint(0, 7)] for col in self.columns} for _ in range(num_rows)]
        self.df = pd.DataFrame(data)

# Instantiate the CustomDataFrame with 10 rows as an example
dataframe_class = CustomDataFrame(num_rows=200)

# Function to create a widget for each value in the selected row, along with a label
def display_row_widgets(row_index):
    selected_data = dataframe_class.df.iloc[row_index]
    widgets = []
    for col, val in selected_data.items():
        # Map value to color
        color = number_to_color_map[list(number_to_word_map.values()).index(val)]
        value_widget = pn.widgets.TextInput(value=val, disabled=True, width=150, background=color, css_classes=['colored-text-input'])
        label_widget = pn.pane.Markdown(f'**{col}**', width=200)
        widgets.append(pn.Row(label_widget, value_widget))
    return pn.Column(*widgets, name='Row Data')

# Apply custom CSS for the TextInput background color
pn.extension(raw_css=[ """.colored-text-input .bk input { color: black; background-color: inherit; }"""])

# Slider widget to select the row
row_slider = pn.widgets.IntSlider(name='Row', start=0, end=len(dataframe_class.df)-1, step=1, width=400)

# Dynamically update the displayed row's widgets when the slider value changes
@pn.depends(row_slider.param.value)
def update_display(row_index):
    return display_row_widgets(row_index)

# Create and display the dashboard
dashboard = pn.Column("# Custom DataFrame Viewer", row_slider, update_display)
dashboard.servable()
