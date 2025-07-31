import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def app():
    st.title("BANKING SECTOR ANALYSIS BY STATE")
    st.write("Content for app1")

    # ✅ File uploader should be INSIDE the function
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], key="file_upload_app1")

    # ✅ All logic inside the function
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)

            if 'state' in df.columns and 'banking' in df.columns:
                # Compute average
                state_banking_avg = df.groupby('state')['banking'].mean().sort_values(ascending=False)

                # Plot
                fig, ax = plt.subplots(figsize=(10, 5))
                state_banking_avg.head(10).plot(kind='bar', color='skyblue', ax=ax)
                ax.set_title('Average of Top 10 States in Banking Sector')
                ax.set_ylabel('Average Banking Value')
                ax.set_xlabel('State')
                ax.tick_params(axis='x', rotation=45)
                plt.tight_layout()

                st.subheader("Top 10 States by Average Banking Sector Value")
                st.pyplot(fig)
            else:
                st.error("CSV must have columns: 'state' and 'banking'.")
        except Exception as e:
            st.error(f"Error reading uploaded file: {e}")
    else:
        st.info("Please upload a CSV file to proceed.")







