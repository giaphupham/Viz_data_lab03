import streamlit as st
import pandas as pd
import plotly.express as px


def page_4():
    data = pd.read_csv('cars_mock_data.csv')

    # Chuyển đổi cột 'Purchase Date' thành kiểu datetime
    data['Purchase Date'] = pd.to_datetime(data['Purchase Date'], format='%d/%m/%Y')

    # Thêm cột 'Year' từ 'Purchase Date'
    data['Year'] = data['Purchase Date'].dt.year

    # Nhóm dữ liệu theo năm và tính giá trị trung bình của 'Sale Price'
    data_grouped = data.groupby(['Year', 'Make']).agg({'Resell Price': 'mean'}).reset_index()

    # Title
    st.title('Trực quan hoá dữ liệu giá bán lại xe của từng hãng qua các năm')

    # Hiển thị dữ liệu
    st.header('Dữ liệu gốc')
    st.dataframe(data)

    # Biểu đồ dòng thời gian giá xe của từng hãng (nhóm theo năm)
    st.header('Biểu đồ dòng thời gian giá bán lại xe của từng hãng (nhóm theo năm)')
    fig = px.line(data_grouped, x='Year', y='Resell Price', color='Make', title='Giá bán lại xe trung bình theo thời gian')
    st.plotly_chart(fig)

    # Biểu đồ phân phối giá theo các hãng xe (nhóm theo năm)
    st.header('Biểu đồ phân phối giá bán lại theo các hãng xe (nhóm theo năm)')
    fig = px.box(data, x='Make', y='Resell Price', title='Phân phối giá xe theo hãng')
    st.plotly_chart(fig)


    # Lọc dữ liệu theo hãng
    st.header('Lọc dữ liệu theo hãng xe')
    selected_make = st.selectbox('Chọn hãng xe', data['Make'].unique())
    filtered_data = data[data['Make'] == selected_make]
    filtered_data_grouped = data_grouped[data_grouped['Make'] == selected_make]

    st.write(f'Dữ liệu lọc theo hãng {selected_make}')
    st.dataframe(filtered_data)

    st.header(f'Biểu đồ dòng thời gian giá bán lại xe của hãng {selected_make} (nhóm theo năm)')
    fig = px.line(filtered_data_grouped, x='Year', y='Resell Price', title=f'Giá xe bán lại trung bình của hãng {selected_make} theo thời gian')
    st.plotly_chart(fig)

    st.header(f'Biểu đồ phân phối giá bán lại của hãng {selected_make}')
    fig = px.box(filtered_data, y='Resell Price', title=f'Phân phối giá bán lại của hãng {selected_make}')
    st.plotly_chart(fig)

    # Biểu đồ so sánh giá gốc và giá bán lại của hãng theo năm với màu gradient
    # Tính toán Loss Ratio cho từng dòng xe
    filtered_data['Loss Ratio'] = (filtered_data['Sale Price'] - filtered_data['Resell Price']) / filtered_data['Sale Price']

    # Tạo ứng dụng Streamlit
    st.header(f'Tỷ lệ lỗ trung bình khi bán lại theo mẫu xe của {selected_make}')

    # Tính tỷ lệ lỗ trung bình theo từng mẫu xe
    average_loss_ratio_model_specific_make = filtered_data.groupby('Model')['Loss Ratio'].mean().reset_index()

    # Tạo biểu đồ bar chart tương tác
    fig_model_specific_make = px.bar(average_loss_ratio_model_specific_make, x='Model', y='Loss Ratio',
                                    title=f'Tỷ lệ lỗ trung bình khi bán lại theo mẫu xe của hãng {selected_make}',
                                    labels={'Loss Ratio': 'Tỷ lệ lỗ trung bình', 'Model': 'Mẫu xe'},
                                    template='plotly')

    # Hiển thị biểu đồ
    st.plotly_chart(fig_model_specific_make)

    # Lọc dữ liệu cho hãng xe cụ thể và loại xe cụ thể
    newcar_option = st.selectbox('Chọn loại xe', ['Xe mới', 'Xe cũ'])
    is_newcar = True if newcar_option == 'Xe mới' else False

    # Lọc dữ liệu cho hãng xe cụ thể và loại xe cụ thể
    df_filtered = data[(data['Make'] == selected_make) & (data['New Car'] == is_newcar)]

    # Tính giá bán trung bình và giá bán lại trung bình theo từng mẫu xe
    average_prices = df_filtered.groupby('Model')[['Sale Price', 'Resell Price']].mean().reset_index()

    # Chuyển đổi dữ liệu sang dạng dài (long format) để sử dụng với plotly express
    average_prices_long = average_prices.melt(id_vars='Model', value_vars=['Sale Price', 'Resell Price'], 
                                            var_name='Price Type', value_name='Price')

    # Tạo biểu đồ bar chart tương tác so sánh giá bán và giá bán lại trung bình
    fig_comparison = px.bar(average_prices_long, x='Model', y='Price', color='Price Type',
                            title=f'So sánh giá bán và giá bán lại trung bình theo mẫu xe của hãng {selected_make} ({newcar_option})',
                            labels={'Price': 'Giá tiền', 'Model': 'Mẫu xe', 'Price Type': 'Loại giá'},
                            barmode='group',
                            template='plotly')

    # Hiển thị biểu đồ
    st.plotly_chart(fig_comparison)

