import streamlit as st
import pandas as pd
import plotly.express as px



# Dark mode theme
def set_dark_mode():
    st.markdown(
        """
        <style>
        .css-18e3th9 { /* Main title */
            color: #ffffff;
            font-family: 'Arial', sans-serif;
            font-size: 40px;
            text-align: center;
            border-bottom: 2px solid #1f77b4;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .css-1d391kg { /* Sidebar background and border */
            background-color: #333333;
            border-right: 2px solid #444444;
        }
        .css-1j7qk0x { /* Sidebar option text */
            color: #ffffff;
        }
        .css-1w4u7ei { /* Sidebar icons */
            color: #1f77b4;
        }
        .css-1v0mbdj { /* Add some padding around the content */
            padding: 20px;
        }
        .css-1l2h7j9 { /* Buttons */
            background-color: #1f77b4;
            color: white;
            border-radius: 5px;
        }
        .css-1csy2w6 { /* Plotly charts */
            border: 1px solid #444444;
            border-radius: 10px;
            padding: 10px;
        }
        body {
            background-color: #222222;
            color: #eeeeee;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def data_ingestion():
    st.header("Data Ingestion")

    uploaded_file = st.file_uploader(
        "Upload a CSV file", type="csv", label_visibility="collapsed"
    )

    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)
            st.session_state.data = data
            st.success("File uploaded successfully!")
            st.dataframe(data.head())
            st.info(f"Rows: {data.shape[0]}, Columns: {data.shape[1]}")
        except pd.errors.EmptyDataError:
            st.error("The uploaded file is empty. Please upload a valid CSV file.")
        except pd.errors.ParserError:
            st.error("Unable to parse the file. Please ensure it's a valid CSV.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
    else:
        st.info("Please upload a CSV file to proceed.")


def data_analysis():
    if st.session_state.data is not None:
        st.header("Data Analysis")

        try:
            # Summary Statistics
            st.subheader("Summary Statistics")
            st.write("Here are some key statistics about your data:")
            description = st.session_state.data.describe(include="all")
            st.write(description)

            st.write("### What does this mean?")
            st.write(
                "- **Count**: The number of non-null entries in each column."
                "- **Mean**: The average value of the column, useful to understand the central tendency of your data."
                "- **Std**: The standard deviation, showing the spread of the data around the mean."
                "- **Min/Max**: The smallest and largest values in the column."
                "- **25%/50%/75% Percentiles**: These values indicate the distribution of your data."
            )

            # Column Information
            st.subheader("Column Information")
            st.write("Here is some information about each column in your dataset:")
            st.write(st.session_state.data.dtypes)

            st.write("### What does this mean?")
            st.write(
                "- **Object**: Categorical or text data."
                "- **Int/Float**: Numerical data."
                "- Understanding column types helps in selecting appropriate analysis and modeling techniques."
            )

            # Missing Values
            st.subheader("Missing Values")
            missing = st.session_state.data.isnull().sum()
            missing_data = missing[missing > 0]
            if not missing_data.empty:
                st.write(missing_data)
                st.write("### What does this mean?")
                st.write(
                    "- **Missing values**: Some columns have missing values, which need to be handled before further analysis."
                    "- Consider filling these missing values with appropriate statistics (mean, median, etc.) or removing the affected rows/columns."
                )
            else:
                st.success("No missing values detected.")

        except Exception as e:
            st.error(f"An error occurred during data analysis: {str(e)}")
    else:
        st.warning(
            "No data available. Please upload a CSV file in the Data Ingestion section."
        )


def data_visualization():
    if st.session_state.data is not None:
        st.header("Customer Data Insights")

        try:
            columns = st.multiselect(
                "Select data points to analyze",
                st.session_state.data.columns,
                default=None,
                help="Choose columns to include in the analysis.",
            )

            if st.button("Generate Insights"):
                st.subheader("Customer Data Analysis")

                overview, details = st.columns([1, 2])

                numeric_columns = [
                    col
                    for col in columns
                    if pd.api.types.is_numeric_dtype(st.session_state.data[col])
                ]
                categorical_columns = [
                    col
                    for col in columns
                    if not pd.api.types.is_numeric_dtype(st.session_state.data[col])
                ]

                with overview:
                    st.markdown("### Quick Overview")
                    total_customers = len(st.session_state.data)
                    st.metric("Total Customers", total_customers)

                    if "revenue" in st.session_state.data.columns:
                        total_revenue = st.session_state.data["revenue"].sum()
                        avg_revenue = st.session_state.data["revenue"].mean()
                        st.metric("Total Revenue", f"${total_revenue:,.2f}")
                        st.metric(
                            "Average Revenue per Customer", f"${avg_revenue:,.2f}"
                        )

                    if categorical_columns:
                        for col in categorical_columns[:3]:
                            top_category = (
                                st.session_state.data[col].value_counts().index[0]
                            )
                            top_category_percentage = (
                                st.session_state.data[col].value_counts().values[0]
                                / total_customers
                            ) * 100
                            st.metric(
                                f"Top {col}",
                                f"{top_category} ({top_category_percentage:.1f}%)",
                            )

                with details:
                    st.markdown("### Detailed Insights")

                    if numeric_columns:
                        st.markdown("#### Customer Metrics")
                        for column in numeric_columns:
                            fig = px.histogram(
                                st.session_state.data,
                                x=column,
                                title=f"Distribution of {column}",
                                labels={column: f"{column} (Values)"},
                                color_discrete_sequence=["#1f77b4"],
                            )
                            fig.update_layout(showlegend=False)
                            st.plotly_chart(fig, use_container_width=True)

                    if categorical_columns:
                        st.markdown("#### Customer Segments")
                        for column in categorical_columns:
                            value_counts = (
                                st.session_state.data[column]
                                .value_counts()
                                .reset_index()
                            )
                            value_counts.columns = ["Category", "Count"]
                            fig = px.pie(
                                value_counts,
                                names="Category",
                                values="Count",
                                title=f"Distribution of {column}",
                                color_discrete_sequence=px.colors.qualitative.Set3,
                            )
                            st.plotly_chart(fig, use_container_width=True)

                st.markdown("### Key Insights and Recommendations")
                insights = generate_insights(
                    st.session_state.data, numeric_columns, categorical_columns
                )
                for insight in insights:
                    st.info(insight)

        except KeyError as e:
            st.error(
                f"Column '{e.args[0]}' not found in the data. Please select a valid column."
            )
        except ValueError as ve:
            st.error(f"Error in creating visualization: {str(ve)}")
        except Exception as e:
            st.error(f"An unexpected error occurred during visualization: {str(e)}")

    else:
        st.warning(
            "No data available. Please upload your customer data CSV file in the Data Ingestion section."
        )


def generate_insights(data, numeric_columns, categorical_columns):
    insights = []

    if "revenue" in numeric_columns:
        top_customers = data.nlargest(5, "revenue")
        insights.append(
            f"Your top 5 customers by revenue contribute ${top_customers['revenue'].sum():,.2f}. Consider implementing a loyalty program for these high-value customers."
        )

    if categorical_columns:
        for col in categorical_columns:
            top_category = data[col].value_counts().index[0]
            top_percentage = (data[col].value_counts().values[0] / len(data)) * 100
            insights.append(
                f"The most common {col} is '{top_category}', representing {top_percentage:.1f}% of your customer base. Tailor your marketing efforts to appeal to this segment."
            )

    if "age" in numeric_columns:
        avg_age = data["age"].mean()
        insights.append(
            f"The average age of your customers is {avg_age:.1f} years. Ensure your products and marketing strategies align with this demographic."
        )

    return insights


def main():
    set_dark_mode()

    st.sidebar.header("Navigation")
    selection = st.sidebar.radio(
        "Go to", ["Data Ingestion", "Data Analysis", "Data Visualization"]
    )

    if selection == "Data Ingestion":
        data_ingestion()
    elif selection == "Data Analysis":
        data_analysis()
    elif selection == "Data Visualization":
        data_visualization()


if __name__ == "__main__":
    main()
