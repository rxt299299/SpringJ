import streamlit as st

st.set_page_config(page_title="SpringOptimalApp", layout="wide")  # centered
with open("style/style_test.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

from streamlit_lottie import st_lottie
from stutils import *
from stconstant import *
from streamlit_extras.switch_page_button import switch_page


# design_measurement_variables = [
#     "N_t",
#     "N_a",
#     "d_i",
#     "d_w",
#     "d_o",
#     "G",
#     "L_free",
#     "L_open",
#     "L_hard",
# ]


#####################################
##########Load the parameters########
#####################################
# input parameters from inputs page
input_dict = initial_input_dict("input_dict")
known_parameters_keys = list_dict_keys(input_dict)

# variables available to design
available_design_variables = [
    item for item in design_measurement_variables if item not in known_parameters_keys
]
diameter_options = design_diameter_options(available_design_variables)
coils_options = design_diameter_coils(available_design_variables)

# initilize the dictionary to save design variables and their ranges
design_variables_range = {}
#####################################
#####################################
#####################################
design_mappings = {
    "L_free": "Free Length",
    "L_open": "Open Length",
    "L_hard": "Hard Length",
    "G": "Shear Modulus",
}


st.title("SpringJ: Optimal Helical Compression Srping Design")
# Header layout
col_start1, col_start2, col_start3, col_start4, col_start5 = st.columns(
    header_layout_range
)

# lottie_spring_animation_loop
with st.container():
    with col_start1:
        st_lottie(lottie_spring_animation_loop, height=120, key="coding")
    with col_start2:
        st.subheader("Select range for design Variables")


# main layout
col1, space1, col2_1, col2_2, space2, col3 = st.columns([1, 0.2, 0.5, 0.5, 0.2, 1])

# Diameter and Coils
with st.container():
    with col1:
        if diameter_options is not None:
            Diameter_design_option = st.selectbox(
                "Wire/Inner/Outer Diameter",
                diameter_options,
            )
            blank1()
        if coils_options is not None:
            Coils_design_option = st.selectbox(
                "Total & Active Coils",
                coils_options,
            )
            blank1()

        multi_selects = [
            item
            for item in available_design_variables
            if item in ["L_free", "L_open", "L_hard", "G"]
        ]
        multi_options = [design_mappings[item] for item in multi_selects]
        other_options = st.multiselect(
            "Select more design variables", multi_options, []
        )
    

    if diameter_options is not None:
        # Wire/Inner/Outer Diameter
        if Diameter_design_option == "Wire":
            with col2_1:
                start_d_w = number_input_start_generate(
                    "Wire Diameter Range", design_constant_input_num, "d_w"
                )
            with col2_2:
                end_d_w = number_input_end_generate(
                    "Wire Diameter Range", design_constant_input_num, "d_w"
                )
                design_variables_range["d_w"] = [start_d_w, end_d_w]

        elif Diameter_design_option == "Inner":
            with col2_1:
                start_d_i = number_input_start_generate(
                    "Inner Diameter Range", design_constant_input_num, "d_i"
                )
            with col2_2:
                end_d_i = number_input_end_generate(
                    "Inner Diameter Range", design_constant_input_num, "d_i"
                )
                design_variables_range["d_i"] = [start_d_i, end_d_i]
        elif Diameter_design_option == "Outer":
            with col2_1:
                start_d_o = number_input_start_generate(
                    "Outer Diameter Range", design_constant_input_num, "d_o"
                )
            with col2_2:
                end_d_o = number_input_end_generate(
                    "Outer Diameter Range", design_constant_input_num, "d_o"
                )
                design_variables_range["d_o"] = [start_d_o, end_d_o]
        elif Diameter_design_option == "Wire & Inner":
            with col2_1:
                start_d_w = number_input_start_generate(
                    "Wire Diameter Range", design_constant_input_num, "d_w"
                )
                start_d_i = number_input_start_generate(
                    "Inner Diameter Range", design_constant_input_num, "d_i"
                )
            with col2_2:
                end_d_w = number_input_end_generate(
                        "Wire Diameter Range", design_constant_input_num, "d_w"
                    )
                end_d_i = number_input_end_generate(
                    "Inner Diameter Range", design_constant_input_num, "d_i"
                )
                design_variables_range["d_w"] = [start_d_w, end_d_w]

                design_variables_range["d_i"] = [start_d_i, end_d_i]
        elif Diameter_design_option == "Wire & Outer":
            with col2_1:
                start_d_w = number_input_start_generate(
                    "Wire Diameter Range", design_constant_input_num, "d_w"
                )
                start_d_o = number_input_start_generate(
                    "Outer Diameter Range", design_constant_input_num, "d_o"
                )
            with col2_2:
                end_d_w = number_input_end_generate(
                    "Wire Diameter Range", design_constant_input_num, "d_w"
                )
                end_d_o = number_input_end_generate(
                    "Outer Diameter Range", design_constant_input_num, "d_o"
                )             
                design_variables_range["d_w"] = [start_d_w, end_d_w]
                design_variables_range["d_o"] = [start_d_o, end_d_o]
        elif Diameter_design_option == "Inner & Outer":
            with col2_1:
                start_d_i = number_input_start_generate(
                    "Inner Diameter Range", design_constant_input_num, "d_i"
                )
                start_d_o = number_input_start_generate(
                    "Outer Diameter Range", design_constant_input_num, "d_o"
                )
            with col2_2:
                end_d_i = number_input_end_generate(
                    "Inner Diameter Range", design_constant_input_num, "d_i"
                )
                end_d_o = number_input_end_generate(
                    "Outer Diameter Range", design_constant_input_num, "d_o"
                )
                design_variables_range["d_i"] = [start_d_i, end_d_i]
                design_variables_range["d_o"] = [start_d_o, end_d_o]

    if coils_options is not None:
        # Coils
        if Coils_design_option == "Total Coils":
            with col2_1:
                start_N_t = number_input_start_generate(
                        "Total Coils Range", design_constant_input_num, "N_t"
                    )
            with col2_2:
                end_N_t = number_input_end_generate(
                        "Total Coils Range", design_constant_input_num, "N_t"
                    )
                design_variables_range["N_t"] = [start_N_t, end_N_t]
        elif Coils_design_option == "Active Coils":
            with col2_1:
                start_N_a = number_input_start_generate(
                        "Active Coils Range", design_constant_input_num, "N_a"
                    )
            with col2_2:
                end_N_a = number_input_end_generate(
                        "Active Coils Range", design_constant_input_num, "N_a"
                    )

                design_variables_range["N_a"] = [start_N_a, end_N_a]

    if "Free Length" in other_options:
        with col2_1:
            start_L_free = number_input_start_generate(
                "Free Length Range", design_constant_input_num, "L_free"
            )
        with col2_2:
            end_L_free = number_input_end_generate(
                        "Free Length Range", design_constant_input_num, "L_free"
                    )

            design_variables_range["L_free"] = [start_L_free, end_L_free]
    if "Open Length" in other_options:
        with col2_1:

            start_L_open = number_input_start_generate(
                "Open Length Range", design_constant_input_num, "L_open"
            )
        with col2_2:
            end_L_open = number_input_end_generate(
                        "Open Length Range", design_constant_input_num, "L_open"
                    )

            design_variables_range["L_open"] = [start_L_open, end_L_open]
    if "Hard Length" in other_options:
        with col2_1:
            start_L_hard = number_input_start_generate(
                "Hard Length Range", design_constant_input_num, "L_hard"
            )
        with col2_2:
            end_L_hard = number_input_end_generate(
                        "Hard Length Range", design_constant_input_num, "L_hard"
                    )
            design_variables_range["L_hard"] = [start_L_hard, end_L_hard]
    if "Shear Modulus" in other_options:
        with col2_1:
            start_G = number_input_start_generate(
                "Shear Modulus Range", design_constant_input_num, "G"
            )
        with col2_2:
            end_G = number_input_end_generate(
                        "Shear Modulus Range", design_constant_input_num, "G"
                    )
            design_variables_range["G"] = [start_G, end_G]


with st.container():
    with col_start3:
        Review = st.button("Review")
    with col_start4:
        Next = st.button("Next")
    with col_start5:
        Clear_Parameters = st.button("Reset")


st.session_state["design_variables_range"] = design_variables_range

df_list = []
for key_ in design_variables_range.keys():
    df_list.append((parameter_names_mapping[key_], design_variables_range[key_]))


if Review:
    with col3:
        df = generate_df(df_list, ("variables", "range"))
        st.table(df)

if Next:
    switch_page("Step3_constraints_num")
if Clear_Parameters:
    st.session_state["design_variables_range"] = {}
