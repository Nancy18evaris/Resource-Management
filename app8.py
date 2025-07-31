import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title("COMPARISON OF RURAL AND URBAN, MAIN AND MARGINAL WORKING WOMAN BY STATE")
    st.write("Content for app8")

    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], key="file_upload_app8")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Step 0: Exclude 'UNKNOWN' states
        df_filtered = df[df['state'] != 'UNKNOWN']

        # Step 1: Columns of interest
        columns_of_interest = [
            'Main Workers - Rural - Females_log_iqr_winsor',
            'Marginal Workers - Rural - Females_log_iqr_winsor',
            'Main Workers - Urban - Females_log_iqr_winsor',
            'Marginal Workers - Urban - Females_log_iqr_winsor'
        ]

        # Check for missing columns
        missing_cols = [col for col in columns_of_interest if col not in df_filtered.columns]
        if missing_cols:
            st.error(f"The following required columns are missing in the dataset: {missing_cols}")
        else:
            # Compute mean per state for the columns
            state_worker_means = df_filtered.groupby('state')[columns_of_interest].mean().reset_index()

            # Melt into long format for plotting
            melted = state_worker_means.melt(
                id_vars='state',
                var_name='Worker Type',
                value_name='Average Log-IQR-Winsorized'
            )

            # Extract 'Worker Category' and 'Area' from the column names
            melted['Worker Category'] = melted['Worker Type'].apply(lambda x: 'Main' if 'Main' in x else 'Marginal')
            melted['Area'] = melted['Worker Type'].apply(lambda x: 'Rural' if 'Rural' in x else 'Urban')

            # Create combined label for color grouping
            melted['Group'] = melted['Area'] + ' - ' + melted['Worker Category']

            # Plot grouped bar chart
            fig = px.bar(
                melted,
                x='state',
                y='Average Log-IQR-Winsorized',
                color='Group',
                barmode='group',
                title='Comparison of Female Workers by State: Rural vs Urban, Main vs Marginal',
                labels={
                    'Average Log-IQR-Winsorized': 'Avg Female Workers (log scale)',
                    'state': 'State',
                    'Group': 'Worker Type'
                },
                height=600
            )

            fig.update_layout(
                xaxis_tickangle=-45,
                xaxis={'categoryorder': 'total descending'}
            )

            st.plotly_chart(fig)

    else:
        st.info("Please upload a CSV file to display the comparison chart.")
