import streamlit as st
from random import randint

def random_key(min=-100000, max=100000):
    return str(randint(min, max))

def todo_list(elements={}, title:str="", divider=False, divider_color="gray", show_total=False, container=st.empty()):
    with container:
        total_container = st.container()
        if type(elements) is list:
            temp_elements = {}
            for elem in elements:
                temp_elements.update({elem:False})
            elements = temp_elements
        if divider:
            st.subheader(title, divider=divider_color)
        else:
            st.subheader(title)
        if "elements" not in st.session_state.keys():
            st.session_state["elements"] = elements
        #idx_counter = 0
        for elem, val in st.session_state["elements"].items():
            col_c, col_v = st.columns([1,6])
            elem = col_v.text_input(" ", label_visibility="collapsed", value=elem)
            val = col_c.checkbox(" ", label_visibility="collapsed", value=val, key=elem)
            st.session_state["elements"][elem] = val
        col_c, col_v = st.columns([1,6])
        elem_new = col_v.text_input(" ", label_visibility="collapsed", key=random_key())
        btn = col_c.button("add", key="add_button"+random_key())
        if btn:
            elements.update({elem_new:False})
            st.session_state["elements"][elem_new] = False
            st.rerun()
        if show_total:
            total_true = 0
            for elem, val in st.session_state["elements"].items():
                if val:
                    total_true += 1
            total = len(st.session_state["elements"])
            total_container.write(":green["+str(total_true)+"] / "+str(total))
    
example = {
    "bu":True,
    "bir":False,
    "testtir":False
}

#todo_list(example, show_total=True)
#st.write(st.session_state)