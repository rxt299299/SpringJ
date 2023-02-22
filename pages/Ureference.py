import streamlit as st

st.set_page_config(page_title="SpringOptimalApp", layout="wide")  # centered

with open("style/style_test.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


import pandas as pd

st.title("Srping Common Materials Reference")
st.sidebar.header("SpringJ")
st.sidebar.image("images/logo.png", use_column_width=True)

#general materials table
general_materials_path = 'docs/general_materials.csv'
df_general = pd.read_csv(general_materials_path)
#Aluminum table
Aluminum_path = 'docs/Aluminum.csv'
df_Aluminum = pd.read_csv(Aluminum_path)
#steel table
steel_path = 'docs/steel.csv'
df_steel = pd.read_csv(steel_path)
#CarbonSteel table
CarbonSteel_path = 'docs/CarbonSteel.csv'
df_CarbonSteel = pd.read_csv(CarbonSteel_path)
#StainlessSteel table
StainlessSteel_path = 'docs/StainlessSteel.csv'
df_StainlessSteel = pd.read_csv(StainlessSteel_path)
#Copper table
Copper_path = 'docs/Copper.csv'
df_Copper = pd.read_csv(Copper_path)
#nitinol table
nitinol_path = 'docs/nitinol.csv'
df_nitinol = pd.read_csv(nitinol_path)
#TitaniumAlloy table
TitaniumAlloy_path = 'docs/TitaniumAlloy.csv'
df_TitaniumAlloy = pd.read_csv(TitaniumAlloy_path)

st.write("It's important to note that these values are \
            approximate and may vary depending on the specific \
            application and requirements. The choice of which aluminum material \
            to use for a spring should be based on the specific needs of the application.")

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["General", "Aluminum Alloy", "Steel", "Carbon Steel", 
                      "Stainless Steel", "Copper and its alloys", "Nickel-titanium alloy", "Titanium alloy"])

tab1.subheader("General Materials")
tab1.table(df_general)

tab2.subheader("Aluminum Alloy")
tab2.write(df_Aluminum)

tab3.subheader("Steel")
tab3.write(df_steel)

tab4.subheader("Carbon Steel")
tab4.write(df_CarbonSteel)

tab5.subheader("Stainless Steel")
tab5.write(df_StainlessSteel)

tab6.subheader("Copper and its Alloys")
tab6.write(df_Copper)

tab7.subheader("Nickel-titanium Alloy")
tab7.write(df_nitinol)

tab8.subheader("Titanium Alloy")
tab8.write(df_TitaniumAlloy)

