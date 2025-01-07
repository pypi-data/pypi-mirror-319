# Streamlit Donut

`streamlit-donut` is a Streamlit component for rendering customizable donut charts. This package allows you to easily create visually appealing donut charts in your Streamlit applications.

## Installation

You can install the package using pip:

```sh
pip install streamlit-donut
```
# Usage
Here is an example of how to use the st_donut function in your Streamlit application:

```sh
import streamlit as st
from streamlit_donut import st_donut

# Example usage
progress = st.slider("Progress", -100, 100, 10)
size = 200
text_size = 24

st_donut(
    label="Site Completion",
    value=progress,
    outOf=100,
    units="%",
    size=size,
    value_text_color="purple",
    text_size=text_size,
    background_stroke_width=30,
    arc_stroke_width=40,
    direction="clockwise",
    delta="-10%",
    rounded=True,
    label_visibility=True,
    hide_background=True,
)
```

## Parameters

- `label` (str): The label for the donut chart.
- `value` (float): The current value to be displayed on the donut chart.
- `outOf` (float, optional): The maximum value of the donut chart. Default is 100.
- `units` (str, optional): The units to be displayed next to the value. Default is an empty string.
- `delta` (Optional[str], optional): The delta value to be displayed below the main value. Default is None.
- `space` (int, optional): The vertical space between the main value and the delta value. Default is 30.
- `size` (int, optional): The size of the donut chart. Default is 180.
- `direction` (Literal["clockwise", "anticlockwise"], optional): The direction of the donut chart. Default is "clockwise".
- `text_size` (int, optional): The font size of the main value. Default is 50.
- `delta_text_size` (int, optional): The font size of the delta value. Default is 18.
- `value_text_color` (Optional[str], optional): The color of the main value text. Default is None.
- `arc_bg_color` (Optional[str], optional): The background color of the arc. Default is None.
- `background_stroke_width` (int, optional): The stroke width of the background circle. Default is 19.
- `arc_stroke_width` (Optional[int], optional): The stroke width of the arc. Default is None.
- `rounded` (bool, optional): Whether the arc should have rounded edges. Default is True.
- `label_visibility` (bool, optional): Whether the label should be visible. Default is True.
- `hide_background` (bool, optional): Whether the background circle should be hidden. Default is False.

## License
This project is licensed under the Apache License 2.0.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## Acknowledgements
Inspired by this [CodePen example](https://codepen.io/benjaminlry/pen/xQydro?anon=true&view=pen).

Author
Benson Nderitu (bent25066@gmail.com)