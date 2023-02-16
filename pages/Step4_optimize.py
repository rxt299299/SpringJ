import streamlit as st

st.set_page_config(page_title="SpringOptimalApp", layout="wide")  # centered

with open("style/style_test.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

from streamlit_lottie import st_lottie
from stutils import *
from stconstant import *
from streamlit_extras.switch_page_button import switch_page


from SpringDesign.spring_design import *
from Scipydirect.scipydirect import minimize
import plotly.express as px
import pandas as pd
import time


#####################################
##########Load the parameters########
#####################################
# input parameters from inputs page
input_dict = initial_input_dict("input_dict")
bounds_inputs = initial_input_dict("design_variables_range")
constraint_policy = initial_input_dict("constraint_infos")
#####################################
#####################################
#####################################

input_dict = {
    'end_closed':True,
    'L_free':85.5,
    'L_hard':20,
    'G':77,
    'Poisson_ratio': 0.3,
}

constraint_policy = {
    'outerDiamMax':60,
    'MaximumShearStressMax': 0.7,
    'CoilBindingGapMin': 0.5
}  

bounds_inputs = {'d_i':[20, 30], 'd_w':[1, 5], 'N_t':[9, 17]}
#2d example
# input_dict = {
#     'end_closed':True,
#     'L_free':85.5,
#     'L_hard':20,
#     'G':77,
#     'Poisson_ratio': 0.3,
#     'N_t':9,
# }
# bounds_inputs = {'d_i':[20, 30], 'd_w':[1, 5]}

objective = {"spring_rate_spring_index": {"MaxorMin": "min", "k_max": 20, "c_max": 10}}

# set the spring class
sping_1 = Spring(input_dict, constraint_policy, objective)

feasible_arr, feasible_arr_steps = sping_1.Feasibility(bounds_inputs)

st.title("SpringJ: Optimal Helical Compression Srping Design")
# Header layout
col_start1, col_start2, col_start3, col_start4, col_start5 = st.columns(
    header_layout_range
)

# lottie_spring_animation_loop
with st.container():
    with col_start1:
        st_lottie(lottie_spring_animation_loop, height=120, key="coding")#well_done_fig
    with col_start2:
        st.subheader("We only support Spring Rate and Index optimize now")


Num_constraints = len(constraint_policy)
constraint_cols = st.columns([1] * Num_constraints)
with st.container():
    for i in range(len(constraint_cols)):
        with constraint_cols[i]:
            fig = scatter_plot(i, feasible_arr_steps, bounds_inputs)
            st.plotly_chart(fig, use_container_width=True, theme="streamlit")



col_res1, col_res2, col_res3 = st.columns([1,1.5,1])
if len(feasible_arr)>0:
    with st.container():
        with col_res2:
            st.subheader("You have passed the Feasibilities test!")
            time.sleep(1.2)
            st.subheader("Start optimize the design variables")

        with col_res2:
            bounds = np.array(list(bounds_inputs.values()))

            res = minimize(sping_1.ConstraintsForOptimize, bounds=bounds)
            df = pd.DataFrame(zip(list(bounds_inputs.keys()), res.x), columns=['variable', 'optimal_value'])
            #df = pd.DataFrame(zip(list(bounds_inputs.keys()), [22, 1.5, 9]), columns=['variable', 'optimal_value'])
            st.table(df)
        with col_res3:
            st_lottie(well_done_fig, height=120, key="well_done")#well_done_fig
