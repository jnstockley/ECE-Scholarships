'''
Script editor component used for the import page merge similar columns form.
'''
from streamlit_ace import st_ace
import streamlit as st

from managers.import_data.similar_columns import StatusMessage

SCRIPT_DEFAULT_TEXT = """def merge(row):
    '''
    Takes a row data (ndarray) and will merge several columns together
    into a single value.

    Inputs
    ------
    row : np.ndarray
        Can be indexed with any of the columns selected above (ex: row["Column Name"])
    
    Returns
    -------
    any
        The FINAL COLUMN value
    '''

    return None
"""

def render_script_expander(form, similar_details):
    '''
    Renders the script expander onto the merge similar columns view
    '''
    # Custom script editor
    with form.expander("Create Custom Merge Script (ADVANCED)"):
        custom_script = st_ace(SCRIPT_DEFAULT_TEXT, auto_update=True, language="python")
        st.write("Make changes to the function below and then press apply. The function will be run on each row and the value returned is what will appear in the FINAL COLUMN value.")

        apply_col, reset_col, _blank = st.columns([2,2,10])
        with apply_col:
            apply_script = st.form_submit_button('apply')
        with reset_col:
            reset_script = st.form_submit_button('reset')

        if StatusMessage.CUSTOM_SCRIPT in similar_details.status_messages:
            st.write(similar_details.status_messages[StatusMessage.CUSTOM_SCRIPT])

    if apply_script:
        similar_details.apply_custom_merge_script(custom_script)
    elif reset_script:
        similar_details.reset_custom_merge_script()
