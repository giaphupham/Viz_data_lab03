import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import plotly.express as px

def page_5():
    # Tải dữ liệu
    data = pd.read_csv('cars_mock_data.csv')

    # Chuyển đổi cột 'Purchase Date' thành kiểu datetime
    data['Purchase Date'] = pd.to_datetime(data['Purchase Date'], format='%d/%m/%Y')
    
    # Thêm cột 'Year' từ 'Purchase Date'
    data['Year'] = data['Purchase Date'].dt.year
    
    # Lọc các cột cần thiết
    df = data[['Buyer Age', 'Discount', 'Top Speed', '0-60 Time', 'Sale Price']].dropna()

    # Phân chia dữ liệu thành đầu vào (X) và đầu ra (y)
    X = df[['Buyer Age', 'Discount', 'Top Speed', '0-60 Time']]
    y = df['Sale Price']

    # Chia dữ liệu thành tập huấn luyện và tập kiểm tra
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Khởi tạo mô hình Gradient Boosting với GridSearchCV để tìm tham số tốt nhất
    param_grid = {
        'n_estimators': [100, 200, 300],
        'learning_rate': [0.01, 0.05, 0.1],
        'max_depth': [3, 5, 7],
        'min_samples_split': [2, 5, 10]
    }
    
    model = GradientBoostingRegressor(random_state=42)
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, n_jobs=-1, scoring='r2')
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    st.title('Dự đoán giá bán lại của xe mới')

    st.subheader('Kết quả đánh giá mô hình')
    st.write(f'Mean Squared Error: {mse}')
    st.write(f'R2 Score: {r2}')
    
    st.write(f'Best parameters: {grid_search.best_params_}')

    # Hiển thị biểu đồ so sánh giá trị thực và giá trị dự đoán
    st.write('Biểu đồ so sánh giá trị thực và giá trị dự đoán')
    comparison_df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred}).sample(500)
    fig = px.scatter(comparison_df, x='Actual', y='Predicted', title='Comparison of Actual and Predicted Values')
    st.plotly_chart(fig)

    # Giao diện nhập liệu để dự đoán giá bán lại
    st.subheader('Dự đoán giá bán lại của xe mới')
    buyer_age = st.number_input('Tuổi người mua', min_value=18, max_value=100, value=30)
    discount = st.slider('Mức giảm giá', min_value=0.0, max_value=1.0, value=0.2)
    top_speed = st.number_input('Tốc độ tối đa (mph)', min_value=50, max_value=300, value=150)
    zero_to_sixty = st.number_input('Thời gian tăng tốc từ 0-60 dặm/giờ (giây)', min_value=2.0, max_value=10.0, value=6.0)

    # Tạo dataframe cho đầu vào dự đoán
    input_data = pd.DataFrame({
        'Buyer Age': [buyer_age],
        'Discount': [discount],
        'Top Speed': [top_speed],
        '0-60 Time': [zero_to_sixty]
    })

    # Dự đoán giá bán lại
    predicted_resell_price = best_model.predict(input_data)[0]
    st.write(f'Giá bán lại dự đoán: ${predicted_resell_price:,.2f}')

