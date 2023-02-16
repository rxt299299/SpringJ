from stutils import *
from PIL import Image

img_logo = Image.open("images/logo.png")

header_layout_range = [0.2, 1.5, 0.2, 0.2, 0.2]
# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

lottie_spring_animation_loop = load_lottie_json("jsons/spring_animation_loop.json")
well_done_fig = load_lottie_json("jsons/well_done.json")

MaxOrMin = ("Max", "Min")

parameter_names_mapping = {
    "d_w": "Wire Diameter",
    "d_i": "Inner Diameter",
    "d_o": "Outer Diameter",
    "N_t": "Total Coils",
    "N_a": "Active Coils",
    "end_closed": "End Closed",
    "Poisson_ratio": "Poisson Ratio",
    "NB_c": "Norton Bailey c",
    "NB_n": "Norton Bailey n",
    "NB_k": "Norton Bailey k",
    "Gsr": "Stress Relaxation Gsr",
    "L_free": "Free Length",
    "L_open": "Open Length",
    "L_hard": "Hard Length",
    "G": "Shear Modulus",
    "deflection": "Deflection",
}

input_parameter_names = [
    "N_t",
    "N_a",
    "d_w",
    "d_i",
    "d_o",
    "L_free",
    "L_open",
    "L_hard",
    "deflection",
    "Young",
    "Poisson_ratio",
    "G",
    "NB_c",
    "NB_n",
    "NB_k",
    "Gsr",
]

design_measurement_variables = [
    "N_t",
    "N_a",
    "d_i",
    "d_w",
    "d_o",
    "G",
    "L_free",
    "L_open",
    "L_hard",
]

inputs_constant = {
    "d_w": (0, 30, 1),
    "d_i": (0, 130, 20),
    "d_o": (0, 130, 25),
    "N_t": (20, 50, 35),
    "N_a": (20, 50, 33),
    "L_free": (20, 100, 80),
    "L_open": (20, 100, 75),
    "L_hard": (20, 100, 70),
    "G": (60, 120, 75),
    "Poisson_ratio": (0.0, 0.5, 0.33),
    "deflection": (0, 120, 25),
    "G": (0, 120, 25),
    "NB_c": (0, 120, 25),
    "NB_n": (0, 120, 25),
    "NB_k": (0, 120, 25),
    "Gsr": (0, 120, 25),
}

design_constant = {
    "d_w": {"options": range(0, 20, 1), "value": (1, 5)},
    "d_i": {"options": range(10, 30, 1), "value": (15, 25)},
    "d_o": {"options": range(20, 40, 1), "value": (25, 35)},
    "N_t": {"options": range(5, 50, 1), "value": (30, 35)},
    "N_a": {"options": range(5, 50, 1), "value": (30, 33)},
    "L_free": {"options": range(20, 130, 1), "value": (50, 90)},
    "L_open": {"options": range(20, 130, 1), "value": (40, 80)},
    "L_hard": {"options": range(20, 130, 1), "value": (35, 75)},
    "G": {"options": range(20, 130, 1), "value": (35, 75)},
}

design_constant_input_num = {
    "d_w": {"options": (0, 20), "value": (1, 5)},
    "d_i": {"options": (10, 30), "value": (15, 25)},
    "d_o": {"options": (20, 40), "value": (25, 35)},
    "N_t": {"options": (5, 50), "value": (30, 35)},
    "N_a": {"options": (5, 50), "value": (30, 33)},
    "L_free": {"options": (20, 130), "value": (50, 90)},
    "L_open": {"options": (20, 130), "value": (40, 80)},
    "L_hard": {"options": (20, 130), "value": (35, 75)},
    "G": {"options": (20, 130), "value": (35, 75)},
}

constraint_constant = {
    "d_i": (0, 130, 20),
    "d_o": (0, 130, 25),
    "CoilBindingGap": (0.0, 1.0, 0.3),
    "MaximumShearStressMax": (0.0, 1.0, 0.5),
    "SpringRate": (0, 10, 1),
    "SpringIndex": (0, 10, 1),
    "DiametralExpansion": (20, 50, 35),
    "StressRelaxation": (0, 130, 25),
    "PreloadForce": (0, 130, 25),
    "BucklingSlendernessRatio": (0, 130, 25),
}
