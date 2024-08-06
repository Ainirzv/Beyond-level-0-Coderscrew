import streamlit as st
import pandas as pd
from pycaret.classification import setup, compare_models, pull, predict_model
import openpyxl


def padding(n=1):
    st.write("<br>" * n, unsafe_allow_html=True)


# Function to load data
def load_data(file):
    file_format = file.name.split(".")[-1]
    if file_format == "csv":
        data = pd.read_csv(file)
    elif file_format in ["xlsx", "xls"]:
        data = pd.read_excel(file)
    else:
        st.error("Unsupported file format.")
        return None
    return data


# Function to display data preview and description
def display_data(data):
    st.write("Data Preview:")
    st.write(data.head())


def display_description(data, uploaded_file):
    st.write("Dataset Description:")
    st.write(
        {
            "rows": data.shape[0],
            "columns": data.shape[1],
            "missing_values": data.isnull().sum().sum(),
            "memory_size": data.memory_usage(deep=True).sum(),
            "file_format": uploaded_file.name.split(".")[-1],
        }
    )


def main():
    st.title("Business Analytics with PyCaret")

    # Data ingestion
    uploaded_file = st.file_uploader(
        "Please upload a dataset", type=["csv", "xlsx", "xls"]
    )

    if uploaded_file is not None:
        data = load_data(uploaded_file)
        if data is not None:
            st.session_state["dataset"] = data
            display_data(data)
            display_description(data, uploaded_file)

            # PyCaret setup
            with st.spinner("Setting up PyCaret..."):
                target_column = st.selectbox(
                    "Select target column", options=data.columns
                )
                setup(data, target=target_column, session_id=123)

                # Compare commonly used models
                st.spinner("Comparing models...")
                common_models = ["dt", "rf", "xgboost", "logistic", "svc","mlp"]
                best_model = compare_models(
                    include=common_models, fold=5  # Number of cross-validation folds
                )
                st.write("Best Model:")
                st.write(best_model)

                # Model predictions
                st.write("Make Predictions")
                input_data = st.text_area(
                    "Enter your data for prediction (comma-separated):"
                )
                if st.button("Predict"):
                    try:
                        input_data = [float(x) for x in input_data.split(",")]
                        input_df = pd.DataFrame([input_data], columns=data.columns[:-1])
                        predictions = predict_model(best_model, data=input_df)
                        st.write("Prediction:")
                        st.write(predictions)
                    except ValueError:
                        st.error("Please enter valid data.")
    else:
        st.caption("Please upload a dataset to proceed.")
        padding()


if __name__ == "__main__":
    main()
