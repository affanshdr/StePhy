import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, LabelEncoder


# 1. CEK CARDINALITY

def cardinality_check(categorical_cols, row_count, df):
    high = []
    low = []

    for col in categorical_cols:
        if df[col].nunique() > (0.05 * row_count):
            high.append(col)
        else:
            low.append(col)

    return low, high

# 2. RANDOM EMBEDDING GENERATOR
def random_embedding(df, column, dim=8, seed=42):
    np.random.seed(seed)

    unique_vals = df[column].unique()
    mapping = {val: np.random.randn(dim) for val in unique_vals}

    embed_rows = [mapping[val] for val in df[column]]
    embed_df = pd.DataFrame(embed_rows, 
                            columns=[f"{column}_emb_{i}" for i in range(dim)])
    
    return embed_df


# 3. FEATURE ENCODING STREAMLIT
def feature_encoding(df, categorical_cols, row_count):
    st.subheader("Feature Encoding")

    row_count = len(df)
    

    # Pisahkan cardinality
    low_cardinality, high_cardinality = cardinality_check(
        categorical_cols, row_count, df
    )

    col1, col2 = st.columns(2)
    with col1:
        st.success("Low Cardinality")
        for c in low_cardinality:
            st.write(f"- {c}")

    with col2:
        st.warning("High Cardinality")
        for c in high_cardinality:
            st.write(f"- {c}")

    st.divider()

    # Pilih metode encoding
    col1, col2 = st.columns(2)
    with col1:
        low_method = st.selectbox(
            "Low Cardinality Encoding",
            ("One-Hot Encoding", "Label Encoding")
        )

    with col2:
        high_method = st.selectbox(
            "High Cardinality Encoding",
            ("Random Embedding (Recommended)",)
        )

    # Tombol proses
    if st.button("Process Encoding"):

        # Ambil kolom numerik
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        df_numeric = df[numeric_cols]


        # LOW CARDINALITY
   
        if low_method == "One-Hot Encoding":
            ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
            low_encoded = pd.DataFrame(
                ohe.fit_transform(df[low_cardinality]),
                columns=ohe.get_feature_names_out(low_cardinality)
            )
        else:
            low_encoded = df[low_cardinality].apply(LabelEncoder().fit_transform)


        # HIGH CARDINALITY
        high_encoded_list = []
        for col in high_cardinality:
            emb_df = random_embedding(df, col, dim=8)
            high_encoded_list.append(emb_df)

        df_high_emb = pd.concat(high_encoded_list, axis=1) if high_encoded_list else pd.DataFrame()

        # GABUNGKAN
        df_final = pd.concat([df_numeric, low_encoded, df_high_emb], axis=1)
        st.success("Encoding Completed!")
        st.session_state["Feature_Encoding"] = df_final.copy()
        df_encoded = st.session_state.get("Feature_Encoding")
        st.dataframe(df_encoded.head(10), use_container_width=True )

        st.download_button(
                    label="Download Preprocessed Data",
                    data=df_encoded.to_csv(index=False),
                    file_name="preprocessed_data.csv",
                    mime="text/csv"
                )

        return df_final

