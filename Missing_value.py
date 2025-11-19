import streamlit as st
import pandas as pd

def missing_value_handler(col_series, option):
    if option == "Mean":
        filled_series = col_series.fillna(col_series.mean())
    elif option == "Median":
        filled_series = col_series.fillna(col_series.median())
    elif option == "Mode":
        filled_series = col_series.fillna(col_series.mode().iloc[0])
    elif option == "Drop":
        filled_series = col_series.dropna()
    elif option == "fill Unknown":
        filled_series = col_series.fillna("Unknown")
    else:
        filled_series = col_series.copy()
    return filled_series

def missing_value_table(df):
    if df is None:
        st.warning("Data belum tersedia untuk penanganan missing value.")
        return
    
    # session state untuk tracking
    if 'original_missing_cols' not in st.session_state:
        st.session_state['original_missing_cols'] = [
            col for col in df.columns if df[col].isnull().sum() > 0
        ]
    
    # Kalo tidak ada missing Value
    if len(st.session_state['original_missing_cols']) == 0:
        st.success("No missing value detected")
        return

    st.subheader("Missing Value Handler")
    
    with st.expander("🚨 Missing Value Status", expanded=True):

        current_missing = [col for col in df.columns if df[col].isnull().sum() > 0]
        total_cols = len(st.session_state['original_missing_cols'])
        processed_cols = total_cols - len(current_missing)
        
        # Progress bar
        progress = processed_cols / total_cols if total_cols > 0 else 1.0
        st.progress(progress)
        st.write(f"**Progress: {processed_cols}/{total_cols} columns processed**")
        st.divider()

        header1, header2, header3 = st.columns([2, 1, 1])
        with header1:
            st.markdown("<h2 style='text-align: center'>Column</h2>", unsafe_allow_html=True)
        with header2:
            st.markdown("<h2 style='text-align: center'>Status</h2>", unsafe_allow_html=True)
        with header3:
            st.markdown("<h2 style='text-align: center'>Action</h2>", unsafe_allow_html=True)
        st.divider()

        # Loop SEMUA kolom yang pernah punya missing value
        for col_name in st.session_state['original_missing_cols']:

            missing_count = df[col_name].isnull().sum()
            is_clean = missing_count == 0
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.subheader(f"{col_name}")
            
            with col2:
                if is_clean:
                    st.success("Clean")
                else:
                    st.error(f"⚠️ {missing_count} missing")
            
            with col3:
                if not is_clean:

                    if df[col_name].dtype in ['int64', 'float64']:
                        action = st.selectbox(
                            "Method",
                            ("Mean", "Median", "Mode", "Drop"),
                            key=f"handling_missing_{col_name}",
                            label_visibility="collapsed"
                        )
                    else:
                        action = st.selectbox(
                            "Method",
                            ("Mode", "Drop", "fill Unknown"),
                            key=f"handling_missing_{col_name}",
                            label_visibility="collapsed"
                        )
                    
                    if st.button("Process", key=f"process_{col_name}"):
                        current_df = st.session_state['df_missing_value']
                        
                        if action == "Drop":
                            current_df = current_df.dropna(subset=[col_name])
                        else:
                            current_df[col_name] = missing_value_handler(current_df[col_name], action)
                        
                        st.session_state['df_missing_value'] = current_df
                        st.rerun()
                else:
                    st.info("Done")
            
            st.divider()
        
        # Summary
        if len(current_missing) == 0:
            st.success("🎉 All missing values have been handled!")


            Final = st.session_state['df_missing_value'].copy()

            st.dataframe(
                Final.head(10),
                use_container_width=True,
            )

            st.write(Final.shape)

            st.download_button(
                label="Download Clean Data",
                data=pd.DataFrame(st.session_state['df_missing_value']).to_csv(index=False),
                file_name="clean_data.csv",
                mime="text/csv"
            )

