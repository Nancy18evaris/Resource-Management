import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title("VISUALISATION ON WHICH INDUSTRY EACH STATE EXCELS - ANIMATED VIDEO CHART")
    st.write("Content for app7")

    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], key="file_upload_app7")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Filter out unknown states
        df_filtered = df[df['state'] != 'UNKNOWN']

        # Define the industries of interest
        industries = [
            'retail', 'poultry', 'agriculture', 'manufacturing', 'service', 'sale',
            'organizations', 'banking', 'animal',
            'production', 'pharmaceutical', 'cattle', 'textiles',
            'telecommunications', 'transport', 'food', 'construction',
            'education', 'insurance'
        ]

        # Check if these columns exist in the dataframe
        missing_cols = [col for col in industries if col not in df_filtered.columns]
        if missing_cols:
            st.error(f"The following industry columns are missing in the dataset: {missing_cols}")
        else:
            # Step 1: Group by state and compute mean for selected industries
            state_industry_avg = df_filtered.groupby('state')[industries].mean()

            # Step 2: Compute total value per state (to get ratios)
            total_value = state_industry_avg.sum(axis=1)

            # Step 3: Calculate industry-wise ratio per state
            industry_ratios = state_industry_avg.div(total_value, axis=0)

            # Step 4: Reshape to long format for animation
            industry_ratios_long = industry_ratios.reset_index().melt(
                id_vars='state',
                value_vars=industries,
                var_name='industry',
                value_name='ratio'
            )

            # Step 5: Create animated bar chart where each frame is one industry
            fig = px.bar(
                industry_ratios_long,
                x='state',
                y='ratio',
                color='state',  # Color by state for clarity
                animation_frame='industry',
                title='Animated: Industry Ratio by State',
                labels={'ratio': 'Industry Ratio', 'state': 'State'},
                range_y=[0, 1],
                height=600
            )
            fig.update_layout(xaxis_tickangle=-45)

            st.plotly_chart(fig)

    else:
        st.info("Please upload a CSV file to visualize the industry ratios by state.")
