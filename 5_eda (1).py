import pandas as pd
import numpy as np

df = pd.read_csv(r"M:\ResourceManagement\after_nlp_mlb.csv")
pd.set_option('display.max_columns', None)
df.head(5)

df.drop(columns=['Unnamed: 0'], inplace = True)

row_count = df.shape[0]
print("Number of rows:", row_count)

print("Number of rows:", len(df))

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# 1. Basic Structure
print("🔹 DataFrame Shape:", df.shape)
print("\n🔹 Column Types:\n", df.dtypes)

# 2. Missing Values
print("\n🔹 Missing Values:\n", df.isnull().sum())

# 3. Summary Statistics for Numerical Columns
print("\n🔹 Summary Statistics:\n", df.describe())

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# One-hot encode the states column
states_encoded = pd.get_dummies(df['state'], prefix='state')

# Select industry columns (make sure these are numeric)
industry_cols = ['retail', 'poultry', 'agriculture', 'manufacturing', 'service', 'sale',
                 'organizations', 'banking', 'animal',
                 'production', 'pharmaceutical', 'cattle', 'textiles',
                 'telecommunications',  'transport', 'food', 'construction',
                 'education', 'insurance']

industries = df[industry_cols]

# Combine encoded states and industry columns
df_combined = pd.concat([states_encoded, industries], axis=1)

# Calculate correlation matrix
corr_matrix = df_combined.corr()

# Plot heatmap
plt.figure(figsize=(16, 12))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap - States and Industry Sectors', fontsize=16)
plt.tight_layout()
plt.show()

#1."Finding the average of Banking sector over states"
state_banking_avg = df.groupby('state')['banking'].mean().sort_values(ascending=False)
state_banking_avg

import matplotlib.pyplot as plt

state_banking_avg.head(10).plot(kind='bar', figsize=(10, 5), color='skyblue')
plt.title('Avg of Top 10 States in Banking')
plt.ylabel('Total Banking Value')
plt.xlabel('State')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Group by state and compute mean
# Step 0: Exclude rows where state == 'UNKNOWN'
df_filtered = df[df['state'] != 'UNKNOWN']
workers_by_state = df_filtered.groupby('state')['Main Workers - Total - Persons_log_iqr_winsor'].mean().sort_values(ascending=False)
print(workers_by_state.head())

#2. "Average of Main workers across states
import plotly.express as px

# Step 0: Exclude rows where state == 'UNKNOWN'
df_filtered = df[df['state'] != 'UNKNOWN']

# Convert the Series to a DataFrame and rename columns
workers_by_state_df = workers_by_state.reset_index()
workers_by_state_df.columns = ['state', 'avg_main_workers']

# Plot the bar chart
fig = px.bar(
    workers_by_state_df,
    x='state',
    y='avg_main_workers',
    title='Average Main Workers per State (Log-Transformed)',
    color='state',  # Optional: for distinct colors per state
    color_discrete_sequence=px.colors.qualitative.Set3
)

# Improve layout
fig.update_layout(
    xaxis_title='State',
    yaxis_title='Avg Main Workers (Log)',
    xaxis_tickangle=45,
    showlegend=False
)

fig.show()

# 3. "Computing the ratio of the Female Working rate between urban and rural"
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Compute mean values
rural_female_mean = df['Main Workers - Rural - Females_log_iqr_winsor'].mean()
urban_female_mean = df['Main Workers - Urban - Females_log_iqr_winsor'].mean()

# Step 2: Compute and print the ratio
if urban_female_mean != 0:
    ratio = rural_female_mean / urban_female_mean
    print(f"Rural to Urban Female Working Rate Ratio (log scale): {ratio:.2f}")
else:
    print("Urban female mean is zero, cannot compute ratio.")

# Step 3: Print who has higher rate
if rural_female_mean > urban_female_mean:
    print("Female working rate is higher in rural areas.")
elif urban_female_mean > rural_female_mean:
    print("Female working rate is higher in urban areas.")
