import streamlit as st
from streamlit_extras.grid import grid 
from random import randint

def random_key(min=-100000, max=100000):
    return str(randint(min, max))

def todo_list2(items, container=st.empty(), isEditable=True, title=None, title_divider=None, title_color=None, second_divider=None):
    if title:
        if title_color:
            title = ":" + title_color + "["+title+"]"
        container.subheader(title, divider=title_divider)
    
    if len(items) > 0:
        if type(items) is list and type(items[0]) is not dict:
            temp_items = []
            for item in items:
                temp_items.append({"key":item, "val":item})
            items = temp_items
        
        # check keys
        set_of_keys = set([k["key"] for k in items])
        if len(set_of_keys) < len(items): # key duplication...
            st.write("ITEM DUPLICATION DETECTED !!")
            for i, item in enumerate(items):
                item["key"] = item["key"] + "_" + str(i)
                
        if type(items) is list and type(items[0]) is dict:
            for item in items:
                #c_check, c_val = container.columns([1,6])
                item["checked"] = container.checkbox(" ", label_visibility="collapsed", key=item["key"], value=item["checked"])
                if isEditable:
                    item["val"] = container.text_input(" ", label_visibility="collapsed", value=item["val"], key=item["key"]+":"+item["val"], disabled=st.session_state[item["key"]])
                else:
                    if item["color"]:
                        rendered_item = ":" + item["color"] + "["+item["val"]+"]"
                    else:
                        rendered_item = item["val"]
                    container.write("[ "+rendered_item+" ]")
                if second_divider:
                    container.subheader("", divider=second_divider)
                
    
example = {
    "bu":True,
    "bir":False,
    "testtir":False
}

#todo_list(example, show_total=True)
#st.write(st.session_state)