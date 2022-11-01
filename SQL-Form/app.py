"""
Login and Sign Up Page using Streamlit and MYSQL
"""

from os import PathLike
import streamlit as st
import mysql.connector


def main():

    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # st.footer 

    st.title("Login and Sign Up Page: DBMS Assignment")

    menu = ["Login", "Sign Up"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.subheader("Login Section")

        username = st.sidebar.text_input("🧑 User Name")
        password = st.sidebar.text_input("🔑 Password", type='password')
        
        if st.sidebar.button("Login"):
            create_usertable()
            result = login_user(username, password)
            if result:
                st.success("Logged In as {}".format(username))
            else:
                st.warning("Incorrect Username/Password")

    elif choice == "Sign Up":
        st.subheader("Create New Account")

        new_user = st.text_input("👤 User Name")
        new_password = st.text_input("🔑 Password", type='password')

        if st.button("Sign Up"):
            create_usertable()
            add_userdata(new_user, new_password)
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")


def create_usertable():
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        # passwd='root',
        database='DBMS_Assignmnet'
    )
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS UsersTable(username TEXT, password TEXT)")

def add_userdata(username, password):
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        # passwd='root',
        database='DBMS_Assignmnet'
    )
    c = conn.cursor()
    c.execute("INSERT INTO UsersTable VALUES (%s, %s)", (username, password))
    conn.commit()

def login_user(username, password):
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        # passwd='root',
        database='DBMS_Assignmnet'
    )
    c = conn.cursor()
    c.execute("SELECT * FROM UsersTable WHERE username = %s AND password = %s", (username, password))
    data = c.fetchall()
    return data

if __name__ == '__main__':
    main()