else:
    print("Female working rate is the same in both rural and urban areas.")

# Step 4: Plotting the bar chart
labels = ['Rural Females', 'Urban Females']
values = [rural_female_mean, urban_female_mean]

plt.figure(figsize=(6, 4))
plt.bar(labels, values, color=['skyblue', 'salmon'])
plt.title('Female Working Rate (log_iqr_winsor)')
plt.ylabel('Log-IQR-Winsorized Value')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

#4.Find the State with highest average Main Rural Female Workers and the
#State with highest average Marginal Rural Female Workers
# Step 0: Exclude rows where state == 'UNKNOWN'
df_filtered = df[df['state'] != 'UNKNOWN']

# Step 1: Group by 'state' and calculate the mean for both columns
state_means = df_filtered.groupby('state')[
    ['Main Workers - Rural - Females_log_iqr_winsor',
     'Marginal Workers - Rural - Females_log_iqr_winsor']
].mean()

# Step 2: Find the state with max average for each column
max_main_worker_state = state_means['Main Workers - Rural - Females_log_iqr_winsor'].idxmax()
max_main_worker_value = state_means['Main Workers - Rural - Females_log_iqr_winsor'].max()

max_marginal_worker_state = state_means['Marginal Workers - Rural - Females_log_iqr_winsor'].idxmax()
max_marginal_worker_value = state_means['Marginal Workers - Rural - Females_log_iqr_winsor'].max()

# Step 3: Display results
print(f"State with highest average Main Rural Female Workers (log scale): {max_main_worker_state} ({max_main_worker_value:.2f})")
print(f"State with highest average Marginal Rural Female Workers (log scale): {max_marginal_worker_state} ({max_marginal_worker_value:.2f})")

import plotly.express as px
import pandas as pd

# Step 0: Exclude rows where state is 'UNKNOWN'
df_filtered = df[df['state'] != 'UNKNOWN']

# Step 1: Group by state and compute mean for both columns
state_means = df_filtered.groupby('state')[
    ['Main Workers - Rural - Females_log_iqr_winsor',
     'Marginal Workers - Rural - Females_log_iqr_winsor']
].mean().reset_index()

# Step 2: Melt the DataFrame for easy plotting
state_means_melted = state_means.melt(
    id_vars='state',
    value_vars=['Main Workers - Rural - Females_log_iqr_winsor', 'Marginal Workers - Rural - Females_log_iqr_winsor'],
    var_name='Worker Type',
    value_name='Average Log-IQR-Winsorized'
)

# Step 3: Rename for prettier labels
state_means_melted['Worker Type'] = state_means_melted['Worker Type'].replace({
    'Main Workers - Rural - Females_log_iqr_winsor': 'Main Rural Females',
    'Marginal Workers - Rural - Females_log_iqr_winsor': 'Marginal Rural Females'
})

# Step 4: Plot grouped bar chart
fig = px.bar(
    state_means_melted,
    x='state',
    y='Average Log-IQR-Winsorized',
    color='Worker Type',
    barmode='group',
    title='Average Main vs Marginal Rural Female Workers by State',
    labels={'state': 'State', 'Average Log-IQR-Winsorized': 'Average Worker Rate (log scale)'}
)

fig.update_layout(
    xaxis_tickangle=-45,
    xaxis={'categoryorder': 'total descending'},
    height=600
)

fig.show()

#5. Computing the ratio of Agriculture over states

# Step 0: Exclude rows where state is 'UNKNOWN'
df_filtered = df[df['state'] != 'UNKNOWN']

# Step 1: Compute average agriculture value per state (already done)
state_agriculture_avg = df.groupby('state')['agriculture'].mean().sort_values(ascending=False)

# Step 2: Compute ratio (each state's average as a fraction of total average sum)
state_agriculture_ratio = state_agriculture_avg / state_agriculture_avg.sum()

#5. "Computing the ratio of Agriculture over states"
# Step 0: Exclude rows where the state is 0
df_filtered = df[df['state'] != 'UNKNOWN']

