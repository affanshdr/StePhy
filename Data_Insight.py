import streamlit as st
import pandas as pd


def Data_Information(df, categorical_cols, numerical_cols): 
    
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Rows", df.shape[0])
                with col2:
                    st.metric("Columns", df.shape[1])
                with col3:
                    st.metric("Memory", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
                    
                # Show categorical and numerical columns
                with st.expander("📊 Numerical Columns"): 
                    for i in numerical_cols:
                        st.write(f"- {i}")

                with st.expander("📊 Categorical Columns"): 
                    for i in categorical_cols:
                        st.write(f"- {i}")
                    
                # Display dataframe dengan grid jelas
                st.dataframe(
                    df.head(10),
                    use_container_width=True,
                )

                