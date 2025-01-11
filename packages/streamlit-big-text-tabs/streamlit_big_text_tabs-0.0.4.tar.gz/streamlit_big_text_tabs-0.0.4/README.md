# streamlit-big-text-tabs 

Streamlit component that allows you to do big text tabs

## Installation instructions

```sh
pip install streamlit-big-text-tabs 
```

## Usage instructions

```python
import streamlit as st
from big_text_tabs import big_text_tabs


styles_ =  """
        .tab-container { }
        .tab-text-container { }
        .tab-text { }
        .tab-text.clicked-tab { }
    """

tabs_data = [
    { "index": 0, "title": "Tab 1", "value": "tab_one" },
    { "index": 1, "title": "Tab 2", "value": "tab_two" },
    { "index": 2, "title": "Tab 3", "value": "tab_three" }
  ]

tab_selected = big_text_tabs(tab_data=tabs_data, styles=styles_)

st.write(tab_selected)

# returns { "index":0, "value":"tab_one" }
```