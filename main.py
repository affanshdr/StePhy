import streamlit as st
import pandas as pd

from Missing_value import missing_value_handler
from Missing_value import missing_value_table
from Data_Insight import Data_Information

if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="StePhy", page_icon= "./Assets/Logo_tunggal.png")

    # Sidebar
    st.sidebar.markdown("# StePhy")
    st.sidebar.markdown("---")


    with st.container():
        st.markdown("<h1 style='text-align: center;'>Data Preprocessing</h1>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 6, 1])

        with col1:
            st.write("")


        # Main 
        with col2:

            # Upload CSV
            uploaded_file = st.file_uploader("Upload your dataset", type=['csv', 'txt'])


            if uploaded_file is not None:
                st.success("File uploaded successfully")
                # Auto-detect separator atau manual

                col1, col2 = st.columns(2)
                with col1:
                    auto_detect = st.checkbox("Auto-detect separator", value=True)
                with col2:
                    if not auto_detect:
                        manual_sep = st.text_input("Manual separator", value=",")

                try:
                    if auto_detect:
                        # Try common separators
                        separators = [',', '\t', ';', ' ', '|']
                        best_df = None
                        max_cols = 0
                        best_sep = None
                        
                        for sep in separators:
                            try:
                                temp_df = pd.read_csv(uploaded_file, sep=sep, nrows=5)
                                if temp_df.shape[1] > max_cols:
                                    max_cols = temp_df.shape[1]
                                    best_df = temp_df
                                    best_sep = sep
                                uploaded_file.seek(0)  # Reset file pointer
                            except:
                                uploaded_file.seek(0)
                                continue
                        
                        if best_df is not None:
                            # Load full dataset with best separator
                            uploaded_file.seek(0)
                            df = pd.read_csv(uploaded_file, sep=best_sep)
                            
                            sep_name = {
                                ',': 'comma',
                                '\t': 'tab',
                                ';': 'semicolon',
                                ' ': 'space',
                                '|': 'pipe'
                            }.get(best_sep, 'unknown')
                            
                            st.info(f"🔍 Auto-detected separator: **{sep_name}**")
                    else:
                        df = pd.read_csv(uploaded_file, sep=manual_sep)

                    st.subheader("Data Preview")

                    
                    # Save Session
                    st.session_state['df_upload'] = df.copy()
                
                except Exception as e:
                    st.error(f"Error loading file: {str(e)}")
                    st.info("Try selecting separator manually or check file format")
                    
                # Step 1
                # Data Information
                Data_Information(st.session_state.get('df_upload'))
                
                if 'df_missing_value' not in st.session_state or \
                   'last_uploaded_file' not in st.session_state or \
                   st.session_state.get('last_uploaded_file') != uploaded_file.name:
                    st.session_state['df_missing_value'] = st.session_state['df_upload'].copy()
                    st.session_state['last_uploaded_file'] = uploaded_file.name
                    # Reset history kolom missing saat upload baru
                    if 'cols_with_missing_history' in st.session_state:
                        del st.session_state['cols_with_missing_history']

                # Step 2 
                # Missing Value 
                missing_value_table(st.session_state['df_missing_value'])

                # Step3
                testing = st.session_state['df_missing_value'].copy()
                test = [col for col in testing.columns if testing[col].isnull().sum() > 0]
            
            
                
            
                with col3:
                    st.write("")