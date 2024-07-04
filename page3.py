import streamlit as st
import pandas as pd
import plotly.express as px

def page_3():

    data = pd.read_csv('cars_mock_data.csv')

    # Chuyển đổi cột 'Purchase Date' thành kiểu datetime
    data['Purchase Date'] = pd.to_datetime(data['Purchase Date'], format='%d/%m/%Y')

    # Thêm cột 'Year' từ 'Purchase Date'
    data['Year'] = data['Purchase Date'].dt.year

    # Title
    st.title('Trực quan hoá dữ liệu về các thương hiệu xe')

    # Biểu đồ độ phổ biến của các hãng xe đối với nam/ nữ
    st.header('Biểu đồ về phổ biến của các thương hiệu xe theo giới tính')

    # Biểu đồ về độ phổ biến cuả các hãng xe cho nam giới
    popular_cars_man = data[data['Buyer Gender'] == 'Male']['Make'].value_counts().reset_index()
    popular_cars_man.columns = ['Make', 'Count']
    fig = px.bar(popular_cars_man, x='Make', y='Count', title='Độ phổ biến của các thương hiệu xe cho nam giới')
    st.plotly_chart(fig)

    # Biểu đồ độ phổ biến của các hãng xe cho nữ giới
    popular_cars_woman = data[data['Buyer Gender'] == 'Female']['Make'].value_counts().reset_index()
    popular_cars_woman.columns = ['Make', 'Count']
    fig = px.bar(popular_cars_woman, x='Make', y='Count', title='Độ phổ biến của các thương hiệu xe cho nữ giới')
    st.plotly_chart(fig)
    
    # Biểu đồ độ phổ biến của các hãng xe theo quốc gia
    st.header('Biểu đồ về độ phổ biến của các thương hiệu xe theo quốc gia')

    # Lọc dữ liệu theo quốc gia
    selected_country = st.selectbox('Chọn quốc gia', data['Country'].unique())
    filtered_data = data[data['Country'] == selected_country]

    brand_counts = filtered_data['Make'].value_counts().reset_index()
    brand_counts.columns = ['Make', 'Count']
    fig = px.bar(brand_counts, x='Make', y='Count', title=f'Độ phổ biến của các thương hiệu xe tại  {selected_country}')
    st.plotly_chart(fig)

    # Biểu đồ độ phổ biến của các hãng xe qua các năm
    st.header('Biểu đồ về độ phổ biến của các thương hiệu xe qua từng năm')

    grouped_data = data.groupby(['Year', 'Make']).size().reset_index(name='Count')
    fig = px.line(grouped_data, x='Year', y='Count', color='Make', title='Độ phổ biến của các thương hiệu xe qua từng năm')
    st.plotly_chart(fig)


    # Biểu đồ về tần suất xuất hiện của các buzzword với từng hãng xe
    st.header('Biểu đồ về top 10 buzzword xuất hiện nhiều nhất của từng thương hiệu xe')

    brands = data['Make'].unique().tolist()
    selected_brand = st.selectbox('Chọn thương hiệu xe:', brands, key='0')

    filtered_data = data[data['Make'] == selected_brand]
    buzzword_counts = filtered_data['Buzzword'].value_counts()

    buzzword_counts_df = pd.DataFrame(buzzword_counts).head(10).reset_index()
    buzzword_counts_df.columns = ['Buzzword', 'Count']

    fig = px.bar(buzzword_counts_df, x='Buzzword', y='Count', title=f'Top 10 Buzzword xuất hiện nhiều nhất của hãng {selected_brand}')
    st.plotly_chart(fig)

    # Biểu đồ về độ phổ biến của các màu sắc của từng hãng xe
    st.header('Biểu đồ về độ phổ biến của các màu sắc theo từng thương hiệu xe')

    selected_brand = st.selectbox('Chọn thương hiệu xe:', brands, key='1')
    filtered_data = data[data['Make'] == selected_brand]

    color_mapping = {
        'Red': '#FF0000',
        'Blue': '#0000FF',
        'Green': '#008000',
        'Aquamarine': '#7FFFD4',
        'Crimson': '#DC143C',
        'Fuscia': '#FF00FF',
        'Goldenrod': '#FCD667',
        'Indigo': '#4F69C6',
        'Khaki': '#F0E68C',
        'Maroon': '#800000',
        'Mauv': '#E0B0FF',
        'Orange': '#FF681F',
        'Pink': '#FFC0CB',
        'Puce': '#CC8899',
        'Purple': '#660099',
        'Teal': '#008080',
        'Turquoise': '#30D5C8',
        'Violet': '#240A40',
        'Yellow': '#FFFF00'
    }

    brand_color_popularity = filtered_data.groupby(['Make', 'Color']).size()\
        .reset_index(name='Count')
    fig = px.bar(brand_color_popularity, x='Make', y='Count', color='Color',
                title=f'Độ phổ biến của thương hiệu {selected_brand} theo màu sắc',
                color_discrete_map=color_mapping)  
    st.plotly_chart(fig)
