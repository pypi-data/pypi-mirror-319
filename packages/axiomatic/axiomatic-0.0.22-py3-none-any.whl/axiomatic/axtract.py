import ipywidgets as widgets  # type: ignore
from IPython.display import display  # type: ignore
from dataclasses import dataclass, field

OPTION_LIST = {
    "IMAGING TELESCOPE": [
        "Resolution (panchromatic)",
        "Ground sampling distance (panchromatic)",
        "Resolution (multispectral)",
        "Ground sampling distance (multispectral)",
        "Altitude",
        "Half field of view",
        "Mirror aperture",
        "F-number",
        "Focal length",
        "Pixel size (panchromatic)",
        "Pixel size (multispectral)",
        "Swath width",
    ],
    "MITRE_Template": [
        "Object height",
        "Image height",
        "Wavelength",
    ],
}

IMAGING_TELESCOPE = {
    "Resolution (panchromatic)": 1.8,
    "Ground sampling distance (panchromatic)": 0.6,
    "Resolution (multispectral)": 1.8,
    "Ground sampling distance (multispectral)": 0.9,
    "Altitude": 460000,
    "Half field of view": 0.02003638,
    "Mirror aperture": 0.60,
    "F-number": 5.53,
    "Focal length": 3.32,
    "Pixel size (panchromatic)": 8.75e-6,
    "Pixel size (multispectral)": 13e-6,
    "Swath width": 18400,
}

MITRE_Template = {
    "Object height": 1.8,
    "Image height": 1.8,
    "Wavelength": 1.8,
}


@dataclass
class Requirement:
    requirement_name: str
    latex_symbol: str
    value: int
    units: str
    tolerance: float
    sympy_symbol: str = field(init=False)

    def __post_init__(self):
        self.sympy_symbol = self.latex_symbol.replace("{", "").replace("}", "")

    # def getSympySymbol(self):
    #     return latex2sympy(self.latex_symbol)

    @property
    def is_fixed(self):
        return self.tolerance == 0.0

    # @property
    # def equations(self, strict=False):
    #     if self.is_fixed:
    #         return [sympy.Eq(self.getSympySymbol(), self.value)]
    #     else:
    #       signs = [">=", "<="] if not strict else [">", "<"]
    #       bounds = [self.value - self.tolerance, self.value + self.tolerance]
    #       return [
    #             sympy.Rel(self.getSympySymbol(), bound, sign)
    #             for bound, sign in zip(bounds, signs)
    #         ]


def _find_symbol(name, variable_dict):

    matching_keys = [
        key for key, value in variable_dict.items() if name in value["name"]
    ]

    if not matching_keys:
        matching_keys.append("unknown")

    return matching_keys[0]


def requirements_from_table(results, variable_dict):
    requirements = []

    for key, value in results["values"].items():

        latex_symbol = _find_symbol(key, variable_dict)

        name = key
        numerical_value = value["Value"]
        unit = value["Units"]
        tolerance = value["Tolerance"]

        requirements.append(
            Requirement(
                requirement_name=name,
                latex_symbol=latex_symbol,
                value=numerical_value,
                units=unit,
                tolerance=tolerance,
            )
        )

    return requirements


