import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Data Analytics Assistant",
    layout="wide"
)

# =====================================================
# TITLE
# =====================================================

st.title("Data Analytics Assistant")

st.write("Upload your Excel or CSV file")

# =====================================================
# FILE UPLOADER
# =====================================================

uploaded_file = st.file_uploader(
    "Upload Excel or CSV File",
    type=["csv", "xlsx"]
)

# =====================================================
# IF FILE IS UPLOADED
# =====================================================

if uploaded_file:

    # =================================================
    # READ FILE
    # =================================================

    if uploaded_file.name.endswith(".csv"):

        df = pd.read_csv(
            uploaded_file,
            low_memory=False
        )

    else:

        df = pd.read_excel(uploaded_file)

    # =================================================
    # LOWERCASE COLUMN NAMES
    # =================================================

    df.columns = df.columns.str.lower()

    # =================================================
    # HANDLE LARGE DATASETS
    # =================================================

    if len(df) > 50000:

        st.warning(
            "Large dataset detected. Using sample for faster performance."
        )

        df = df.sample(50000)

    # =================================================
    # DETECT DATE COLUMNS
    # =================================================

    date_columns = []

    for col in df.columns:

        if "date" in col:

            try:

                df[col] = pd.to_datetime(df[col])

                date_columns.append(col)

            except:

                pass

    # =================================================
    # DETECT NUMERIC COLUMNS
    # =================================================

    numeric_cols = []

    for col in df.columns:

        if pd.api.types.is_numeric_dtype(df[col]):

            numeric_cols.append(col)

    # =================================================
    # SUCCESS MESSAGE
    # =================================================

    st.success("File uploaded successfully")

    # =================================================
    # DATASET PREVIEW
    # =================================================

    st.subheader("Dataset Preview")

    st.dataframe(df.head(20))

    # =================================================
    # DATASET INFORMATION
    # =================================================

    st.subheader("Dataset Information")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Rows",
            df.shape[0]
        )

    with col2:

        st.metric(
            "Columns",
            df.shape[1]
        )

    with col3:

        st.metric(
            "Unique Values First Column",
            df.iloc[:, 0].nunique()
        )

    # =================================================
    # BASIC ANALYTICS
    # =================================================

    st.subheader("Basic Analytics")

    if len(numeric_cols) > 0:

        selected_col = st.selectbox(
            "Select Numeric Column",
            numeric_cols,
            key="basic_analytics_selectbox"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Highest Value",
                round(float(df[selected_col].max()), 2)
            )

        with col2:

            st.metric(
                "Lowest Value",
                round(float(df[selected_col].min()), 2)
            )

        with col3:

            st.metric(
                "Average Value",
                round(float(df[selected_col].mean()), 2)
            )

    else:

        st.warning("No numeric columns found")

    # =================================================
    # QUESTION ENGINE
    # =================================================

    st.subheader("Business Questions")

    question = st.selectbox(

        "Select Business Question",

        [

            "Total Sales",
            "Total Profit",
            "Unique Products",
            "Top Selling Product",
            "Top Selling Product In Year",
            "Highest Sales Region",
            "Average Discount",
            "Highest Profit Product",
            "Lowest Profit Product",
            "Top 5 Products",
            "Total Quantity Sold"

        ],

        key="question_dropdown"

    )

    # =================================================
    # YEAR INPUT
    # =================================================

    selected_year = None

    if question == "Top Selling Product In Year":

        selected_year = st.number_input(
            "Enter Year",
            min_value=2000,
            max_value=2100,
            step=1,
            key="year_input"
        )

    # =================================================
    # ANALYZE BUTTON
    # =================================================

    if st.button(
        "Analyze Data",
        key="analyze_button"
    ):

        # =============================================
        # TOTAL SALES
        # =============================================

        if question == "Total Sales":

            if "sales" in df.columns:

                total_sales = df["sales"].sum()

                st.success(
                    f"Total Sales: {round(total_sales, 2)}"
                )

            else:

                st.error("Sales column not found")

        # =============================================
        # TOTAL PROFIT
        # =============================================

        elif question == "Total Profit":

            if "profit" in df.columns:

                total_profit = df["profit"].sum()

                st.success(
                    f"Total Profit: {round(total_profit, 2)}"
                )

            else:

                st.error("Profit column not found")

        # =============================================
        # UNIQUE PRODUCTS
        # =============================================

        elif question == "Unique Products":

            if "product_name" in df.columns:

                unique_products = df["product_name"].nunique()

                st.success(
                    f"Unique Products: {unique_products}"
                )

            else:

                st.error("Product column not found")

        # =============================================
        # TOP SELLING PRODUCT
        # =============================================

        elif question == "Top Selling Product":

            if "product_name" in df.columns and "sales" in df.columns:

                result = (
                    df
                    .groupby("product_name")["sales"]
                    .sum()
                    .sort_values(ascending=False)
                    .head(1)
                )

                st.subheader("Top Selling Product")

                st.write(result)

            else:

                st.error("Required columns not found")

        # =============================================
        # TOP SELLING PRODUCT IN YEAR
        # =============================================

        elif question == "Top Selling Product In Year":

            year = selected_year

            if len(date_columns) > 0:

                date_col = date_columns[0]

                df["year"] = df[date_col].dt.year

                filtered_df = df[df["year"] == year]

                if len(filtered_df) > 0:

                    result = (

                        filtered_df
                        .groupby("product_name")["sales"]
                        .sum()
                        .sort_values(ascending=False)
                        .head(1)

                    )

                    st.subheader(
                        f"Top Selling Product in {year}"
                    )

                    st.write(result)

                else:

                    st.warning(
                        "No data found for that year"
                    )

            else:

                st.error("No date column found")

        # =============================================
        # HIGHEST SALES REGION
        # =============================================

        elif question == "Highest Sales Region":

            if "region" in df.columns and "sales" in df.columns:

                result = (
                    df
                    .groupby("region")["sales"]
                    .sum()
                    .sort_values(ascending=False)
                    .head(1)
                )

                st.subheader("Highest Sales Region")

                st.write(result)

            else:

                st.error("Required columns not found")

        # =============================================
        # AVERAGE DISCOUNT
        # =============================================

        elif question == "Average Discount":

            if "discount" in df.columns:

                avg_discount = df["discount"].mean()

                st.success(
                    f"Average Discount: {round(avg_discount, 2)}"
                )

            else:

                st.error("Discount column not found")

        # =============================================
        # HIGHEST PROFIT PRODUCT
        # =============================================

        elif question == "Highest Profit Product":

            if "product_name" in df.columns and "profit" in df.columns:

                result = (
                    df
                    .groupby("product_name")["profit"]
                    .sum()
                    .sort_values(ascending=False)
                    .head(1)
                )

                st.subheader("Highest Profit Product")

                st.write(result)

            else:

                st.error("Required columns not found")

        # =============================================
        # LOWEST PROFIT PRODUCT
        # =============================================

        elif question == "Lowest Profit Product":

            if "product_name" in df.columns and "profit" in df.columns:

                result = (
                    df
                    .groupby("product_name")["profit"]
                    .sum()
                    .sort_values()
                    .head(1)
                )

                st.subheader("Lowest Profit Product")

                st.write(result)

            else:

                st.error("Required columns not found")

        # =============================================
        # TOP 5 PRODUCTS
        # =============================================

        elif question == "Top 5 Products":

            if "product_name" in df.columns and "sales" in df.columns:

                result = (
                    df
                    .groupby("product_name")["sales"]
                    .sum()
                    .sort_values(ascending=False)
                    .head(5)
                )

                st.subheader("Top 5 Products")

                st.write(result)

            else:

                st.error("Required columns not found")

        # =============================================
        # TOTAL QUANTITY SOLD
        # =============================================

        elif question == "Total Quantity Sold":

            if "quantity" in df.columns:

                total_quantity = df["quantity"].sum()

                st.success(
                    f"Total Quantity Sold: {total_quantity}"
                )

            else:

                st.error("Quantity column not found")

    # =================================================
    # VISUALIZATIONS
    # =================================================

    st.subheader("Visualizations")

    if len(numeric_cols) > 0:

        chart_type = st.selectbox(
            "Select Chart Type",
            [
                "Bar Chart",
                "Pie Chart",
                "Line Chart"
            ],
            key="chart_type_selectbox"
        )

        x_axis = st.selectbox(
            "Select X Axis",
            df.columns,
            key="x_axis_selectbox"
        )

        y_axis = st.selectbox(
            "Select Y Axis",
            numeric_cols,
            key="y_axis_selectbox"
        )

        chart_data = df[[x_axis, y_axis]].head(100)

        chart_data = chart_data.dropna()

        # =============================================
        # BAR CHART
        # =============================================

        if chart_type == "Bar Chart":

            fig = px.bar(
                chart_data,
                x=x_axis,
                y=y_axis
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # =============================================
        # PIE CHART
        # =============================================

        elif chart_type == "Pie Chart":

            fig = px.pie(
                chart_data,
                names=x_axis,
                values=y_axis
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # =============================================
        # LINE CHART
        # =============================================

        elif chart_type == "Line Chart":

            fig = px.line(
                chart_data,
                x=x_axis,
                y=y_axis
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )