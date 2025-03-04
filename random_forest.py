import streamlit as st
import numpy as np
from joblib import load
import pandas as pd

if "pred" not in st.session_state:
    st.session_state["pred"] = None

@st.cache_data
def load_data():
    df = pd.read_csv('data/honda_toyota_ca.csv')
    return df

@st.cache_resource(show_spinner="Loading model...")
def load_model():
    pipe = load('model.joblib')
    return pipe

def make_prediction(pipe):
    miles = st.session_state["miles"]
    year = st.session_state["year"]
    make = st.session_state["make"]
    model = st.session_state["model"]
    trim = st.session_state["trim"]
    body_type = st.session_state["body_type"]
    engine_size = st.session_state["engine_size"]
    province = st.session_state["province"]

    X_pred = np.array([miles, year, make, model, trim, body_type, engine_size, province]).reshape(1, -1)

    pred = pipe.predict(X_pred)
    pred = round(pred[0], 2)

    st.session_state["pred"] = pred

    mae = 3900
    lower_bound = round(pred - mae, 2)
    upper_bound = round(pred + mae, 2)
    range_str = f"{lower_bound:,.2f} ~ {upper_bound:,.2f}"

    st.session_state["metrics"] = {
        "cheaper_than_market": f"{lower_bound:,.2f}",
        "normal_range": f"{range_str}",
        "expensive_than_market": f"{upper_bound:,.2f}"
    }

def format_metric_cheap(label, value):
    return f"""
    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; margin: 10px; text-align: center; background-color: grey;">
        <div style="font-size: 14px; color: green;">{label}</div>
        <div style="font-size: 20px; color: green;">{value}</div>
    </div>
    """

def format_metric_normal(label, value):
    return f"""
    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; margin: 10px; text-align: center; background-color: grey;">
        <div style="font-size: 14px; color: yellow;">{label}</div>
        <div style="font-size: 20px; color: yellow;">{value}</div>
    </div>
    """

def format_metric_expensive(label, value):
    return f"""
    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; margin: 10px; text-align: center; background-color: grey;">
        <div style="font-size: 14px; color: red;">{label}</div>
        <div style="font-size: 20px; color: red;">{value}</div>
    </div>
    """

if __name__ == "__main__":
    st.title("🍁Used car price calculator")

    pipe = load_model()

    with st.form(key="form"):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.number_input("Miles", value=86132.0, min_value=0.0, step=0.1, key="miles")
            st.selectbox("Model", index=0, key="model", options=['Prius', 'Highlander', 'Civic', 'Accord', 'Corolla', 'Ridgeline',
       'Odyssey', 'CR-V', 'Pilot', 'Camry Solara', 'Matrix', 'RAV4',
       'Rav4', 'HR-V', 'Fit', 'Yaris', 'Yaris iA', 'Tacoma', 'Camry',
       'Avalon', 'Venza', 'Sienna', 'Passport', 'Accord Crosstour',
       'Crosstour', 'Element', 'Tundra', 'Sequoia', 'Corolla Hatchback',
       '4Runner', 'Echo', 'Tercel', 'MR2 Spyder', 'FJ Cruiser',
       'Corolla iM', 'C-HR', 'Civic Hatchback', '86', 'S2000', 'Supra',
       'Insight', 'Clarity', 'CR-Z', 'Prius Prime', 'Prius Plug-In',
       'Prius c', 'Prius C', 'Prius v'])
        with col2:
            st.number_input("Year", value=2001, min_value=1886, step=1, key="year")
            st.number_input("Engine size (L)", value=1.5, key="engine_size", min_value=0.9, step=0.1)
        with col3:
            st.selectbox("Make", key="make", index=0, options=['toyota', 'honda'])
            st.selectbox("Province", index=0, key="province", options=['NB', 'QC', 'BC', 'ON', 'AB', 'MB', 'SK', 'NS', 'PE', 'NL', 'YT', 'NC', 'OH', 'SC'])
        with col4:    
            st.selectbox("trim", index=0, key="trim", options=['Base', 'Three Touring', 'Touring', 'Two', 'L Eco', 'Four', 'II',
       'Three', 'XLE', 'Limited', 'LE', 'IV', 'Persona Series', 'One',
       'Standard', 'Five', 'III', 'LE AWD-e', 'XLE AWD-e',
       'Limited Hybrid', 'Hybrid', 'SE', 'Plus', 'LE Plus',
       'Limited Platinum', 'Platinum', 'Sport', 'XSE', 'LX', 'EX',
       'VALUE PACKAGE', 'DX', 'VP', 'LX-S', 'EX-L', 'EX-T', 'Si', 'SI',
       'HYBRID', 'Hybrid CVT SULEV', 'EX Leather', 'EX-L V6', '3.0 EX',
       'EX LEATHER', 'EX V6', 'EX-L V-6', 'Touring V6', '3.0 LX',
       'Hybrid Touring', 'B1', 'CE', 'XRS', 'LE Eco', 'LE Eco Premium',
       'VE', 'S', 'L', 'LE Special Edition',
       '50th Anniversary Special Edition', 'S Plus', 'LE Premium',
       'Special Edition', 'S Premium', 'RT', 'RTS', 'RTL', 'RTX', 'RTL-E',
       'Black Edition', 'Touring Elite', 'Elite', 'SPECIAL EDITION',
       'SLE', 'XR', 'Adventure', 'PreRunner', 'TRD Sport', 'TRD Off Road',
       'SR', 'TRD Pro', 'SR5', 'SE Sport', 'LE V6', 'SE V6', 'XLE V6',
       'SE Nightshade', 'XLE Hybrid', 'SE Hybrid', 'LE Hybrid', 'Avalon',
       'XLS', 'XLE Limited', 'XLE Premium', 'Limited Premium',
       'SE Premium', 'EX-P', 'SC', '1794 Edition', 'Tundra Grade',
       'SR5 V6', 'V6 LIMITED', 'LIMITED', 'Night Shade', 'SR5 Premium',
       'Off-Road', 'TRD Off-Road Premium', 'Trail', 'Venture',
       'Sport Touring', 'Type-R', '860 Special Edition', 'TRD SE', 'GT',
       'A91 Edition', 'Premium', 'Launch Edition', 'Advanced'])
            st.selectbox("body_type", index=0, key="body_type", options=['sedan', 'hatchback', 'suv', 'coupe', 'pickup', 'minivan',
       'convertible', 'wagon', 'crossover', 'mini_mpv'])

        st.form_submit_button("Calculate", type="primary", on_click=make_prediction, kwargs=dict(pipe=pipe))

    if st.session_state["pred"] is not None:
        st.subheader(f"The estimated car price is {st.session_state.pred:,.2f}$")
        
        metrics = st.session_state.get("metrics", {})
        if metrics:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(format_metric_cheap("Cheaper than market if below", f"${metrics['cheaper_than_market']}"), unsafe_allow_html=True)
            with col2:
                st.markdown(format_metric_normal("Normal Range", f"${metrics['normal_range']}"), unsafe_allow_html=True)
            with col3:
                st.markdown(format_metric_expensive("Expensive if over", f"${metrics['expensive_than_market']}"), unsafe_allow_html=True)
    else:
        st.write("Input information and click on Calculate to get an estimated price")

    #st.write(st.session_state)