def interactive_table(preset_options_dict, variable_dict):
    """
    Creates an interactive table with a dropdown for selecting options.

    Parameters:
    options_dict (dict): A dictionary where keys are dropdown options and
      values are lists of row names.

    Returns:
    dict: A dictionary containing user inputs for the selected rows.
    """

    variable_names = [details["name"] for details in variable_dict.values()]

    # Placeholder for result dictionary
    result = {}

    # Create dropdown for options
    dropdown = widgets.Dropdown(
        options=list(preset_options_dict.keys()),
        description="Select Option:",
        style={"description_width": "initial"},
    )

    # Dictionary to hold widgets for user input
    value_widgets = {}

    # VBox to stack rows vertically
    rows_output = widgets.VBox()

    # Output widget for confirmation messages
    message_output = widgets.Output()

    # Mutable container to store the current name label width
    name_label_width = ["150px"]  # Default width

    # Function to display the table based on the dropdown selection
    def display_table(change):
        selected_option = change["new"]

        # Clear existing rows
        rows_output.children = []
        value_widgets.clear()

        if selected_option in preset_options_dict:
            rows = preset_options_dict[selected_option]
            max_name_length = max(len(name) for name in rows)
            # Update the name_label_width based on the longest row name
            name_label_width[0] = f"{max_name_length + 2}ch"

            for row_name in rows:
                # Create name label with dynamic width
                name_label = widgets.Label(
                    value=row_name,
                    layout=widgets.Layout(width=name_label_width[0]),
                )

                # Depending on the selected option, set default values
                if selected_option == "IMAGING TELESCOPE":
                    default_value = IMAGING_TELESCOPE.get(row_name, 0.0)
                # elif selected_option == "LIDAR":
                #     default_value = LIDAR.get(row_name, 0.0)
                elif selected_option == "MITRE_Template":
                    default_value = MITRE_Template.get(row_name, 0.0)

                # Create input widgets
                value_text = widgets.FloatText(
                    placeholder="Value",
                    value=default_value,
                    layout=widgets.Layout(width="150px"),
                )
                tolerance_text = widgets.FloatText(
                    placeholder="Tolerance", layout=widgets.Layout(width="150px")
                )
                accuracy_text = widgets.FloatText(
                    placeholder="Accuracy", layout=widgets.Layout(width="150px")
                )
                units_text = widgets.Text(
                    placeholder="Units", layout=widgets.Layout(width="150px")
                )

                # Combine widgets into a horizontal box
                row = widgets.HBox(
                    [
                        name_label,
                        value_text,
                        tolerance_text,
                        accuracy_text,
                        units_text,
                    ]
                )

                # Store the row widgets
                value_widgets[row_name] = row

                # Add the row to the rows_output VBox
                rows_output.children += (row,)

    # Attach handler to dropdown
    dropdown.observe(display_table, names="value")
    display(dropdown)
    display(rows_output)
    display(message_output)

    # Function to collect and store user inputs
    def submit_values(_):
        updated_values = {}

        for key, widget in value_widgets.items():
            variable = widget.children[0].value
            if key.startswith("req_"):
                updated_values[variable] = {
                    "Value": widget.children[1].value,
                    "Tolerance": widget.children[2].value,
                    "Accuracy": widget.children[3].value,
                    "Units": widget.children[4].value,
                }
            else:
                updated_values[key] = {
                    "Value": widget.children[1].value,
                    "Tolerance": widget.children[2].value,
                    "Accuracy": widget.children[3].value,
                    "Units": widget.children[4].value,
                }

        result["values"] = updated_values

        # Display confirmation message
        with message_output:
            message_output.clear_output()

    # Function to add a new requirement row
    def add_req(_):

        unique_key = (
            f"req_{len([k for k in value_widgets if k.startswith('req_')]) + 1}"
        )

        # Create a dropdown for variable selection with dynamic width
        variable_dropdown = widgets.Dropdown(
            options=variable_names,
            description="Variable:",
            style={"description_width": "initial"},
            layout=widgets.Layout(width=2 * name_label_width[0]),
        )
        value_text = widgets.FloatText(
            placeholder="Value",
            layout=widgets.Layout(width="150px"),
        )
        tolerance_text = widgets.FloatText(
            placeholder="Tolerance", layout=widgets.Layout(width="150px")
        )
        accuracy_text = widgets.FloatText(
            placeholder="Accuracy", layout=widgets.Layout(width="150px")
        )
        units_text = widgets.Text(
            placeholder="Units", layout=widgets.Layout(width="150px")
        )

        new_row = widgets.HBox(
            [variable_dropdown, value_text, tolerance_text, accuracy_text, units_text]
        )

        rows_output.children += (new_row,)
        value_widgets[unique_key] = new_row

    submit_button = widgets.Button(description="Submit")
    submit_button.on_click(submit_values)

    add_req_button = widgets.Button(description="Add Requirement")
    add_req_button.on_click(add_req)

    buttons_box = widgets.HBox([submit_button, add_req_button])
    display(buttons_box)

    return result
