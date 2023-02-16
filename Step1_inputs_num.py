import streamlit as st

st.set_page_config(page_title="SpringOptimalApp", layout="wide")  # centered
with open("style/style_test.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


from streamlit_lottie import st_lottie
from stutils import *
from stconstant import *
from streamlit_extras.switch_page_button import switch_page

st.title("SpringJ: Optimal Helical Compression Srping Design")

#####################################
##########Initialize#################
#####################################
# initial the input parameters dictionary
input_dict = {"end_closed": False}
#####################################
#####################################
#####################################

# Header layout
col_start1, col_start2, col_start3, col_start4, col_start5 = st.columns(
    header_layout_range
)
# lottie_spring_animation_loop
with st.container():
    with col_start1:
        st_lottie(lottie_spring_animation_loop, height=120, key="coding")

with st.container():
    with col_start2:
        st.subheader("Please select the Input Parameters")

        # 是否闭合这个必须要选
        input_end_closed = st.checkbox("If End Closed (Must decide if select)")

        if input_end_closed:
            input_dict["end_closed"] = True
        else:
            input_dict["end_closed"] = False

st.write("##")


# main layout
col1, space1, col2, space2, col3 = st.columns([1, 0.2, 1, 0.2, 1])

# Diameters and Coils
with st.container():
    with col1:
        Diameter_input_option = st.selectbox(
            "Wire/Inner/Outer Diameter",
            (
                "No Input",
                "Only Wire",
                "Only Inner",
                "Only Outer",
                "Wire & Inner",
                "Wire & Outer",
                "Inner & Outer",
            ),
        )
        blank1()
        Coils_input_option = st.selectbox(
            "Total/Active Coils",
            (
                "No Input",
                "Total Coils",
                "Active Coils",
            ),
        )

        if Diameter_input_option == "No Input":
            pass
        elif Diameter_input_option == "Only Wire":
            input_d_w = numer_input_generate("Wire Diameter", inputs_constant, "d_w")
            input_dict["d_w"] = input_d_w

        elif Diameter_input_option == "Only Inner":
            input_d_i = numer_input_generate("Inner Diameter", inputs_constant, "d_i")
            input_dict["d_i"] = input_d_i

        elif Diameter_input_option == "Only Outer":
            input_d_o = numer_input_generate("Outer Diameter", inputs_constant, "d_o")
            input_dict["d_o"] = input_d_o

        elif Diameter_input_option == "Wire & Inner":
            input_d_w = numer_input_generate("Wire Diameter", inputs_constant, "d_w")
            input_d_i = numer_input_generate("Inner Diameter", inputs_constant, "d_i")
            if input_d_w >= input_d_i:
                st.error("Wire Diameter could not larger than Inner Diameter", icon="🚨")
            input_dict["d_w"] = input_d_w
            input_dict["d_i"] = input_d_i
            input_dict["d_o"] = input_d_i + 2 * input_d_w
        elif Diameter_input_option == "Wire & Outer":
            input_d_w = numer_input_generate("Wire Diameter", inputs_constant, "d_w")
            input_d_o = numer_input_generate("Outer Diameter", inputs_constant, "d_o")
            if input_d_w >= input_d_o:
                st.error("Wire Diameter could not larger than Outer Diameter", icon="🚨")
            input_dict["d_w"] = input_d_w
            input_dict["d_o"] = input_d_o
            input_dict["d_i"] = input_d_o - 2 * input_d_w
        elif Diameter_input_option == "Inner & Outer":
            input_d_i = numer_input_generate("Inner Diameter", inputs_constant, "d_i")
            input_d_o = numer_input_generate("Outer Diameter", inputs_constant, "d_o")
            if input_d_i >= input_d_o:
                st.error(
                    "Inner Diameter could not larger than Outer Diameter", icon="🚨"
                )
            input_dict["d_i"] = input_d_i
            input_dict["d_o"] = input_d_o
            input_dict["d_w"] = (input_d_o - input_d_i) / 2

        blank1()

        if Coils_input_option == "No Input":
            pass
        elif Coils_input_option == "Total Coils":
            input_total_coils = numer_input_generate("Total Coils", inputs_constant, "N_t")
            input_dict["N_t"] = input_total_coils

            if input_end_closed:
                input_dict["N_a"] = input_dict["N_t"] - 2
            else:
                input_dict["N_a"] = input_dict["N_t"] - 1

        elif Coils_input_option == "Active Coils":
            input_active_coils = numer_input_generate("Active Coils", inputs_constant, "N_a")
            input_dict["N_a"] = input_active_coils

            if input_end_closed:
                input_dict["N_t"] = input_dict["N_a"] + 2
            else:
                input_dict["N_t"] = input_dict["N_a"] + 1


other_parameters_name_dict = [
    ("Free Length", "L_free"),
    ("Open Length", "L_open"),
    ("Hard Length", "L_hard"),
    ("Deflection", "deflection"),
    ("Poisson Ratio", "Poisson_ratio"),
    ("Shear Modulus", "G"),
    ("Norton Bailey c", "NB_c"),
    ("Norton Bailey n", "NB_n"),
    ("Norton Bailey k", "NB_k"),
    ("Stress Relaxation Gsr", "Gsr"),
]
# other parameters
with st.container():
    with col2:
        options = st.multiselect(
            "Select input parameters",
            [
                "Free Length",
                "Open Length",
                "Hard Length",
                "Deflection",
                "Poisson Ratio",
                "Shear Modulus",
                "Norton Bailey c",
                "Norton Bailey n",
                "Norton Bailey k",
                "Stress Relaxation Gsr",
            ],
            [],
        )

        for name in other_parameters_name_dict:
            slider_name, key_ = name
            if slider_name in options:
                input_value = numer_input_generate(slider_name, inputs_constant, key_)
                input_dict[key_] = input_value

        # Logic among L_free, L_open and L_hard
        if "L_free" in input_dict.keys() and "L_open" in input_dict.keys():
            report_error_compare(
                input_dict["L_free"], input_dict["L_open"], ("L_free", "L_open")
            )

        if "L_free" in input_dict.keys() and "L_hard" in input_dict.keys():
            report_error_compare(
                input_dict["L_free"], input_dict["L_hard"], ("L_free", "L_hard")
            )

        if "L_open" in input_dict.keys() and "L_hard" in input_dict.keys():
            report_error_compare(
                input_dict["L_open"], input_dict["L_hard"], ("L_open", "L_hard")
            )

# Buttons
with st.container():
    with col_start3:
        Review = st.button("Review")
    with col_start4:
        Next = st.button("Next")
    with col_start5:
        Clear_Parameters = st.button("Reset")

st.session_state["input_dict"] = input_dict


# Review table
df_list = []
for key_ in input_dict.keys():
    df_list.append((parameter_names_mapping[key_], input_dict[key_]))


if Review:
    with col3:
        df = generate_df(df_list, ("parameter", "value"))
        st.table(df)
if Next:
    switch_page("Step2_design_num")
if Clear_Parameters:
    st.session_state["input_dict"] = {}
