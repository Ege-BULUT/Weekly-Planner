import streamlit as st
st.set_page_config(layout="wide")
from util import todo_list


# Constants

layout = {"upper":["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "lower": ["Saturday", "Sunday", "Week", "Month", "Year"]}


st.title("Weekly Planner v:0.0.1")

# layout:
# [md][td][wd][thd][fd]
# [std][sd][w][m][y]

def main():
    days_col, extra_col = st.columns([6,1])
    container_upper = days_col.container(border=True)
    container_lower = days_col.container(border=True)
    
    with extra_col.container(border=True):
        st.subheader("Extra Column", divider="blue", )
    with container_upper:
        st.subheader("Container Upper", divider="blue")
    with container_lower:
        st.subheader("Container Lower", divider="blue")
    
    cols_upper = container_upper.columns(len(layout["upper"]))
    cols_lower = container_lower.columns(len(layout["lower"]))
    
    for i, col  in enumerate(cols_upper):
        title = layout["upper"][i]
        todo_list({},title=title,divider=True, container=col)
    for i, col in enumerate(cols_lower):
        title = layout["lower"][i]
        todo_list({},title=title,divider=True, container=col)
        



main()

