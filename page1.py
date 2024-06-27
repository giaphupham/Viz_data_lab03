import streamlit as st
import pandas as pd
import plotly.express as px


def page_1():
    data = pd.read_csv('cars_mock_data.csv')

    # Chuyển đổi cột 'Purchase Date' thành kiểu datetime
    data['Purchase Date'] = pd.to_datetime(data['Purchase Date'], format='%d/%m/%Y')

    # Thêm cột 'Year' từ 'Purchase Date'
    data['Year'] = data['Purchase Date'].dt.year

    # Nhóm dữ liệu theo năm và tính giá trị trung bình của 'Sale Price'
    data_grouped = data.groupby(['Year', 'Make']).agg({'Sale Price': 'mean'}).reset_index()

    # Title
    st.title('Trực quan hoá dữ liệu giá xe của từng hãng qua các năm')

    # Hiển thị dữ liệu
    st.header('Dữ liệu gốc')
    st.dataframe(data)

    # Biểu đồ dòng thời gian giá xe của từng hãng (nhóm theo năm)
    st.header('Biểu đồ dòng thời gian giá xe của từng hãng (nhóm theo năm)')
    fig = px.line(data_grouped, x='Year', y='Sale Price', color='Make', title='Giá xe trung bình theo thời gian')
    st.plotly_chart(fig)

    # Biểu đồ phân phối giá theo các hãng xe (nhóm theo năm)
    st.header('Biểu đồ phân phối giá theo các hãng xe (nhóm theo năm)')
    fig = px.box(data, x='Make', y='Sale Price', title='Phân phối giá xe theo hãng')
    st.plotly_chart(fig)

    # Biểu đồ so sánh giá gốc và giá bán lại
    st.header('Biểu đồ so sánh giá gốc và giá bán lại')
    data['Discounted Price'] = data['Sale Price'] * (1 - data['Discount'])
    fig = px.scatter(data, x='Sale Price', y='Resell Price', color='Make', title='So sánh giá gốc và giá bán lại')
    st.plotly_chart(fig)

    # Biểu đồ số lượng xe bán ra của từng hãng
    st.header('Biểu đồ số lượng xe bán ra của từng hãng')
    sales_count = data['Make'].value_counts().reset_index()
    sales_count.columns = ['Make', 'Count']
    fig = px.bar(sales_count, x='Make', y='Count', title='Số lượng xe bán ra của từng hãng')
    st.plotly_chart(fig)

    # Lọc dữ liệu theo hãng
    st.header('Lọc dữ liệu theo hãng xe')
    selected_make = st.selectbox('Chọn hãng xe', data['Make'].unique())
    filtered_data = data[data['Make'] == selected_make]
    filtered_data_grouped = data_grouped[data_grouped['Make'] == selected_make]

    st.write(f'Dữ liệu lọc theo hãng {selected_make}')
    st.dataframe(filtered_data)

    st.header(f'Biểu đồ dòng thời gian giá xe của hãng {selected_make} (nhóm theo năm)')
    fig = px.line(filtered_data_grouped, x='Year', y='Sale Price', title=f'Giá xe trung bình của hãng {selected_make} theo thời gian')
    st.plotly_chart(fig)

    st.header(f'Biểu đồ phân phối giá của hãng {selected_make}')
    fig = px.box(filtered_data, y='Sale Price', title=f'Phân phối giá của hãng {selected_make}')
    st.plotly_chart(fig)

    # Biểu đồ so sánh giá gốc và giá bán lại của hãng theo năm với màu gradient
    st.header(f'Biểu đồ so sánh giá gốc và giá bán lại của hãng {selected_make}')
    filtered_data['Discounted Price'] = filtered_data['Sale Price'] * (1 - filtered_data['Discount'])
    fig = px.scatter(
        filtered_data, 
        x='Sale Price', 
        y='Resell Price', 
        title=f'So sánh giá gốc và giá bán lại của hãng {selected_make}',
        color='Year',  # Sử dụng cột Year để xác định màu sắc
        color_continuous_scale=px.colors.sequential.Blues  # Chọn thang màu gradient xanh biển
    )
    st.plotly_chart(fig)

    # Biểu đồ số lượng xe bán ra của hãng cụ thể
    st.header(f'Biểu đồ số lượng xe bán ra của hãng {selected_make} theo model')
    sales_count_specific = filtered_data['Model'].value_counts().reset_index()
    sales_count_specific.columns = ['Model', 'Count']
    fig = px.bar(sales_count_specific, x='Model', y='Count', title=f'Số lượng xe bán ra của hãng {selected_make} theo model')
    st.plotly_chart(fig)
