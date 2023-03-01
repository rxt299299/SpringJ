import streamlit as st

st.set_page_config(page_title="SpringOptimalApp", layout="wide")  # centered

with open("style/style_test.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

from streamlit_lottie import st_lottie
from stutils import *
from stconstant import *
from streamlit_extras.switch_page_button import switch_page

#####################################
##########Initialize#################
#####################################
constraint_infos = {}
#####################################
#####################################
#####################################


st.title("Optimal Helical Compression Srping Design")
st.sidebar.header("SpringJ")
st.sidebar.image("images/logo.png", use_column_width=True)

# Header layout
col_start1, col_start2, col_start3, col_start4, col_start5 = st.columns(
    header_layout_range
)

# lottie_spring_animation_loop
with st.container():
    with col_start1:
        st_lottie(lottie_spring_animation_loop, height=120, key="coding")
    with col_start2:
        st.subheader("Select Constraints")

col1, space1, col2, space2, col3, space3, col4 = st.columns(
    [0.5, 0.2, 0.5, 0.2, 1, 0.2, 1]
)

# Outer Diameter
with st.container():
    with col1:
        st.write("Select constraints")
    with col2:
        st.write("Max or Min")
    with col3:
        st.write("Select Threshold")

# Outer Diameter
with st.container():
    with col1:
        checkbox_d_o = st.checkbox("Outer Diameter")
        blank1()
    with col2:
        if checkbox_d_o:
            d_o_design_option = st.selectbox("Outer Diameter", MaxOrMin,)
    with col3:
        if checkbox_d_o and d_o_design_option == "Max":

            threshold_d_o = numer_input_generate(
                "Outer Diameter Max", constraint_constant, "d_o"
            )
            constraint_infos["outerDiamMax"] = threshold_d_o
        elif checkbox_d_o and d_o_design_option == "Min":
            threshold_d_o = numer_input_generate(
                "Outer Diameter Min", constraint_constant, "d_o"
            )
            constraint_infos["outerDiamMin"] = threshold_d_o

# Inner Diameter
with st.container():
    with col1:
        checkbox_d_i = st.checkbox("Inner Diameter")
        blank1()
    with col2:
        if checkbox_d_i:
            d_i_design_option = st.selectbox("Inner Diameter", MaxOrMin,)
    with col3:
        if checkbox_d_i:
            if d_i_design_option == "Max":
                threshold_d_i = numer_input_generate(
                    "Inner Diameter Max", constraint_constant, "d_i"
                )
                constraint_infos["InnerDiamMax"] = threshold_d_i
            elif d_i_design_option == "Min":
                threshold_d_i = numer_input_generate(
                    "Inner Diameter Min", constraint_constant, "d_i"
                )
                constraint_infos["InnerDiamMin"] = threshold_d_i


# Maximum Shear Stress
with st.container():
    with col1:
        checkbox_maximum_shear_stress = st.checkbox("Maximum Shear Stress")
        blank1()
    with col2:
        if checkbox_maximum_shear_stress:
            maximum_shear_stress_design_option = st.selectbox(
                "Maximum Shear Stress", MaxOrMin,
            )
    with col3:
        if checkbox_maximum_shear_stress:
            if maximum_shear_stress_design_option == "Max":
                threshold_maximum_shear_stress = numer_input_generate(
                    "Maximum Shear Stress Max",
                    constraint_constant,
                    "MaximumShearStressMax",
                )
                constraint_infos[
                    "MaximumShearStressMax"
                ] = threshold_maximum_shear_stress
            elif maximum_shear_stress_design_option == "Min":
                threshold_maximum_shear_stress = numer_input_generate(
                    "Maximum Shear Stress Min",
                    constraint_constant,
                    "MaximumShearStressMax",
                )
                constraint_infos[
                    "MaximumShearStressMin"
                ] = threshold_maximum_shear_stress

# CoilBindingGap
with st.container():
    with col1:
        checkbox_coil_binding_gap = st.checkbox("Coil Binding Gap")
        blank1()
    with col2:
        if checkbox_coil_binding_gap:
            coil_binding_gap_design_option = st.selectbox("Coil Binding Gap", MaxOrMin,)
    with col3:
        if checkbox_coil_binding_gap:
            if coil_binding_gap_design_option == "Max":
                threshold_coil_binding_gap = numer_input_generate(
                    "Coil Binding Gap Max", constraint_constant, "CoilBindingGap"
                )
                constraint_infos["CoilBindingGapMax"] = threshold_coil_binding_gap
            elif coil_binding_gap_design_option == "Min":
                threshold_coil_binding_gap = numer_input_generate(
                    "Coil Binding Gap Min", constraint_constant, "CoilBindingGap"
                )
                constraint_infos["CoilBindingGapMin"] = threshold_coil_binding_gap

# Spring Rate
with st.container():
    with col1:
        checkbox_spring_rate = st.checkbox("Spring Rate")
        blank1()
    with col2:
        if checkbox_spring_rate:
            spring_rate_design_option = st.selectbox("Spring Rate", MaxOrMin,)
    with col3:
        if checkbox_spring_rate:
            if spring_rate_design_option == "Max":

                threshold_spring_rate = numer_input_generate(
                    "Spring Rate Max", constraint_constant, "SpringRate"
                )
                constraint_infos["SpringRateMax"] = threshold_spring_rate
            elif spring_rate_design_option == "Min":
                threshold_spring_rate = numer_input_generate(
                    "Spring Rate Min", constraint_constant, "SpringRate"
                )
                constraint_infos["SpringRateMin"] = threshold_spring_rate

# Spring index
with st.container():
    with col1:
        checkbox_spring_index = st.checkbox("Spring Index")
        blank1()
    with col2:
        if checkbox_spring_index:
            spring_index_design_option = st.selectbox("Spring Index", MaxOrMin,)
    with col3:
        if checkbox_spring_index:
            if spring_index_design_option == "Max":
                threshold_spring_index = numer_input_generate(
                    "Spring Index Max", constraint_constant, "SpringIndex"
                )
                constraint_infos["SpringIndexMax"] = threshold_spring_index
            elif spring_index_design_option == "Min":
                threshold_spring_index = numer_input_generate(
                    "Spring Index Min", constraint_constant, "SpringIndex"
                )
                constraint_infos["SpringIndexMin"] = threshold_spring_index

# Diametral Expansion
with st.container():
    with col1:
        checkbox_diametral_expansion = st.checkbox("Diametral Expansion")
        blank1()
    with col2:
        if checkbox_diametral_expansion:
            diametral_expansion_design_option = st.selectbox(
                "Diametral Expansion", MaxOrMin,
            )
    with col3:
        if checkbox_diametral_expansion:
            if diametral_expansion_design_option == "Max":

                threshold_diametral_expansion = numer_input_generate(
                    "Diametral Expansion Max", constraint_constant, "DiametralExpansion"
                )
                constraint_infos[
                    "DiametralExpansionMax"
                ] = threshold_diametral_expansion
            elif diametral_expansion_design_option == "Min":
                threshold_diametral_expansion = numer_input_generate(
                    "Diametral Expansion Min", constraint_constant, "DiametralExpansion"
                )
                constraint_infos[
                    "DiametralExpansionMin"
                ] = threshold_diametral_expansion


# Stress Relaxation
with st.container():
    with col1:
        checkbox_stress_relaxation = st.checkbox("Stress Relaxation")
        blank1()
    with col2:
        if checkbox_stress_relaxation:
            stress_relaxation_design_option = st.selectbox(
                "Stress Relaxation", MaxOrMin,
            )
    with col3:
        if checkbox_stress_relaxation:
            if stress_relaxation_design_option == "Max":
                threshold_stress_relaxation = numer_input_generate(
                    "Stress Relaxation Max", constraint_constant, "StressRelaxation"
                )
                constraint_infos["StressRelaxationMax"] = threshold_stress_relaxation
            elif stress_relaxation_design_option == "Min":
                threshold_stress_relaxation = numer_input_generate(
                    "Stress Relaxation Min", constraint_constant, "StressRelaxation"
                )
                constraint_infos["StressRelaxationMin"] = threshold_stress_relaxation


# Preload Force
with st.container():
    with col1:
        checkbox_preload_force = st.checkbox("Preload Force")
        blank1()
    with col2:
        if checkbox_preload_force:
            preload_force_design_option = st.selectbox("Preload Force", MaxOrMin,)
    with col3:
        if checkbox_preload_force:
            if preload_force_design_option == "Max":
                threshold_preload_force = numer_input_generate(
                    "Preload Force Max", constraint_constant, "PreloadForce"
                )
                constraint_infos["PreloadForceMax"] = threshold_preload_force
            elif preload_force_design_option == "Min":
                threshold_preload_force = numer_input_generate(
                    "Preload Force Min", constraint_constant, "PreloadForce"
                )
                constraint_infos["PreloadForceMin"] = threshold_preload_force

# Buckling Slenderness Ratio
with st.container():
    with col1:
        checkbox_buckling_slenderness_ratio = st.checkbox("Buckling Slenderness Ratio")
        blank1()
    with col2:
        if checkbox_buckling_slenderness_ratio:
            buckling_slenderness_ratio_design_option = st.selectbox(
                "Buckling Slenderness Ratio", MaxOrMin,
            )
    with col3:
        if checkbox_buckling_slenderness_ratio:
            if buckling_slenderness_ratio_design_option == "Max":
                threshold_buckling_slenderness_ratio = numer_input_generate(
                    "Buckling Slenderness Ratio Max",
                    constraint_constant,
                    "BucklingSlendernessRatio",
                )
                constraint_infos[
                    "BucklingSlendernessRatioMax"
                ] = threshold_buckling_slenderness_ratio
            elif buckling_slenderness_ratio_design_option == "Min":

                threshold_buckling_slenderness_ratio = numer_input_generate(
                    "Buckling Slenderness Ratio Min",
                    constraint_constant,
                    "BucklingSlendernessRatio",
                )
                constraint_infos[
                    "BucklingSlendernessRatioMin"
                ] = threshold_buckling_slenderness_ratio

with st.container():
    with col_start3:
        Review = st.button("Review")
    with col_start4:
        Next = st.button("Next")
    with col_start5:
        Clear_Parameters = st.button("Reset")


st.session_state["constraint_infos"] = constraint_infos

df_list = []
for key_ in constraint_infos.keys():
    df_list.append((key_, constraint_infos[key_]))


if Review:
    with col4:
        df = generate_df(df_list, ("variables", "range"))
        st.table(df)

if Next:
    switch_page("Step4_optimize")
if Clear_Parameters:
    st.session_state["constraint_infos"] = {}
