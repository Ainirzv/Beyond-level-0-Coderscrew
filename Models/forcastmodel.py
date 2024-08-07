import streamlit as st
import pandas as pd
import numpy as np
from pycaret.regression import *


def forecasting():
    if "data" not in st.session_state or st.session_state.data is None:
        st.warning("Please upload data in the Data Ingestion section first.")
        return

    st.header("Forecasting with PyCaret")

    # Allow user to select columns to drop
    columns_to_drop = st.multiselect(
        "Select columns to drop:", st.session_state.data.columns
    )
    df = st.session_state.data.drop(columns=columns_to_drop)

    # Select column to predict
    target_column = st.selectbox("Select column to predict:", df.columns)

    # Check if the target column is numeric
    if not np.issubdtype(df[target_column].dtype, np.number):
        st.error(
            "The selected column must be numeric for regression. Please select a numeric column."
        )
        return

    # Handle non-numeric columns
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    categorical_columns = df.select_dtypes(exclude=[np.number]).columns

    # Create input fields for numeric columns
    st.subheader("Enter values for numeric features:")
    input_data = {}
    for col in numeric_columns:
        if col != target_column:
            input_data[col] = st.number_input(
                f"Enter value for {col}:", value=float(df[col].mean())
            )

    # Create select boxes for categorical columns
    st.subheader("Select values for categorical features:")
    for col in categorical_columns:
        unique_values = df[col].unique()
        input_data[col] = st.selectbox(f"Select value for {col}:", unique_values)

    # Set up PyCaret and train models
    if "model" not in st.session_state:
        if st.button("Start Automated ML Process"):
            with st.spinner("Setting up the experiment..."):
                reg_setup = setup(
                    data=df,
                    target=target_column,
                    session_id=42,
                    normalize=True,
                    transformation=True,
                    remove_multicollinearity=True,
                    multicollinearity_threshold=0.95,
                    log_experiment=False,
                    experiment_name="bat_forecast",
                )

            st.success("Experiment setup complete!")

            # Compare models
            with st.spinner("Training and comparing models..."):
                best_model = compare_models(sort="RMSE")

            st.success("Model training complete!")

            # Display best model results
            st.subheader("Best Model:")
            model_results = pull()
            st.dataframe(model_results.head(1))

            # Store the best model in session state
            st.session_state.model = best_model
            st.session_state.model_results = model_results.head(1)

    else:
        st.subheader("Best Model:")
        st.dataframe(st.session_state.model_results)

    # Make prediction
    if st.button("Make Prediction"):
        if "model" in st.session_state:
            # Create a DataFrame with user input
            input_df = pd.DataFrame([input_data])

            prediction = predict_model(st.session_state.model, data=input_df)
            st.write(
                f"Predicted {target_column}: {prediction['prediction_label'].iloc[0]}"
            )
        else:
            st.warning(
                "Please train the model first by clicking 'Start Automated ML Process'."
            )

    # Option to retrain
    if st.button("Retrain Model"):
        if "model" in st.session_state:
            del st.session_state.model
            del st.session_state.model_results
        st.rerun()
