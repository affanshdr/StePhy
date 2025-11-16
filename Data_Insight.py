import streamlit as st
import pandas as pd


def Data_Information(df):
    
                # Display metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Rows", df.shape[0])
                with col2:
                    st.metric("Columns", df.shape[1])
                with col3:
                    st.metric("Memory", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
                    

                # Show column list
                with st.expander("📋 Column List"):
                    st.write(df.columns.tolist())


                # Show categorical and numerical columns
                numerik_cols = df[[i for i in df.columns if df[i].dtype in ['int64', 'float64']]].columns
                kategorik_cols = df[[i for i in df.columns if df[i].dtype in ['object']]].columns
                st.expander("📊 Numerical Columns").write(numerik_cols)
                st.expander("📊 Categorical Columns").write(kategorik_cols)
                        
                    
                
                # Display dataframe dengan grid jelas
                st.dataframe(
                    df.head(10),
                    use_container_width=True,
                )

                