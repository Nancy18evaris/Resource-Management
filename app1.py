import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("BANKING SECTOR ANALYSIS BY STATE")

# File uploader widget
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

#1.Top 10 States by Average Banking Sector Value
if uploaded_file is not None:
    # Read uploaded CSV
    try:
        df = pd.read_csv(uploaded_file)

        # Check required columns
        if 'state' in df.columns and 'banking' in df.columns:
            # Calculate average banking per state
            state_banking_avg = df.groupby('state')['banking'].mean().sort_values(ascending=False)

            # Plotting with Matplotlib
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
            st.error("Columns 'state' and 'banking' not found in the uploaded CSV.")
    except Exception as e:
        st.error(f"Error reading the uploaded file: {e}")
else:
    st.info("Please upload a CSV file to proceed.")






