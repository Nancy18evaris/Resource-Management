import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title("GEOGRAPHICAL COMPARISON OF MALE VS FEMALE VS TOTAL WORKERS ACROSS INDIAN STATES")
    st.write("Content for app9")

    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], key="file_upload_app9")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Step 0: Define coordinates for each state
        state_coords = {
            'WEST BENGAL': [22.9868, 87.8550], 'RAJASTHAN': [27.0238, 74.2179], 'KARNATAKA': [15.3173, 75.7139],
            'TAMIL NADU': [11.1271, 78.6569], 'MAHARASHTRA': [19.7515, 75.7139], 'NCT OF DELHI': [28.7041, 77.1025],
            'KERALA': [10.8505, 76.2711], 'GUJARAT': [22.2587, 71.1924], 'ODISHA': [20.9517, 85.0985],
            'JHARKHAND': [23.6102, 85.2799], 'ASSAM': [26.2006, 92.9376], 'MANIPUR': [24.6637, 93.9063],
            'UTTAR PRADESH': [26.8467, 80.9462], 'ARUNACHAL PRADESH': [28.2180, 94.7278], 'MIZORAM': [23.1645, 92.9376],
            'NAGALAND': [26.1584, 94.5624], 'HIMACHAL PRADESH': [31.1048, 77.1734], 'BIHAR': [25.0961, 85.3131],
            'PUDUCHERRY': [11.9416, 79.8083], 'UTTARKHAND': [30.0668, 79.0193], 'SIKKIM': [27.5330, 88.5122],
            'TRIPURA': [23.9408, 91.9882], 'GOA': [15.2993, 74.1240]
        }

        coord_df = pd.DataFrame(state_coords).T.reset_index()
        coord_df.columns = ['state', 'lat', 'lon']

        if 'state' not in df.columns:
            st.error("The dataset must contain a 'state' column.")
            return

        df['state'] = df['state'].str.upper()

        # Define columns for male and female workers
        cols_female = [
            'Main Workers - Rural - Females_log_iqr_winsor',
            'Marginal Workers - Rural - Females_log_iqr_winsor',
            'Main Workers - Urban - Females_log_iqr_winsor',
            'Marginal Workers - Urban - Females_log_iqr_winsor'
        ]
        cols_male = [
            'Main Workers - Rural - Males_log_iqr_winsor',
            'Marginal Workers - Rural - Males_log_iqr_winsor',
            'Main Workers - Urban - Males_log_iqr_winsor',
            'Marginal Workers - Urban - Males_log_iqr_winsor'
        ]

        missing_cols_female = [col for col in cols_female if col not in df.columns]
        missing_cols_male = [col for col in cols_male if col not in df.columns]

        if missing_cols_female or missing_cols_male:
            st.error(f"Missing columns in dataset:\nFemale columns: {missing_cols_female}\nMale columns: {missing_cols_male}")
            return

        # Calculate totals
        df['Total_Female_Workers'] = df[cols_female].sum(axis=1)
        df['Total_Male_Workers'] = df[cols_male].sum(axis=1)
        df['Total_Workers'] = df['Total_Female_Workers'] + df['Total_Male_Workers']

        df = df.drop(columns=['lat', 'lon'], errors='ignore')
        df = df.merge(coord_df, on='state', how='left')

        # Create the scatter plot
        fig = px.scatter_geo(
            df,
            lat='lat',
            lon='lon',
            text='state',
            size='Total_Female_Workers',
            color_discrete_sequence=['purple'],
            hover_name='state',
            hover_data={'Total_Female_Workers': True, 'lat': False, 'lon': False},
            projection='natural earth',
            title='Female Workers'
        )
        fig.update_traces(name='Female Workers')

        fig.add_trace(px.scatter_geo(
            df,
            lat='lat',
            lon='lon',
            text='state',
            size='Total_Male_Workers',
            color_discrete_sequence=['orange'],
            hover_name='state',
            hover_data={'Total_Male_Workers': True, 'lat': False, 'lon': False},
            projection='natural earth'
        ).data[0])
        fig.data[1].name = 'Male Workers'

        fig.add_trace(px.scatter_geo(
            df,
            lat='lat',
            lon='lon',
            text='state',
            size='Total_Workers',
            color_discrete_sequence=['green'],
            hover_name='state',
            hover_data={'Total_Workers': True, 'lat': False, 'lon': False},
            projection='natural earth'
        ).data[0])
        fig.data[2].name = 'Total Workers'

        fig.update_geos(
            scope='asia',
            center=dict(lat=22, lon=80),
            projection_scale=5,
            showland=True,
            landcolor="lightgray"
        )

        fig.update_layout(
            height=600,
            margin=dict(l=0, r=0, t=50, b=0),
            updatemenus=[
                dict(
                    buttons=[
                        dict(label='Show All', method='update',
                             args=[{'visible': [True, True, True]},
                                   {'title': 'Male, Female and Total Workers'}]),
                        dict(label='Female Only', method='update',
                             args=[{'visible': [True, False, False]},
                                   {'title': 'Female Workers Only'}]),
                        dict(label='Male Only', method='update',
                             args=[{'visible': [False, True, False]},
                                   {'title': 'Male Workers Only'}]),
                        dict(label='Total Only', method='update',
                             args=[{'visible': [False, False, True]},
                                   {'title': 'Total Workers Only'}]),
                    ],
                    direction='down',
                    showactive=True,
                    x=0,
                    y=1.1,
                    xanchor='left',
                    yanchor='top'
                )
            ]
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Please upload a CSV file to display the geographical comparison.")

