# import hmac
# import pandas as pd
import logging


# from streamlit.web.server import Server

#
# from db.sql_commands.get_logins_passwords import get_all_logins_passwords
#
#
# def sout():
#     st.write(cookie_manager.get_all())
#
# def check_password():
#
#     def login_form():
#         with st.form('Credentials'):
#             st.text_input('Username', key='username')
#             st.text_input('Password', type='password', key='password')
#             st.form_submit_button('Log in', on_click=password_entered)
#
#
#     def password_entered():
#
#         logins_passwords = {user: password for user, password in get_all_logins_passwords()}
#
#         try:
#             if logins_passwords[st.session_state['username']] == st.session_state['password']:
#                 st.session_state['password_correct'] = True
#                 cookie_manager.set('password', True)
#             else:
#                 st.session_state['password_correct'] = False
#                 cookie_manager.set('password', False)
#
#         except Exception as e:
#             st.session_state['password_correct'] = False
#             cookie_manager.set('password', False)
#
#     if st.session_state.get('password_correct') or cookie_manager.get('password'):
#         st.session_state['password_correct'] = True
#         return True
#
#     login_form()
#
#     if 'password_correct' in st.session_state:
#         st.error('😕 User not known or password incorrect')
#     return False
#
#
# if not check_password():
#     st.stop()
#
# st.subheader('Вы можете смело пользоваться функционалом')
# sout()
# if cookie_manager.get('password'):
#     if st.button('Log out'):
#         cookie_manager.delete('password')

import streamlit_authenticator as stauth
import yaml
from streamlit.source_util import get_pages
from yaml.loader import SafeLoader
import streamlit as st
import extra_streamlit_components as stx


def initialize_session_state():
    if 'name' not in st.session_state:
        st.session_state['name'] = None
    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = None
    if 'username' not in st.session_state:
        st.session_state['username'] = None


if __name__ == '__main__':
    initialize_session_state()
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
    )

    authenticator.login()

    if st.session_state["authentication_status"]:
        st.title(f'Привет, *{st.session_state["name"]}*')

        pages = get_pages('auth.py')
        st.title('Доступные страницы')
        st.page_link('pages/general_info.py', label='Общая информация')
        st.page_link('pages/projects_info.py', label='Информация о проектах')
        st.page_link('pages/staff_info.py', label='Информация о сотрудниках')

        st.page_link('pages/projects_management.py', label='Управление проектами',)
        st.page_link('pages/staff_management.py', label='Управление сотрудниками',)
        authenticator.logout()
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
