import os
from copy import deepcopy
from typing import List, Dict, Optional, Any
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
    default: int = 0
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

    key : any, optional
        An optional key to uniquely identify this component instance (useful for caching or re-rendering).

    default : int, optional
        The index of the tab to be used as the default tab (default is 0).

    Returns:
    --------
    component_value : any
        The default value or the result from the `_big_text_tabs` internal function call.
    
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

    # Handle cases where tab_data is an empty list or None
    if tab_data is None or len(tab_data) == 0:
        component_value = _big_text_tabs(tab_data=tab_data, styles=styles, key=key, default=None)
    else:
        # Check if the default index is valid
        if default < 0 or default >= len(tab_data):
            raise IndexError(f"Default index {default} is out of range for tab_data of length {len(tab_data)}.")
        
        # Use the specified default index's value
        copy_of_tabs = deepcopy(tab_data)
        default_to_view = copy_of_tabs[default]
        del default_to_view["title"]
        component_value = _big_text_tabs(tab_data=tab_data, styles=styles, key=key, default=default_to_view)

    return component_value
