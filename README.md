INDUSTRIAL HUMAN RESOURCE GEO-VISUALIZATION

📌 Problem Statement

Industrial Human Resource Geo-Visualization is a data-driven analysis project focused on understanding and visualizing the classification of Main and Marginal workers in Rural and urban areas in India. The project aims to update the outdated industrial classification data by gender, section, division, and class of workers. The insights generated will aid policymakers, researchers, and planners in employment forecasting and resource distribution.

🎯 Objectives

Update and modernize the classification of industrial human resources in India. Analyze gender-wise, state-wise, and industry-wise worker distribution. Apply EDA and NLP to extract meaningful insights. Visualize workforce patterns geographically using interactive plots and maps.

🧰 Technologies Used

Category Tools / Libraries Programming - Python Data Manipulation - pandas, NumPy Visualization - matplotlib, seaborn, plotly NLP 'Spacy', transformers (BERT tokenizer) Data Preprocessing - scikit-learn, scipy Others - Jupyter Notebook, Streamlit (for deployment)

🧹 Data Preprocessing

Missing Value Handling: Used imputation methods to fill missing data. Outlier Detection & Handling: IQR (Interquartile Range) Winsorization (to cap extreme outliers) Skewness & Kurtosis Analysis: Applied log1p() transformation for right-skewed data. Feature Transformation: MultiLabelBinarizer for multi-class categorical features. Text preprocessing for NLP tokenization.

🔍 Exploratory Data Analysis (EDA)

Visualizations: Histograms, Bar Charts, KDE plots Gender-wise and industry-wise worker distribution State-wise industrial workforce mapping Statistical Analysis: Distribution insights Skewness and kurtosis values

🧠 NLP Integration

Used the BERT tokenizer for preprocessing industrial classification text: from transformers import AutoTokenizer tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
