import streamlit as st
import pandas as pd
import os
from io import BytesIO 

# 🎨 Streamlit Page Configurations
st.set_page_config(page_title="🚀 Data Transformer", layout='wide')
st.markdown("""
    <style>
        body {
            background-color: #f4f4f4; /* Light Gray */
        }
        .stApp {
            background-color: #FFEBB2; /* Light Yellow */
        }
    </style>
""", unsafe_allow_html=True)
# 🌟 Attractive Header
st.markdown("""
    <style>
        @keyframes fadeInScale {
            0% { opacity: 0; transform: scale(0.8); }
            100% { opacity: 1; transform: scale(1); }
        }
        .animated-title {
            text-align: center;
            color: #FF5733;
            font-size: 2.5em;
            font-weight: bold;
            animation: fadeInScale 1.2s ease-in-out;
        }
    </style>
    <h1 class="animated-title"> Data Transformer</h1> """, unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #3498DB;'>📂 Upload CSV or Excel files for transformation and cleaning</h4>", unsafe_allow_html=True)
st.write("")

# 📤 File Upload Section
st.markdown("### 📁 Upload your files (CSV or Excel):")
uploaded_files = st.file_uploader("Choose files:", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        # 📊 Read the uploaded file
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file format: {file_ext}")
            continue

        # 📌 Display File Info
        st.markdown(f"### 📝 File: `{file.name}`")
        st.markdown(f"📏 **Size:** `{file.size / 1024:.2f} KB`")
        st.markdown("#### 🔍 Data Preview:")
        st.dataframe(df.head())

        # 🛠 Data Cleaning Section
        st.markdown("## 🧹 Data Cleaning")
        if st.checkbox(f"✅ Clean Data for `{file.name}`"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🗑 Remove Duplicates - {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("🎉 Duplicates Removed!")

            with col2:
                if st.button(f"📊 Fill Missing Values - {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✨ Missing values filled!")

        # 🔄 Column Selection
        st.markdown("## 🎯 Select Columns to Keep")
        columns = st.multiselect(f"📌 Choose Columns for `{file.name}`", df.columns, default=df.columns)
        df = df[columns]

        # 📊 Data Visualization
        st.markdown("## 📈 Data Visualization")
        if st.checkbox(f"📊 Show Chart for `{file.name}`"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # 🔄 Conversion Section
        st.markdown("## 🔄 Convert & Download")
        conversion_type = st.radio(f"🎯 Convert `{file.name}` to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"🚀 Convert `{file.name}`"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                new_file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                new_file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            buffer.seek(0)

            st.download_button(
                label=f"📥 Download `{new_file_name}`",
                data=buffer,
                file_name=new_file_name,
                mime=mime_type
            )

st.success("🎉 Thank you for using Data Transformer! 🚀")
