"""
Login and Sign Up Page using Streamlit and MYSQL
"""

import streamlit as st
import mysql
import mysql.connector
import uuid as uid
import footer

conn = mysql.connector.connect(
        host='localhost',
        user='rao',
        passwd='password',
        database='DBMS_Assignment'
    )

if 'id' not in st.session_state:
    st.session_state["id"] = None


def main():

    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # st.footer 

    st.title("Welcome to DBMS Assignments")

    menu = ["Login", "Sign Up"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.subheader("Login Section")

        username = st.sidebar.text_input("🧑 User Name")
        password = st.sidebar.text_input("🔑 Password", type='password')
        
        if st.sidebar.button("Login") or st.session_state["id"]!=None:
            # st.write(st.session_state["id"])

            create_usertable()

            User = login_user(username, password)

            if not User:
                st.warning("Incorrect Username/Password")
                st.session_state["id"] = None
                return

            id, user = User[0][0], User[0][1]

            st.session_state["id"] = id

            # st.balloons()
            # st.error(User)

            formbtn = st.button("View Form")

            if "formbtn_state" not in st.session_state:
                st.session_state.formbtn_state = False

            if formbtn or st.session_state.formbtn_state:
                st.session_state.formbtn_state = True
                if id:
                    st.success("Logged In as {} with ID {}".format(user, id))

                    st.subheader("User Info Form")

                        # name = st.text_input("Name")
                    with st.form(key = 'user_info'):
                        st.write('User Information')

                        name = st.text_input(label="Name 📛")
                        age = st.number_input(label="Age 🔢")
                        email = st.text_input(label="Email 📧")
                        phone = st.text_input(label="Phone 📱")
                        gender = st.radio("Gender 🧑", ("Male", "Female", "Prefer Not To Say"))
                        submit_form = st.form_submit_button(label="Register", help="Click to register!")

                        st.write(submit_form)

                        # Checking if all the fields are non empty
                        if submit_form:
                            st.write(submit_form)

                            if name and age and email and phone and gender:
                                # add_user_info(id, name, age, email, phone, gender)
                                st.success(
                                f"ID:  \n Name: {name}  \n Age: {int(age)}  \n Email: {email}  \n Phone: {phone}  \n Gender: {gender}")

                                # Adding the user_info in to the database
                                add_user_info(id, name, age, email, phone, gender)
                            else:
                                st.warning("Please fill all the fields")
                            # else:
                                # st.warning("Please fill all the fields")
                else:
                    st.warning("Incorrect Username/Password")

    elif choice == "Sign Up":
        st.subheader("Create New Account")

        new_user = st.text_input("👤 User Name")
        new_password = st.text_input("🔑 Password", type='password')

        if st.button("Sign Up"):
            if not new_user:
                st.warning("Please enter a username")
            elif not new_password:
                st.warning("Please enter a password")
            else:
                create_usertable()
                add_userdata(new_user, new_password)
        

def create_usertable():
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS UsersTable(id TEXT, username TEXT, password TEXT)")

def add_userdata(username, password):
    c = conn.cursor()
    # Checking if the username already exists or not
    c.execute("SELECT * FROM UsersTable WHERE username = %s", (username,))
    data = c.fetchall()

    if data:
        st.warning("Username already exists")
    else:
        c.execute("INSERT INTO UsersTable(id, username, password) VALUES(%s, %s, %s)", (uid.uuid4().hex, username, password))
        conn.commit()

        st.success("You have successfully created a valid Account")
        st.info("Go to Login Menu to login")

    conn.commit()

def login_user(username, password):
    if not username:
        st.warning("Please enter a username")
    elif not password:
        st.warning("Please enter a password")
    else: 
        c = conn.cursor()
        # Check if username exists or not
        c.execute('SELECT username FROM UsersTable WHERE username = %(username)s', { 'username' : username })

        # query = "SELECT username FROM UsersTable WHERE username = 'admin'"
        # c.execute(query)
        checkUsername = c.fetchall()
        username_exists = checkUsername is not None

        # if username is valid then check if the passwords matches or not
        if username_exists:
            # st.success(checkUsername)

            c.execute('SELECT password FROM UsersTable WHERE password = %(password)s', { 'password' : password })
            checkPassword = c.fetchall()
            password_exists = checkPassword is not None
            
            if password_exists:
                # if true then return username and ID
                c.execute('SELECT id, username FROM UsersTable WHERE username = %(username)s', { 'username' : username })
                # st.warning(c.fetchall())

                data = c.fetchall()
            
                return data

            else:
                st.info(checkPassword)
                st.error('!Password')
                return False
        else:
            # st.info(user_name)
            st.info(checkUsername)
            st.error('!Username')
            return False
        
        # c.execute("SELECT * FROM UsersTable WHERE username = %s AND password = %s", (username, password))
        # data = c.fetchall()
        # return data

def add_user_info(id, name, age, email, phone, gender):
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS UserInfo(id TEXT, name TEXT, age TEXT, email TEXT, phone TEXT, gender TEXT)")

    # Checking if the id is registered or not
    c.execute("SELECT * FROM UserInfo WHERE id = %s", (id,))
    data = c.fetchone()
    id_exists = data is not None

    st.write(data)
    st.write(id_exists)

    if id_exists:
        st.warning("ID already exists\n You've been registered already.")
    else:
        c.execute("INSERT INTO UserInfo(id, name, age, email, phone, gender) VALUES(%s, %s, %s, %s, %s, %s)", (id, name, age, email, phone, gender))

        conn.commit()
        st.success("You have successfully registered!")

    conn.commit()

if __name__ == '__main__':
    main()
    footer.footer()