# Step 1: Compute average agriculture value per state
state_agriculture_avg = df_filtered.groupby('state')['agriculture'].mean().sort_values(ascending=False)

# Step 2: Compute ratio (each state's average as a fraction of total average sum)
state_agriculture_ratio = state_agriculture_avg / state_agriculture_avg.sum()

import plotly.express as px

df_filtered = df[df['state'] != 'UNKNOWN']

# Convert to DataFrame for pie chart
ratio_df = state_agriculture_ratio.reset_index()
ratio_df.columns = ['State', 'Ratio']

fig = px.pie(
    ratio_df,
    names='State',
    values='Ratio',
    title='State-wise Ratio of Average Agriculture',
    hole=0.3  # Optional: donut-style chart
)

fig.show()

#6. "Finding in which industry Puducherry excels"
import plotly.express as px
df_filtered = df[df['state'] != 'UNKNOWN']

# Step 1: Filter for Puducherry
pudu_df = df_filtered[df_filtered['state'].str.lower() == 'puducherry']

# Step 2: Identify industry columns
industry_cols = [col for col in df.columns if col not in ['Unnamed: 0', 'State Code',	'District Code',	'Division',	'Group',	'Class',
'Main Workers - Total - Persons_log_iqr_winsor',	'Main Workers - Total - Males_log_iqr_winsor','Main Workers - Total - Females_log_iqr_winsor',
'Main Workers - Rural - Persons_log_iqr_winsor',	'Main Workers - Rural - Males_log_iqr_winsor',	'Main Workers - Rural - Females_log_iqr_winsor',
'Main Workers - Urban - Persons_log_iqr_winsor',	'Main Workers - Urban - Males_log_iqr_winsor',	'Main Workers - Urban - Females_log_iqr_winsor',
'Marginal Workers - Total - Persons_log_iqr_winsor',	'Marginal Workers - Total - Males_log_iqr_winsor',	'Marginal Workers - Total - Females_log_iqr_winsor',
'Marginal Workers - Rural - Persons_log_iqr_winsor',	'Marginal Workers - Rural - Males_log_iqr_winsor',	'Marginal Workers - Rural - Females_log_iqr_winsor',
'Marginal Workers - Urban - Persons_log_iqr_winsor',	'Marginal Workers - Urban - Males_log_iqr_winsor',	'Marginal Workers - Urban - Females_log_iqr_winsor',
'tokens_no_stop',	'manual_token_present',	'matched_manual_tokens', 'state',	'district', 'state_count', 'district_count', 'Total_Workers', 'Total_Female_Workers', 'lon',
'lat', 'Total_Male_Workers']]

# Step 3: Calculate average value for each industry in Puducherry
industry_avg = pudu_df[industry_cols].mean().sort_values(ascending=False)

# Step 4: Create a DataFrame for plotting
industry_avg_df = industry_avg.reset_index()
industry_avg_df.columns = ['Industry', 'Average Value']

# Step 5: Plot using Plotly
fig = px.bar(
    industry_avg_df,
    x='Industry',
    y='Average Value',
    title='Average Industry Performance in Puducherry',
    labels={'Average Value': 'Avg Value'},
    color='Average Value',
    color_continuous_scale='Blues'
)
top_industry = industry_avg.idxmax()
top_value = industry_avg.max()
print(f"Puducherry excels in '{top_industry}' with an average value of {top_value:.2f}.")
fig.update_layout(xaxis_tickangle=-45)
fig.show()

#7. "Finding in which industry each state excels and and created an animated interactive chart"
import pandas as pd
import plotly.express as px

df_filtered = df[df['state'] != 'UNKNOWN']

industries = ['retail', 'poultry', 'agriculture', 'manufacturing', 'service', 'sale',
                 'organizations', 'banking', 'animal',
                 'production', 'pharmaceutical', 'cattle', 'textiles',
                 'telecommunications',  'transport', 'food', 'construction',
                 'education', 'insurance']

