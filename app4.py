import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title("STATE WISE MAIN AND MARGINAL - RURAL FEMALE WORKERS ANALYSIS")
    st.write("Content for app4")

    # File uploader
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], key="file_upload_app4")

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)

            # Step 0: Exclude rows where state is 'UNKNOWN'
            df_filtered = df[df['state'] != 'UNKNOWN']

            # Step 1: Group by state and calculate mean for both columns
            state_means = df_filtered.groupby('state')[
                ['Main Workers - Rural - Females_log_iqr_winsor',
                 'Marginal Workers - Rural - Females_log_iqr_winsor']
            ].mean()

            # Step 2: Identify states with highest averages
            max_main_worker_state = state_means['Main Workers - Rural - Females_log_iqr_winsor'].idxmax()
            max_main_worker_value = state_means['Main Workers - Rural - Females_log_iqr_winsor'].max()

            max_marginal_worker_state = state_means['Marginal Workers - Rural - Females_log_iqr_winsor'].idxmax()
            max_marginal_worker_value = state_means['Marginal Workers - Rural - Females_log_iqr_winsor'].max()

            # Display metrics
            st.subheader("Top Performing States")
            col1, col2 = st.columns(2)
            col1.metric(
                label="Highest Avg Main Rural Female Workers",
                value=max_main_worker_state,
                delta=f"{max_main_worker_value:.2f} (log)"
            )
            col2.metric(
                label="Highest Avg Marginal Rural Female Workers",
                value=max_marginal_worker_state,
                delta=f"{max_marginal_worker_value:.2f} (log)"
            )

            # Prepare data for plot
            state_means_reset = state_means.reset_index()

            # Melt for grouped bar chart
            melted = state_means_reset.melt(
                id_vars='state',
                value_vars=[
                    'Main Workers - Rural - Females_log_iqr_winsor',
                    'Marginal Workers - Rural - Females_log_iqr_winsor'
                ],
                var_name='Worker Type',
                value_name='Average Log-IQR-Winsorized'
            )

            # Rename for clarity
            melted['Worker Type'] = melted['Worker Type'].replace({
                'Main Workers - Rural - Females_log_iqr_winsor': 'Main Rural Females',
                'Marginal Workers - Rural - Females_log_iqr_winsor': 'Marginal Rural Females'
            })

            # Plot
            st.subheader("Grouped Bar Chart")
            fig = px.bar(
                melted,
                x='state',
                y='Average Log-IQR-Winsorized',
                color='Worker Type',
                barmode='group',
                title='Average Main vs Marginal Rural Female Workers by State',
                labels={'state': 'State'}
            )
            fig.update_layout(
                xaxis_tickangle=-45,
                xaxis={'categoryorder': 'total descending'},
                height=600
            )

            st.plotly_chart(fig)

        except Exception as e:
            st.error(f"❌ Error reading file: {e}")
    else:
        st.info("📁 Please upload a CSV file to proceed.")
