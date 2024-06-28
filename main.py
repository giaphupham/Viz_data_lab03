from page1 import page_1
from page2 import page_2
import streamlit as st

def main():
    st.title("Visualize lab 3")

    menu = ["Giá xe của từng hãng qua các năm", "Page 2 (chủ đề về vận tốc của các xe)", "Page 3"]
    choice = st.sidebar.selectbox("Chọn trang", menu)

    if choice == "Giá xe của từng hãng qua các năm":
        page_1()
    elif choice == "Page 2 (chủ đề về vận tốc của các xe)":
        page_2()
    elif choice == "Page 3":
        page_1()


if __name__ == "__main__":
    main()
