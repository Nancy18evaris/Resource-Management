import streamlit as st 
import pandas as pd
import plotly.express as px

def app():
    st.title("FINDING IN WHICH INDUSTRY PUDUCHERRY EXCELS")
    st.write("Content for app6")

    # File uploader
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], key="file_upload_app6")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Step 0: Exclude rows where state is 'UNKNOWN'
        df_filtered = df[df['state'] != 'UNKNOWN']

        # Step 1: Filter for Puducherry (case-insensitive)
        pudu_df = df_filtered[df_filtered['state'].str.lower() == 'puducherry']

        if pudu_df.empty:
            st.warning("No data found for Puducherry.")
        else:
            # Step 2: Identify industry columns by excluding known non-industry columns
            exclude_cols = [
                'Unnamed: 0', 'State Code', 'District Code', 'Division', 'Group', 'Class',
                'Main Workers - Total - Persons_log_iqr_winsor', 'Main Workers - Total - Males_log_iqr_winsor',
                'Main Workers - Total - Females_log_iqr_winsor', 'Main Workers - Rural - Persons_log_iqr_winsor',
                'Main Workers - Rural - Males_log_iqr_winsor', 'Main Workers - Rural - Females_log_iqr_winsor',
                'Main Workers - Urban - Persons_log_iqr_winsor', 'Main Workers - Urban - Males_log_iqr_winsor',
                'Main Workers - Urban - Females_log_iqr_winsor', 'Marginal Workers - Total - Persons_log_iqr_winsor',
                'Marginal Workers - Total - Males_log_iqr_winsor', 'Marginal Workers - Total - Females_log_iqr_winsor',
                'Marginal Workers - Rural - Persons_log_iqr_winsor', 'Marginal Workers - Rural - Males_log_iqr_winsor',
                'Marginal Workers - Rural - Females_log_iqr_winsor', 'Marginal Workers - Urban - Persons_log_iqr_winsor',
                'Marginal Workers - Urban - Males_log_iqr_winsor', 'Marginal Workers - Urban - Females_log_iqr_winsor',
                'tokens_no_stop', 'manual_token_present', 'matched_manual_tokens', 'state', 'district',
                'state_count', 'district_count', 'Total_Workers', 'Total_Female_Workers',
                'Total_Male_Workers', 'lon', 'lat'
            ]

            industry_cols = [col for col in df.columns if col not in exclude_cols]

            # Step 3: Calculate average value for each industry in Puducherry
            industry_avg = pudu_df[industry_cols].mean().sort_values(ascending=False)

            # Step 4: Create DataFrame for plotting
            industry_avg_df = industry_avg.reset_index()
            industry_avg_df.columns = ['Industry', 'Average Value']

            # Step 5: Show top excelling industry
            top_industry = industry_avg.idxmax()
            top_value = industry_avg.max()
            st.markdown(f"### Puducherry excels in **'{top_industry}'** with an average value of **{top_value:.2f}**.")

            # Step 6: Plot bar chart
            fig = px.bar(
                industry_avg_df,
                x='Industry',
                y='Average Value',
                title='Average Industry Performance in Puducherry',
                labels={'Average Value': 'Avg Value'},
                color='Average Value',
                color_continuous_scale='Blues'
            )
            fig.update_layout(xaxis_tickangle=-45)

            st.plotly_chart(fig)
    else:
        st.info("📁 Please upload a CSV file to get started.")