# Step 1: Group by state and compute mean only for selected industries
state_industry_avg = df_filtered.groupby('state')[industries].mean()

# Step 2: Compute total value across all industries per state
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

# Step 5: Create animated bar chart
fig = px.bar(
    industry_ratios_long,
    x='state',
    y='ratio',
    color='industry',
    animation_frame='industry',
    title='Animated: Industry Ratio by State',
    labels={'ratio': 'Industry Ratio', 'state': 'State'},
    range_y=[0, 1],  # consistent y-axis across frames
    height=600
)

fig.update_layout(xaxis_tickangle=-45)
fig.show()

#8."Comparison of Rural and Urban , Main and Marginal Working Woman"
import pandas as pd
import plotly.express as px

# Step 0: Exclude 'UNKNOWN' states
df_filtered = df[df['state'] != 'UNKNOWN']

# Step 1: Select relevant columns and compute mean per state
columns_of_interest = [
    'Main Workers - Rural - Females_log_iqr_winsor',
    'Marginal Workers - Rural - Females_log_iqr_winsor',
    'Main Workers - Urban - Females_log_iqr_winsor',
    'Marginal Workers - Urban - Females_log_iqr_winsor'
]

state_worker_means = df_filtered.groupby('state')[columns_of_interest].mean().reset_index()

# Step 2: Melt to long format
melted = state_worker_means.melt(
    id_vars='state',
    var_name='Worker Type',
    value_name='Average Log-IQR-Winsorized'
)

# Step 3: Split 'Worker Type' into 'Worker' and 'Area' for faceted plotting
melted['Worker Category'] = melted['Worker Type'].apply(lambda x: 'Main' if 'Main' in x else 'Marginal')
melted['Area'] = melted['Worker Type'].apply(lambda x: 'Rural' if 'Rural' in x else 'Urban')

# Step 4: Combine area and worker category for better labeling
melted['Group'] = melted['Area'] + ' - ' + melted['Worker Category']

# Step 5: Plot interactive bar chart
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

fig.show()

max_row = melted.loc[melted['Average Log-IQR-Winsorized'].idxmax()]
print(f"Highest percentage of working women (log scale):\n"
      f"State: {max_row['state']}, Type: {max_row['Group']}, Value: {max_row['Average Log-IQR-Winsorized']:.2f}")

#9. "Comparison of Male and Female Workers"
import pandas as pd
import plotly.express as px

# === Step 1: Define coordinates for each state ===
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

# === Step 2: Sum Female and Male worker columns ===
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

df['Total_Female_Workers'] = df[cols_female].sum(axis=1)
df['Total_Male_Workers'] = df[cols_male].sum(axis=1)
df['Total_Workers'] = df['Total_Female_Workers'] + df['Total_Male_Workers']

# === Step 3: Drop existing lat/lon if any, then merge coordinates ===
df = df.drop(columns=['lat', 'lon'], errors='ignore')
df = df.merge(coord_df, on='state', how='left')

# === Step 4: Create Bubble Map Traces ===
fig = px.scatter_geo(
    df,
    lat='lat',
    lon='lon',
    text='state',
    size='Total_Female_Workers',
    color_discrete_sequence=['purple'],
    hover_name='state',
    hover_data={'Total_Female_Workers': True, 'lat': False, 'lon': False},
    projection='natural earth'
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

# === Step 5: Layout and Dropdown for interactive filtering ===
fig.update_geos(
    scope='asia',
    center=dict(lat=22, lon=80),
    projection_scale=5,
    showland=True,
    landcolor="lightgray"
)

fig.update_layout(
    title='Geographical Comparison of Male vs Female vs Total Workers Across Indian States',
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

fig.show()

print(df[['state', 'Total_Female_Workers', 'Total_Male_Workers']].head(10))
print(df[['Total_Female_Workers', 'Total_Male_Workers']].describe())

print(df[df['lat'].isna()]['state'].unique())

df.to_csv("after_eda.csv")











