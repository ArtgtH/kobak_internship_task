import streamlit as st
import pandas as pd

from db.sql_commands.select_all_projects_with_id import select_all_projects_with_id
from db.sql_commands.insert_new_project import insert_new_project_in_db
from db.sql_commands.delete_project import delete_project
from db.sql_commands.select_all_staff_with_id import select_all_staff_from_db
from db.sql_commands.select_all_from_staff_projects import select_all_staff_projects_with_relations
from db.sql_commands.delete_staff_project_relation import delete_relation
from db.sql_commands.insert_new_staff_project_relation import insert_new_relation

from auth import initialize_session_state


def get_projects():
    return pd.DataFrame(select_all_projects_with_id(), columns=['id', 'description'])

def get_staff():
    return pd.DataFrame(select_all_staff_from_db(), columns=['id', 'name', 'tg_name', 'role', 'grade'])

def get_staff_to_projects():
    return pd.DataFrame(select_all_staff_projects_with_relations(), columns=['staff name', 'project name'])

def get_staff_for_current_project(project_name, relations_list):
    return relations_list.loc[relations_list['project name'] == project_name]['staff name']


if __name__ == '__main__':
    initialize_session_state()
    if st.session_state["authentication_status"]:
        st.header('Страница управления проектами')

        page = st.selectbox('Выберите действие', ['Внести новый проект', 'Удалить проект', 'Привязать/отвязать сотрудника от проекта'])

        if page == 'Внести новый проект':

            st.text_input(
                'Введите название проекта',
                placeholder='СуперСекретныйПроект№1',
                key='description'
            )
            command = st.button('Создать')

            if command:

                res = insert_new_project_in_db((st.session_state.description))
                st.write(res)

        elif page == 'Удалить проект':

            projects = get_projects()
            project = st.selectbox(
                'Выберите проект для удаления',
                projects['description']
            )
            id_table = projects.loc[projects['description'] == project]['id']

            try:
                project_id = int(id_table)
            except Exception as e:
                st.write('Возможно, в таблице дублируются названия проектов')
            else:
                command = st.button('Удалить')

                if command:

                    res = delete_project(project_id)
                    st.write(res)


        else:
            semi_page = st.selectbox(label = 'Выберите режим', options=['Добавить сотрудника в проект', 'Удалить сотрудника из проекта'])

            col1, col2 = st.columns(2)

            staff = get_staff()
            projects = get_projects()
            relations = get_staff_to_projects()

            if semi_page == 'Добавить сотрудника в проект':

                with col1:
                    project = st.selectbox(
                        'Выберите проект',
                        projects['description']
                    )

                project_staff = get_staff_for_current_project(project, relations).tolist()

                staff_not_in_project = []

                for index, person in staff.iterrows():

                    name = person.loc[['name']][0]

                    if not name in project_staff:
                        staff_not_in_project.append(name)


                with col2:
                    person = st.selectbox(
                        'Выберите сотрудника',
                        staff_not_in_project
                    )

                project_id = projects.loc[projects['description'] == project]['id']
                staff_id = staff.loc[staff['name'] == person]['id']

                try:
                    staff_id = int(staff_id)
                    project_id = int(project_id)
                except Exception as e:
                    st.write('Возможно, все работники уже участвуют в проекте')
                else:
                    command = st.button('Добавить')

                    if command:
                        res = insert_new_relation(staff_id, project_id)
                        st.write(res)

            else:

                with col1:
                    project = st.selectbox(
                        'Выберите проект',
                        projects['description']
                    )

                project_staff = get_staff_for_current_project(project, relations)

                with col2:
                    person = st.selectbox(
                        'Выберите сотрудника',
                        project_staff
                    )

                project_id = projects.loc[projects['description'] == project]['id']
                staff_id = staff.loc[staff['name'] == person]['id']

                try:
                    staff_id = int(staff_id)
                    project_id = int(project_id)
                except Exception as e:
                    st.write('Возможно, в проекте уже не осталось сотрудников')
                else:

                    command = st.button('Удалить')

                    if command:
                        res = delete_relation(staff_id, project_id)
                        st.write(res)
