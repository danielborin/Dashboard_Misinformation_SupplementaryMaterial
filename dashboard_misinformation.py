import streamlit as st
import pandas as pd
from functions import *

# Set the configuration
st.set_page_config(layout='wide')

# -----------------
# ---- Sidebar ----
# -----------------

# # Set the title and author's name
# st.sidebar.title('Misinfromation Research')
# st.sidebar.write('by [Daniel Borin](https://danielborin.github.io)')


# year_ini = st.sidebar.slider('Start Date', 1994, 2024, 1994, 1)
# year_end = st.sidebar.slider('End Date', 1994, 2024, 2024, 1)

# # Ensure the year_min is less than or equal to year_end
# if year_ini > year_end:
#     st.sidebar.warning("Start Date cannot be later than End Date. Adjusting End Date to match Start Date.")
#     year_end = year_ini


st.title("Supplementary Material: Thirty Years of Misinformation Research: A team science perspective (1994-2024)")

st.write("""
This dashboard provides a visual and interactive platform which follows the paper **"Thirty Years of Misinformation Research: A team science perspective (1994--2024)"** by **Daniel Borin**, **Diego Fregolent Mendes de Oliveira** and **Brian Uzzi**. 
    
For more information, visit the [author's homepage](https://danielborin.github.io).

""")

st.divider()
st.header('Composition over the years')
# Get the selected years
year_ini, year_end = st.slider(
    'Which years are you interested in?',
    min_value=1994,
    max_value=2024,
    value=[1994, 2024])

# Now you can use year_min and year_end safely, knowing year_min <= year_end
st.write(f'Selected Range: {year_ini} - {year_end}')



dataset = pd.read_excel('Data//full_core_dataset_new.xlsx')
df = dataset[(dataset['Publication Year'] >= year_ini) & (dataset['Publication Year'] <= year_end)]

col1, col2 = st.columns(2)

fig = plot_veen_diagram(df)
col1.pyplot(fig, width=600)

with col2:
    # Define the dictionary
    keyword_map = {
        'misinformation': 'Misinformation',
        'fake_news': 'Fake News',
        'disinformation': 'Disinformation',
        'All Keywords': 'All Keywords'
    }

    # Available options (capitalized for display in multiselect)
    capitalized_options = list(keyword_map.values())

    # Corresponding lowercase options (for use in plotting)
    lowercase_options = list(keyword_map.keys())

    selected_keywords = st.multiselect(
        'Which keywords would you like to view?',
        capitalized_options,
        capitalized_options
    )

    selected_keywords_lowercase = [key for key, value in keyword_map.items() if value in selected_keywords]
    colors_dic = {
        'slateblue': '#020035',
        'deepskyblue': '#00BFFF',
        'violet': '#9a0eea',
    }

    df_pivot = split_keyword(df)

    st.line_chart(df_pivot, x = 'Publication Year', y =  selected_keywords_lowercase, height = "stretch", x_label='Year', y_label='Number of Publications')#, color=list(colors_dic.values()))

st.divider()

st.header('Team science Analysis (All years 1994-2024)')

# col3, col4, col5 = st.columns(3)
# col6, col7, col8 = st.columns(3)

# col3, col4 = st.columns(2)
# col5, col6 = st.columns(2)
# col7, col8 = st.columns(2)

# col3 = st.columns(1)
# col4 = st.columns(1)
# col5 = st.columns(1)
# col6 = st.columns(1)
# col7 = st.columns(1)
# col8 = st.columns(1)

# with col3:
#     df3 = pd.read_excel('Data//df_authors_pub_cit_analysis.xlsx')
#     st.dataframe(df3)

# with col4:
#     df4 = pd.read_excel('Data//df_number_authors_pub_cit_analysis.xlsx')
#     st.dataframe(df4)

# with col5:
#     df5 = pd.read_excel('Data//df_countries_pub_cit_analysis.xlsx')
#     st.dataframe(df5)

# with col6:
#     df6 = pd.read_excel('Data//df_number_countries_pub_cit_analysis.xlsx')
#     st.dataframe(df6)

# with col7:
#     df7 = pd.read_excel('Data//df_affiliation_pub_cit_analysis.xlsx')
#     st.dataframe(df7)

# with col8:
#     df8 = pd.read_excel('Data//df_number_affiliations_pub_cit_analysis.xlsx')
#     st.dataframe(df8)

st.subheader('Authors')
df3 = pd.read_excel('Data//df_authors_pub_cit_analysis.xlsx')
st.dataframe(df3)
st.subheader('Number of Authors')
df4 = pd.read_excel('Data//df_number_authors_pub_cit_analysis.xlsx')
st.dataframe(df4)
st.subheader('Countries')
df5 = pd.read_excel('Data//df_countries_pub_cit_analysis.xlsx')
st.dataframe(df5)
st.subheader('Number of Countries')
df6 = pd.read_excel('Data//df_number_countries_pub_cit_analysis.xlsx')
st.dataframe(df6)
st.subheader('Institituions')
df7 = pd.read_excel('Data//df_affiliation_pub_cit_analysis.xlsx')
st.dataframe(df7)
st.subheader('Number of Institutions')
df8 = pd.read_excel('Data//df_number_affiliations_pub_cit_analysis.xlsx')
st.dataframe(df8)