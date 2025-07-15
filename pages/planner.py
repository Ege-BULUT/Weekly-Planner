import streamlit as st
st.set_page_config(layout="wide")
from util import todo_list2


# Constants
options = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Weekly", "Monthly", "Yearly"]
ss = {
    "layout" : {"upper":["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "lower": ["Saturday", "Sunday", "Weekly", "Monthly", "Yearly"]},

    "todo_items" : {
        "Monday":[{"key":"Monday",       "val":"item", "color":None, "checked":False,}],
        "Tuesday":[{"key":"Tuesday",     "val":"item", "color":None, "checked":False,}],
        "Wednesday":[{"key":"Wednesday", "val":"item", "color":None, "checked":False,}],
        "Thursday":[{"key":"Thursday",   "val":"item", "color":None, "checked":False,}],
        "Friday":[{"key":"Friday",       "val":"item", "color":None, "checked":False,}],
        "Saturday":[{"key":"Saturday",   "val":"item", "color":None, "checked":False,}],
        "Sunday":[{"key":"Sunday",       "val":"item", "color":None, "checked":False,}],
        "Weekly":[{"key":"Weekly",       "val":"item", "color":None, "checked":False,}],
        "Monthly":[{"key":"Monthly",     "val":"item", "color":None, "checked":False,}],
        "Yearly":[{"key":"Yearly",       "val":"item", "color":None, "checked":False,}]
    }
}

for key, val in ss.items():
    if key not in st.session_state.keys():
        st.session_state[key] = val
layout = st.session_state["layout"]
todo_items = st.session_state["todo_items"]

def ss_update():
    global layout, todo_items
    layout = st.session_state["layout"]
    todo_items = st.session_state["todo_items"]
    

st.title("Weekly Planner v:0.0.1")

# layout:
# [md][td][wd][thd][fd]
# [std][sd][w][m][y]

@st.dialog("Remove Tasks")
def remove_task():
    program = st.select_slider("Pick a time", options=options)
    selected_task_indexes=[]
    but1, but2 = st.columns(2)
    for i, task in enumerate(st.session_state["todo_items"][program]):
            c_check, c_val = st.columns([1,5])
            selected = c_check.checkbox("", label_visibility="collapsed", key=task["val"])
            if task["color"]:
                render_text = ":" + task["color"] + "[" + task["val"] + "]"
            else:
                render_text = task["val"]
            c_val.write(render_text)
            if selected:
                selected_task_indexes.append(i)
            else:
                try:
                    selected_task_indexes.remove(i)
                except Exception as e:
                    pass
    if but1.button("Remove All!"):
        st.session_state["todo_items"][program] = []
        st.toast("Tasks removed successfuly!")
        ss_update()
        st.rerun()

    if but2.button("Remove Selected!"):
        for i in selected_task_indexes:
            st.session_state["todo_items"][program].pop(i)
            st.toast("Task removed successfuly!")
        ss_update()
        st.rerun()

@st.dialog("Add New Task")
def add_task():
    program = st.select_slider("Pick a time", options=options)
    val = st.text_input(" ", placeholder="Task Details", label_visibility="collapsed")
    checked = st.checkbox("Completed?")
    color = st.selectbox("color", ["orange", "green", "blue", "red", "grey", "rainbow"]) if st.checkbox("Important?") else None
    if st.button("Add!"):
        st.session_state["todo_items"][program].append({"key":val, "val":val, "color":color, "checked":checked})
        ss_update()
        st.toast("Task added successfuly!")
        st.rerun()

def main():
    days_col, extra_col = st.columns([6,1])
    container_upper = days_col.container(border=True)
    container_lower = days_col.container(border=True)
    
    with extra_col.container(border=True):
        st.subheader("Extra Column", divider="blue", )
        
        editable = st.toggle("Edit Items", value=True)
        if st.button("Add Task"):
            add_task()            
        if st.button("Remove Task"):
            remove_task()
        
    with container_upper:
        st.subheader("Container Upper", divider="blue")
    
    
    with container_lower:
        st.subheader("Container Lower", divider="blue")
    
    cols_upper = container_upper.columns(len(layout["upper"]))
    cols_lower = container_lower.columns(len(layout["lower"]))
    
    for i, col  in enumerate(cols_upper):
        title = layout["upper"][i]
        todo_list2(title=title, items=todo_items[layout["upper"][i]], isEditable=editable, container=col, title_color="green", title_divider="green", second_divider="grey")
    for i, col in enumerate(cols_lower):
        title = layout["lower"][i]
        todo_list2(title=title, items=todo_items[layout["lower"][i]], isEditable=editable, container=col, title_color="blue", title_divider="blue", second_divider="grey")

main()