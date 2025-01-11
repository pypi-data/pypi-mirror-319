import streamlit as st
from functools import partial
from __init__ import big_text_tabs

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

if "test_cols" not in st.session_state:
    st.session_state["test_cols"] = None

def test_change(variable):
    if st.session_state["test_cols"]:
        st.session_state["test_cols"].write(variable)

# Correctly passing a callable using partial
test = big_text_tabs(tab_data=tabs_data, on_change=partial(test_change, "hii"), styles=styles_)

# Initialize test_cols after passing the partial callable
st.session_state["test_cols"] = st.container()
