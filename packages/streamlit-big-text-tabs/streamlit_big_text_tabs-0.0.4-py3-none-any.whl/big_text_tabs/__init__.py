import os
import streamlit as st
from copy import deepcopy
from typing import List, Dict, Optional, Any, Callable
import streamlit.components.v1 as components

_RELEASE = True  

if not _RELEASE:
    _big_text_tabs = components.declare_component(
        "big_text_tabs",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _big_text_tabs = components.declare_component("big_text_tabs", path=build_dir)

def big_text_tabs(
    tab_data: Optional[List[Dict[str, Any]]] = None,
    styles: Optional[str] = None,
    key: Optional[Any] = None,
    default: int = 0,
    on_change: Callable = None
) -> Any:
    """
    Generates a big text tab component with the specified data, styles, and key.

    Parameters:
    -----------
    tab_data : list, optional
        A list of dictionaries, each representing a tab, with the following required format:
        [
            { "index": 0, "title": "Tab 1", "value": "tab_one" },
            { "index": 1, "title": "Tab 2", "value": "tab_two" },
            { "index": 2, "title": "Tab 3", "value": "tab_three" }
        ]
        - `index` (int): The position of the tab in the list.
        - `title` (str): The display title for the tab.
        - `value` (str): The value associated with the tab.
        If not provided or not in this format, a TypeError will be raised.

    styles : str, optional
        A string containing custom CSS rules to style the tabs.
        Example:
            '''
                .tab-container { }
                .tab-text-container { }
                .tab-text { }
                .tab-text.clicked-tab { }
            '''
    
    on_change : callabled function
        A function to run when the widget is interacted with.
        Example:
            ```
                if "tab_sel" not in st.session_state:
                    st.session_state["tab_sel"] = None 

                def on_change_tab():
                    st.session_state["tab_sel"] = st.session_state["big_text_tab"]
                
                data = [{...}]
                big_text_tabs(tab_data=data, on_change=on_change_tab, key="big_text_tab")
                    
            ```

    key : any, optional
        An optional key to uniquely identify this component instance (useful for caching or re-rendering).

    default : int, optional
        The index of the tab to be used as the default tab (default is 0).

    Returns:
    --------
    component_value : any
        The default value or dictionary {"index":0, "value":"value"} for example
    
    Raises:
    -------
    TypeError:
        If `tab_data` is not a list or is not in the required format.
    IndexError:
        If `default` is out of range of the `tab_data` list.
    """

    # Validate that `tab_data` is a list or None
    if not isinstance(tab_data, list) and tab_data is not None:
        raise TypeError("tab_data must be a list in the required format: "
                        "[{ 'index': int, 'title': str, 'value': str }, ...]")
        return 
    
    else:
        # Check if the default index is valid
        if default < 0 or default >= len(tab_data):
            raise IndexError(f"Default index {default} is out of range for tab_data of length {len(tab_data)}.")
        
        # Use the specified default index's value
        copy_of_tabs = deepcopy(tab_data)
        default_to_view = copy_of_tabs[default]
        del default_to_view["title"]
        component_value = _big_text_tabs(
            tab_data=tab_data, 
            styles=styles, 
            key=key, 
            default=default_to_view,
            on_change=on_change,
            )

        return component_value
