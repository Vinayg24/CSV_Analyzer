# 📊 Final Version: app.py with SQLite DB Connection
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Import database functions
from database import create_table, insert_metadata, get_metadata

# Page Setup
st.set_page_config(page_title="📊 CSV Analyzer", layout="wide")

# Call to create DB table on first run
create_table()

# Custom Styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
        }
        .main {
            background-color: #f0f2f6;
            padding: 20px;
        }
        h1 {
            text-align: center;
            color: #2c3e50;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        .stButton>button {
            background-color: #4a90e2;
            color: white;
            padding: 0.6em 1em;
            border: none;
            border-radius: 8px;
            transition: 0.3s ease-in-out;
            font-weight: 600;
        }
        .stButton>button:hover {
            background-color: #1c66c1;
            transform: scale(1.02);
        }
        .block-container {
            padding: 2rem 2rem 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>📊 CSV Analyzer Dashboard</h1>", unsafe_allow_html=True)
st.markdown("### Upload your dataset and perform smart analysis and visualizations 🚀")

# Upload File
st.sidebar.header("📁 Upload File")
uploaded_file = st.sidebar.file_uploader("Choose a CSV or JSON file", type=["csv", "json"])

# Data Handling
df = None

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding_errors='ignore')
            st.sidebar.success("✅ CSV file uploaded successfully!")
        elif uploaded_file.name.endswith('.json'):
            df = pd.read_json(uploaded_file)
            st.sidebar.success("✅ JSON file uploaded and converted to CSV format!")

            # Download option
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_bytes = csv_buffer.getvalue().encode()
            st.sidebar.download_button(
                label="⬇️ Download Converted CSV",
                data=csv_bytes,
                file_name=uploaded_file.name.replace('.json', '.csv'),
                mime='text/csv'
            )

        # Save metadata to database
        filename = uploaded_file.name
        rows, columns = df.shape
        insert_metadata(filename, rows, columns)
        st.success("✅ File metadata saved to the database.")

        # Preview
        st.markdown("## 🔍 Data Preview")
        with st.expander("Click to view first 5 rows", expanded=True):
            st.dataframe(df.head(), use_container_width=True)

        # DataFrame Operations
        st.markdown("## ⚙️ DataFrame Operations")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("📏 Show Shape"):
                st.info(f"Shape: {df.shape} (Rows, Columns)")

            if st.button("📋 Show Size"):
                st.info(f"Total elements: {df.size}")

            if st.button("👀 Show Head"):
                st.write(df.head())

            if st.button("📉 Show Tail"):
                st.write(df.tail())

        with col2:
            if st.button("ℹ️ Show Info"):
                buffer = io.StringIO()
                df.info(buf=buffer)
                st.code(buffer.getvalue())

            if st.button("📊 Show Describe"):
                st.write(df.describe())

        # Missing Values
        st.markdown("## 🚫 Missing Values")
        missing = df.isnull().sum()
        missing_percent = (missing / len(df)) * 100
        missing_df = pd.DataFrame({'Missing Values': missing, 'Percent (%)': missing_percent})
        st.dataframe(missing_df[missing_df['Missing Values'] > 0])

        # Data Cleaning
        st.markdown("## 🧹 Data Cleaning")
        option = st.radio("Choose cleaning method", ["Drop missing rows", "Fill with 0", "Fill with mean"])
        if st.button("Clean Data"):
            if option == "Drop missing rows":
                df.dropna(inplace=True)
            elif option == "Fill with 0":
                df.fillna(0, inplace=True)
            elif option == "Fill with mean":
                df.fillna(df.mean(numeric_only=True), inplace=True)
            st.success("✅ Data cleaned successfully!")

        # Column Filter
        st.markdown("## 🔎 Column Filter")
        selected_column = st.selectbox("Select column to filter", df.columns)
        unique_vals = df[selected_column].dropna().unique()
        selected_val = st.selectbox("Select value", unique_vals)
        filtered_df = df[df[selected_column] == selected_val]
        st.dataframe(filtered_df)

        # Correlation Heatmap
        st.markdown("## 🔥 Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

        # Date Filtering
        st.markdown("## 📅 Date Filtering")
        date_cols = df.select_dtypes(include='object').columns
        for col in date_cols:
            try:
                df[col] = pd.to_datetime(df[col])
            except:
                continue

        date_filter_col = st.selectbox("🗓️ Select a date column (if any)", df.select_dtypes(include='datetime').columns)
        if date_filter_col:
            start_date = st.date_input("Start Date", value=df[date_filter_col].min())
            end_date = st.date_input("End Date", value=df[date_filter_col].max())
            df = df[(df[date_filter_col] >= pd.to_datetime(start_date)) & (df[date_filter_col] <= pd.to_datetime(end_date))]

        # Top-K Values
        st.markdown("## 🔢 Top-K Frequent Values")
        column_to_check = st.selectbox("Select column", df.columns)
        top_k = st.slider("How many top values?", 1, 20, 5)
        top_values = df[column_to_check].value_counts().head(top_k)
        st.bar_chart(top_values)

        # GroupBy Aggregation
        st.markdown("## 🔄 GroupBy Aggregation")
        group_column = st.selectbox("Group by column", df.columns)
        agg_column = st.selectbox("Aggregate on column", df.select_dtypes(include=np.number).columns)
        agg_func = st.selectbox("Aggregation", ["mean", "sum", "min", "max"])
        if st.button("Group & Aggregate"):
            grouped = df.groupby(group_column)[agg_column].agg(agg_func).reset_index()
            st.dataframe(grouped)

        # Pie Chart
        st.markdown("## 🥧 Pie Chart")
        cat_column = st.selectbox("Select categorical column", df.select_dtypes(include='object').columns)
        if st.button("Show Pie Chart"):
            counts = df[cat_column].value_counts()
            fig, ax = plt.subplots()
            ax.pie(counts, labels=counts.index, autopct="%1.1f%%", startangle=90)
            ax.axis('equal')
            st.pyplot(fig)

        # Custom Visualization
        st.markdown("## 📈 Visualization")
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

        if len(numeric_cols) >= 2:
            x_axis = st.selectbox("🔸 X-axis", options=numeric_cols, index=0)
            y_axis = st.selectbox("🔹 Y-axis", options=numeric_cols, index=1)
            plot_type = st.radio("📍 Select Plot Type", ["Bar Chart", "Line Chart"], horizontal=True)

            fig, ax = plt.subplots(figsize=(10, 5))
            if plot_type == "Bar Chart":
                ax.bar(df.index, df[y_axis], color="#3498db")
                ax.set_title(f"{y_axis} - Bar Chart")
            else:
                ax.plot(df[x_axis], df[y_axis], color="#2ecc71", marker="o")
                ax.set_title(f"{y_axis} vs {x_axis} - Line Chart")

            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)
            st.pyplot(fig)
        else:
            st.warning("🔑 Need at least 2 numeric columns for plotting!")

    except Exception as e:
        st.error(f"❌ Error loading file:\n{e}")
else:
    st.info("👈 Upload a CSV or JSON file to get started!")

# Upload History (from database)
st.markdown("## 🕒 Recent Upload History")
try:
    history = get_metadata()
    if history:
        history_df = pd.DataFrame(history, columns=["Filename", "Uploaded On", "Rows", "Columns"])
        st.dataframe(history_df)
    else:
        st.info("No upload history yet.")
except Exception as e:
    st.error(f"⚠️ Failed to fetch history: {e}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color: gray;'>"
    "Made with ❤️ by <b>Laksh Vyas</b> using Streamlit"
    "</div>",
    unsafe_allow_html=True
)
