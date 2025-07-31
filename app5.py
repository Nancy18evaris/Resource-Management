import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title("STATE WISE AGRICULTURE RATIO ANALYSIS")
    st.write("Content for app5")

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], key="file_upload_app5")

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)

            # Step 0: Exclude rows where state is 'UNKNOWN'
            df_filtered = df[df['state'] != 'UNKNOWN']

            # Step 1: Compute average agriculture per state
            state_agriculture_avg = df_filtered.groupby('state')['agriculture'].mean().sort_values(ascending=False)

            # Step 2: Compute ratio of each state vs total
            state_agriculture_ratio = state_agriculture_avg / state_agriculture_avg.sum()

            # Step 3: Convert to DataFrame for pie chart
            ratio_df = state_agriculture_ratio.reset_index()
            ratio_df.columns = ['State', 'Ratio']

            # Step 4: Plot pie chart (donut style)
            st.subheader("Agriculture Sector Contribution by State (Ratio)")
            fig = px.pie(
                ratio_df,
                names='State',
                values='Ratio',
                title='State-wise Ratio of Average Agriculture',
                hole=0.3  # for donut chart
            )

            # Show chart in Streamlit
            st.plotly_chart(fig)

        except Exception as e:
            st.error(f"❌ Error loading file: {e}")
    else:
        st.info("📁 Please upload a CSV file to see the agriculture ratio chart.")
