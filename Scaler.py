import streamlit as st
import pandas as np


def Normalize(df, numerical_cols):
    st.subheader("Normalize")

    option = st.selectbox(
        "Select Scaler",
        ("Min-Max Scaler", "Z-Score Scaler"),
    )

    button_normalize = st.button("Process")

    if button_normalize:
        if option == "Min-Max Scaler":
            for col in numerical_cols:
                df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
            st.session_state["df_Normalize"] = df.copy()
        elif option == "Z-Score Scaler":
            for col in numerical_cols:
                df[col] = (df[col] - df[col].mean()) / df[col].std()

            st.session_state["df_Normalize"] = df.copy()

        normalized = st.session_state.get("df_Normalize")

        st.dataframe(normalized.head(10), use_container_width=True)
        st.download_button("Download Normalized Data", normalized.to_csv().encode('utf-8'), "Normalized_data.csv", "text/csv", key='download-csv')
        

    