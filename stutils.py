import json
import streamlit as st
import pandas as pd
import plotly.express as px


def numer_input_generate(show_name, config_dict, key_):
    return st.number_input(
        show_name,
        min_value=config_dict[key_][0],
        max_value=config_dict[key_][1],
        value=config_dict[key_][2],
    )


def number_input_start_generate(show_name, config_dict, key_):
    start_ = st.number_input(
        show_name + " Start",
        min_value=config_dict[key_]["options"][0],
        max_value=config_dict[key_]["options"][1],
        value=config_dict[key_]["value"][0],
    )

    return start_


def number_input_end_generate(show_name, config_dict, key_):
    end_ = st.number_input(
        show_name + " End",
        min_value=config_dict[key_]["options"][0],
        max_value=config_dict[key_]["options"][1],
        value=config_dict[key_]["value"][1],
    )

    return end_


def slider_generate(show_name, config_dict, key_):
    return st.slider(
        show_name,
        config_dict[key_][0],
        config_dict[key_][1],
        config_dict[key_][2],
        disabled=False,
    )


def select_slider_generate(slider_name, config_dict, key_):
    return st.select_slider(
        slider_name,
        options=config_dict[key_]["options"],
        value=config_dict[key_]["value"],
    )


def generate_df(df_list, column_names):
    df = pd.DataFrame(df_list, columns=column_names)
    return df


def list_dict_keys(dict_):
    return list(dict_.keys())


def initial_input_dict(dict_name):
    if dict_name in st.session_state:
        return st.session_state[dict_name]
    return {}


# functions
def load_lottie_json(json_file):
    # Opening JSON file
    f = open(json_file, encoding="utf8")

    return json.load(f)


# use local css
def load_css(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def blank3():
    st.write("##")
    st.write("##")
    st.write("##")


def blank1():
    st.write("#")


def blank2():
    st.write("#")
    st.write("#")


def report_error_compare(value1, value2, value_names):
    if value1 < value2:
        st.error(value_names[0] + " must be larger than " + value_names[1], icon="🚨")


def design_diameter_coils(available_design_variables):
    if "N_a" in available_design_variables and "N_t" in available_design_variables:
        return (
            "No design",
            "Total Coils",
            "Active Coils",
        )
    return None


def design_diameter_options(available_design_variables):
    # default 是否display
    # d_w,d_i,d_o都没有inputs输入
    if (
        "d_w" in available_design_variables
        and "d_i" in available_design_variables
        and "d_o" in available_design_variables
    ):
        return (
            "No design",
            "Wire & Inner",
            "Wire & Outer",
            "Inner & Outer",
        )
    # d_o 有输入
    elif "d_w" in available_design_variables and "d_i" in available_design_variables:
        return (
            "No design",
            "Wire",
            "Inner",
        )
    # d_i 有输入, 这个时候，让d_w可作为design variables
    elif "d_w" in available_design_variables and "d_o" in available_design_variables:
        return (
            "No design",
            "Wire",
            "Outer",
        )
    # d_w 有输入, 这个时候，让d_i可作为design variables
    elif "d_i" in available_design_variables and "d_o" in available_design_variables:
        return (
            "No design",
            "Inner",
            "Outer",
        )
    return None


def scatter_plot(idx, feasible_arr_steps, bounds_inputs):
    constraint_name, feasible_arr = feasible_arr_steps[idx]
    feasible_arr = pd.DataFrame(feasible_arr, columns=list(bounds_inputs.keys()))

    if len(bounds_inputs.keys()) >= 3:
        top3_keys = list(bounds_inputs.keys())[:3]

        feasible_arr = feasible_arr[top3_keys]
        fig = px.scatter_3d(
            feasible_arr,
            x=top3_keys[0],
            y=top3_keys[1],
            z=top3_keys[2],
            title=constraint_name,
            opacity=0.4,
            size_max=5,
        )
    elif len(bounds_inputs.keys()) == 2:
        top2_keys = list(bounds_inputs.keys())[:2]

        feasible_arr = feasible_arr[top2_keys]
        fig = px.scatter(
            feasible_arr,
            x=top2_keys[0],
            y=top2_keys[1],
            title=constraint_name,
            opacity=0.4,
            size_max=5,
        )
    else:
        return None

    return fig


"""
#各个input的输入例子

input_parameters = {
    'end_closed':True,
    'L_free':85.5,
    'L_hard':20,
    'G':77,
    'Poisson_ratio': 0.3,
}

constraint_policy = {
    'outerDiamMax':60,
    'MaximumShearStressMax': 0.7,
    'CoilBindingGapMin': 0.5,
    'BucklingSlendernessRatioMax': (True, 3.705), #if_use_Poisson_ratio, value if not use Poisson_ratio
    'DiametralExpansionMax': 35,
}        

objective = {
    'spring_rate_spring_index': {'MaxorMin':'min', 'k_max': 20, 'c_max':10}
}

"""
