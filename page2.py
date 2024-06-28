import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def page_2():
    # Load data
    data = pd.read_csv('cars_mock_data.csv')

    # Convert 'Purchase Date'
    data['Purchase Date'] = pd.to_datetime(data['Purchase Date'], format='%d/%m/%Y')
    data['Year'] = data['Purchase Date'].dt.year

    # Title
    st.title('Chủ đề : Vận tốc của các xe : bao gồm vận tốc lớn nhất \
             và thời gian ngắn nhất để xe đạt vận tốc 60 dặm/giờ')

    # # Hiển thị dữ liệu
    # st.header('Speed and Time to Reach 60')
    # if all(col in data.columns for col in ['Make', 'Model', 'Nickname', 'Top Speed', '0-60 Time']):
    #     st.dataframe(data[['Make', 'Model', 'Nickname', 'Top Speed', '0-60 Time']])
        

    # Line chart cho top speed qua chuỗi thời gian
    st.header('Biểu đồ đường biểu diễn tốc độ cao nhất của xe được sản xuất qua các năm')
    top_speed_each_year = data.loc[data.groupby('Year')['Top Speed'].idxmax()]
    fig = px.line(top_speed_each_year, x='Year', y='Top Speed', title='Tốc độ cao nhất qua các năm', markers=True)
    st.plotly_chart(fig)

    # Line chart cho 0-60 Time qua chuỗi thời gian
    st.header('Biểu đồ đường biểu diễn thời gian ngắn nhất đạt vận tốc 60 dặm/h của xe qua các năm')
    fastest_acceleration_each_year = data.loc[data.groupby('Year')['0-60 Time'].idxmin()]
    fig = px.line(fastest_acceleration_each_year, x='Year', y='0-60 Time', title='Thời gian ngắn nhất đạt 60 dặm/h qua các năm', markers=True)
    st.plotly_chart(fig)

    # Top 5 hãng sản xuất với vận tốc trung bình của các xe cao nhất
    st.header("Biểu đồ cột biểu diễn top 5 hãng sản xuất xe có vận tốc trung bình của các xe cao nhất")
    avg_top_speed = data.groupby('Make')['Top Speed'].mean().nlargest(5).reset_index()
    fig = px.bar(avg_top_speed, x='Make', y='Top Speed', title="Top 5 hãng sản xuất xe có vận tốc trung bình cao nhất")
    st.plotly_chart(fig)

    # Top 5 hãng sản xuất với thời gian đạt được vận tốc 60 dặm/giờ của các xe ngắn nhát
    st.header("Biểu đồ cột biểu diễn top 5 hãng sản xuất xe có thời gian đạt được vận tốc 60 dặm/giờ ngắn nhất")
    avg_060_time = data.groupby('Make')['0-60 Time'].mean().nsmallest(5).reset_index()
    fig = px.bar(avg_060_time, x='Make', y='0-60 Time', title="Top 5 hãng sản xuất xe có thời gian đạt được vận tốc 60 dặm/giờ ngắn nhất")
    st.plotly_chart(fig)

    # Tương quan giữa tốc độ lớn nhất và thời gian ngắn nhất đạt vận tốc 60 dặm/giờ
    st.header('Biểu đồ phân tán thể hiện tương quan giữa tốc độ lớn nhất và thời gian ngắn nhất đạt vận tốc 60 dặm/giờ')
    top_speed_each_year = data.loc[data.groupby('Year')['Top Speed'].idxmax()]
    fastest_acceleration_each_year = data.loc[data.groupby('Year')['0-60 Time'].idxmin()]
    combined = pd.concat([top_speed_each_year, fastest_acceleration_each_year]).drop_duplicates(subset=['Year'])
    fig = px.scatter(combined, x='0-60 Time', y='Top Speed', title='Tương quan giữa tốc độ lớn nhất và thời gian ngắn nhất')
    # line from top-right to bottom-left
    fig.add_shape(
        type="line",
        x0=combined['0-60 Time'].min(), y0=combined['Top Speed'].max(),
        x1=combined['0-60 Time'].max(), y1=combined['Top Speed'].min(),
        line=dict(color="Red", width=2, dash="dash")
    )
    st.plotly_chart(fig)

    # Vận tốc trung bình của các dòng xe dựa theo lứa tuổi mua
    st.header('Biểu đồ đường biểu diễn vận tốc trung bình của các dòng xe dựa theo lứa tuổi mua')
    age_speed_avg = data.groupby('Buyer Age')['Top Speed'].mean().reset_index()
    fig = px.line(age_speed_avg, x='Buyer Age', y='Top Speed', title='Vận tốc trung bình theo lứa tuổi mua')
    st.plotly_chart(fig)

    # tỉ lệ nam và nữ với những dòng xe có thời gian đạt được vận tốc 60 dặm/giờ ít hơn 5 giây
    st.header("Biểu đồ tròn thể hiện tỉ lệ nam và nữ với những dòng xe có thời gian đạt được vận tốc 60 dặm/giờ ít hơn 5 giây")
    fast_cars = data[data['0-60 Time'] < 5]
    gender_distribution = fast_cars['Buyer Gender'].value_counts().reset_index()
    gender_distribution.columns = ['Gender', 'Count']
    fig = px.pie(gender_distribution, names='Gender', values='Count', title="Tỉ lệ")
    st.plotly_chart(fig)

    # Tương quan giữa giá xe và vận tốc lớn nhất
    st.header('Biểu đồ phân tán thể hiện tương quan giữa giá xe và vận tốc lớn nhất')
    filtered_data = data[(data['Sale Price'] >= 20000) & (data['Sale Price'] <= 100000)]
    selected_indices = np.linspace(0, len(filtered_data)-1, num=10, dtype=int)
    selected_data = filtered_data.iloc[selected_indices]
    fig = px.scatter(selected_data, x='Sale Price', y='Top Speed', title='Tương quan giữa giá xe và vận tốc lớn nhất')
    fig.add_shape(
        type="line",
        x0=selected_data['Sale Price'].min(), y0=selected_data['Top Speed'].min(),
        x1=selected_data['Sale Price'].max(), y1=selected_data['Top Speed'].max(),
        line=dict(color="Red", width=2, dash="dash")
    )
    st.plotly_chart(fig)





   