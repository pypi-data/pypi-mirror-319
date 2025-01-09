# `pgss` - Page-Specific SessionState for Streamlit

The `pgss` package provides an easy way to manage session states in Streamlit applications on a per-page basis. By using `PageSessionState`, you can ensure that variables are kept consistent across different pages, even if they have the same variable names. This package is perfect for managing page-specific data without interfering with other pages.

## Installation

You can install `pgss` using `pip`:

```bash
pip install pgss
```

## Usage

Once installed, you can use the [PageSessionState](http://_vscodecontentref_/1) class to manage session states for each page in your Streamlit app. Here's an example:

```python
import streamlit as st
from pgss import PageSessionState  # Import the PageSessionState class

# Create a PageSessionState object for the current page
pss = PageSessionState("page1.py")

# Initialize the session state variable if it does not exist
pss.set_if_not_exist({"count": 1, "text": ""})
# or set as usual
# if "count" not in pss:
#     pss["count"] = 1

# Create a button to increment the counter
if st.button("Increment"):
    pss["count"] += 1

# Display the current value of the count variable
st.write(f"Count: {pss['count']}")

# Use pss(name) to generate a unique key for the text input
if text := st.text_input("Input text", value=pss.text, key=pss("text_key")):
    pss.text = text

st.write(f"pss.text_key: {pss.text_key}")
st.write(f"pss.text: {pss.text}")
```
Adding Keys to Session State
You can add keys to the session state if they do not already exist using the following method:


### How it Works

1. **Page-Specific SessionState**:  
   By creating an instance of `PageSessionState` using the current file (ex: `page.py`), you ensure that the session state is unique to the page. This means that each page can maintain its own state, even if the same variable names are used on multiple pages.

1. **Set Default Values**:  
   The `set_if_not_exist` method allows you to set default values for your session state variables if they haven't been initialized yet. This ensures that the state starts with predefined values.

1. **Adding Keys to Session State**:  
   You can add keys to the session state if they do not already exist using the following method:
   ```python
   if "count" not in pss:
       pss["count"] = 1
   ```

1. **Persistent Session State**:  
   Session state variables are preserved as long as the user is on the same page, making it easy to store and update data across user interactions without losing it between reruns.

1. **Generating Session State Names**:
   The pss(name) method allows you to generate session state names dynamically. This is useful for creating unique keys for Streamlit widgets, ensuring that the session state is correctly managed.

### Example Use Case

You can use this approach in Streamlit applications with multiple pages. For instance, one page could manage a counter, while another page could manage a different state, but both could share the same variable name (`count`) without interfering with each other.

---

## Features

- **Per-page session state management**: Ensures that session state variables are unique to each page.
- **Simple API**: Use the same variable names across pages without conflicts.
- **Streamlit-friendly**: Fully compatible with Streamlit’s rerun behavior.

---

## License

This package is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

---

### Notes:
- **Installation**: To install `pgss`, you can use the Python package manager `pip`.
- **Usage**: The example provided demonstrates how to create a page-specific session state, set default values, and update the state based on user interaction.

