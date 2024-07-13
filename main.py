import streamlit as st
from page1 import page_1
from page2 import page_2
from page3 import page_3

def main():
    st.title("Visualize lab 3")

    menu = ["Giá xe của từng hãng qua các năm", "Chủ đề về vận tốc của các xe", "Chủ đề về thương hiệu xe"]
    choice = st.sidebar.selectbox("Chọn trang", menu)

    if choice == "Giá xe của từng hãng qua các năm":
        page_1()
    elif choice == "Chủ đề về vận tốc của các xe":
        page_2()
    elif choice == "Chủ đề về thương hiệu xe":
        page_3()


if __name__ == "__main__":
    main()
