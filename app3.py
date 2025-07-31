import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def app():
    st.title("FEMALE WORKING RATE RURAL VS URBAN - MAIN WORKERS")
    st.write("Content for app3")

    # ✅ File uploader inside the app function
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], key="file_upload_app3")

    if uploaded_file is not None:
        try:
            # Load the dataset
            df = pd.read_csv(uploaded_file)

            # Step 1: Compute mean values
            rural_col = 'Main Workers - Rural - Females_log_iqr_winsor'
            urban_col = 'Main Workers - Urban - Females_log_iqr_winsor'

            if rural_col in df.columns and urban_col in df.columns:
                rural_female_mean = df[rural_col].mean()
                urban_female_mean = df[urban_col].mean()

                # Step 2: Compute and display the ratio
                if urban_female_mean != 0:
                    ratio = rural_female_mean / urban_female_mean
                    st.subheader("Rural to Urban Female Working Rate Ratio (Log Scale)")
                    st.metric(label="Rural/Urban Ratio", value=f"{ratio:.2f}")
                else:
                    st.error("Urban female mean is zero, cannot compute ratio.")

                # Step 3: Determine and display who has a higher rate
                st.subheader("Comparison Summary")
                if rural_female_mean > urban_female_mean:
                    st.success("✅ Female working rate is **higher in rural areas**.")
                elif urban_female_mean > rural_female_mean:
                    st.success("✅ Female working rate is **higher in urban areas**.")
                else:
                    st.info("✅ Female working rate is **the same** in both rural and urban areas.")

                # Step 4: Bar Chart
                st.subheader("Bar Chart: Female Working Rate (Log Transformed)")
                labels = ['Rural Females', 'Urban Females']
                values = [rural_female_mean, urban_female_mean]

                fig, ax = plt.subplots(figsize=(6, 4))
                ax.bar(labels, values, color=['skyblue', 'salmon'])
                ax.set_title('Female Working Rate (log_iqr_winsor)')
                ax.set_ylabel('Log-IQR-Winsorized Value')
                ax.grid(axis='y', linestyle='--', alpha=0.5)
                st.pyplot(fig)
            else:
                st.error(f"Required columns '{rural_col}' and/or '{urban_col}' not found in the uploaded CSV.")
        except Exception as e:
            st.error(f"Error processing file: {e}")
    else:
        st.info("📁 Please upload a CSV file to begin.")
