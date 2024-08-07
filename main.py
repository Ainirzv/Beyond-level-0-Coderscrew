import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from Models.utils import *
from Models.forcastmodel import *

# Set page config
st.set_page_config(page_title="B.A.T. - Business Analysis Tool", layout="wide")


def main():
    st.title("B.A.T. - Business Analysis Tool")

    # Sidebar for navigation
    with st.sidebar:
        selected = option_menu(
            menu_title="Menu",
            options=["Data Ingestion", "Data Analysis", "Visualization", "Forecasting"],
            icons=["cloud-upload", "table", "bar-chart","calendar"],
            menu_icon="cast",
            default_index=0,
        )

    # Initialize session state
    if "data" not in st.session_state:
        st.session_state.data = None

    if selected == "Data Ingestion":
        data_ingestion()
    elif selected == "Data Analysis":
        data_analysis()
    elif selected == "Visualization":
        data_visualization()
    elif selected == "Forecasting":
        forecasting()

if __name__ == "__main__":
    main()

