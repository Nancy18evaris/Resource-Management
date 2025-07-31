import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def app():
    st.title("AVERAGE MAIN WORKERS PER STATE")
    st.write("Content for app2")

    # ✅ File uploader must be inside the function
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], key="file_upload_app2")

    if uploaded_file is not None:
        try:
            # Load the dataset
            df = pd.read_csv(uploaded_file)

            # Check if required column exists
            if 'state' in df.columns and 'Main Workers - Total - Persons_log_iqr_winsor' in df.columns:
                
                # Exclude 'UNKNOWN' state rows
                df_filtered = df[df['state'] != 'UNKNOWN']

                # Group by state and calculate average
                workers_by_state = df_filtered.groupby('state')['Main Workers - Total - Persons_log_iqr_winsor'].mean().sort_values(ascending=False)

                # Convert to DataFrame
                workers_by_state_df = workers_by_state.reset_index()
                workers_by_state_df.columns = ['state', 'avg_main_workers']

                # Plot using Plotly
                fig = px.bar(
                    workers_by_state_df,
                    x='state',
                    y='avg_main_workers',
                    title='Average Main Workers per State (Log-Transformed)',
                    color='state',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )

                fig.update_layout(
                    xaxis_title='State',
                    yaxis_title='Avg Main Workers (Log)',
                    xaxis_tickangle=45,
                    showlegend=False
                )

                st.plotly_chart(fig)

                # Optional: Show data table
                st.subheader("Data Summary")
                st.dataframe(workers_by_state_df)
            else:
                st.error("CSV must contain 'state' and 'Main Workers - Total - Persons_log_iqr_winsor' columns.")

        except Exception as e:
            st.error(f"Error loading or processing file: {e}")
    else:
        st.info("Please upload a CSV file to begin.")




