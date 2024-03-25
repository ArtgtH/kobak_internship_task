import streamlit as st
import pandas as pd

from db.sql_commands.insert_new_staff_project_relation import insert_new_relation
from db.sql_commands.select_all_from_staff_projects import select_all_staff_projects_with_relations
from db.sql_commands.select_all_projects_with_id import select_all_projects_with_id
from db.sql_commands.select_all_staff_with_id import select_all_staff_from_db
from db.sql_commands.insert_new_staff import insert_new_staff_in_db
from db.sql_commands.delete_staff import delete_staff
from db.sql_commands.delete_staff_project_relation import delete_relation
from db.sql_commands.change_staff_info import change_info

from auth import initialize_session_state


roles = ['Проджект менеджер', 'Бизнес аналитик', 'Архитектор ПО', 'Тимлид ПО', 'Тимлид Web', 'Тимлид DS',
         'Разработчик backend ПО', 'Разработчик frontend ПО', 'Разработчик backend Web', 'Разработчик frontend Web',
         'Data scientist', 'Мобильный разработчик', 'QA инженер', 'Разметчик', 'Дизайнер UX / UI']



def get_projects():
    return pd.DataFrame(select_all_projects_with_id(), columns=['id', 'description'])

def get_staff():
    return pd.DataFrame(select_all_staff_from_db(), columns=['id', 'name', 'tg_name', 'role', 'grade'])

def get_staff_to_projects():
    return pd.DataFrame(select_all_staff_projects_with_relations(), columns=['staff name', 'project name'])


def get_projects_for_staff(staff_name, relations_list):
    return relations_list.loc[relations_list['staff name'] == staff_name]['project name']


if __name__ == '__main__':
    initialize_session_state()
    if st.session_state["authentication_status"]:
        st.header('Страница управления сотрудниками')

        page = st.selectbox('Выберите действие', ['Внести нового сотрудника', 'Удалить сотрудника', 'Изменить данные о сотруднике', 'Привязать/отвязать проект от сотрудника'])

        if page == 'Внести нового сотрудника':

            st.text_input(
                'ФИО сотрудника',
                placeholder='Иванов Иван Иванович',
                key='name'
            )
            st.text_input(
                'ТГ сотрудника',
                placeholder='@IvanIvanovich',
                key='tg'
            )
            st.selectbox(
                'Роль',
                roles,
                key='role'
            )
            match st.session_state.role:
                case 'Проджект менеджер' | 'Бизнес аналитик' | 'Разработчик backend ПО' | \
                    'Разработчик frontend ПО' | 'Разработчик backend Web' | 'Разработчик frontend Web' | 'Data scientist':
                    grades = ('intern', 'junior', 'middle', 'senior')
                case 'Архитектор ПО' | 'Тимлид ПО' | 'Тимлид DS':
                    grades = ('middle', 'senior', 'principal')
                case 'Тимлид Web':
                    grades = ('senior', 'principle')
                case 'Мобильный разработчик' | 'Дизайнер UX / UI':
                    grades = ('junior', 'middle', 'senior')
                case 'QA инженер':
                    grades = ('middle', 'senior')
                case _:
                    grades = ('student', 'lead')

            st.selectbox(
                'Уровень',
                grades,
                key='grade'
            )
            command = st.button('Создать')

            if command:

                res = insert_new_staff_in_db(st.session_state.name, st.session_state.tg, st.session_state.role, st.session_state.grade)
                st.write(res)


        elif page == 'Удалить сотрудника':

            staff = get_staff()
            person = st.selectbox(
                'Выберите сотрудника для удаления',
                staff['name']
            )
            id_table = staff.loc[staff['name'] == person]['id']

            try:
                staff_id = int(id_table)
            except Exception as e:
                st.write('Возможно, в таблице дублируются ФИО')
            else:
                command = st.button('Удалить')

                if command:

                    res = delete_staff(staff_id)
                    st.write(res)

        elif page == 'Изменить данные о сотруднике':

            staff = get_staff()
            person = st.selectbox(
                'Выберите сотрудника, данные которого нужно поменять',
                staff['name']
            )
            id_table = staff.loc[staff['name'] == person]['id']

            try:
                staff_id = int(id_table)
            except Exception as e:
                st.write('Возможно, в таблице дублируются ФИО')
            else:
                staff = staff.loc[staff['id'] == staff_id]

                tg_name = staff['tg_name'].iloc[0]
                role = staff['role'].iloc[0]
                grade = staff['grade'].iloc[0]

                st.text_input(
                    'ФИО сотрудника',
                    value=person,
                    key='name'
                )
                st.text_input(
                    'ТГ сотрудника',
                    value=tg_name,
                    key='tg'
                )

                try:
                    new_roles = roles[::1]
                    new_roles.remove(role)
                    new_roles.append(role)
                    new_roles = new_roles[::-1]
                except Exception as e:
                    new_roles = roles[::1]

                st.selectbox(
                    'Роль',
                    options=new_roles,
                    key='role'
                )
                match st.session_state.role:
                    case 'Проджект менеджер' | 'Бизнес аналитик' | 'Разработчик backend ПО' | \
                         'Разработчик frontend ПО' | 'Разработчик backend Web' | 'Разработчик frontend Web' | 'Data scientist':
                        grades = ('intern', 'junior', 'middle', 'senior')
                    case 'Архитектор ПО' | 'Тимлид ПО' | 'Тимлид DS':
                        grades = ('middle', 'senior', 'principal')
                    case 'Тимлид Web':
                        grades = ('senior', 'principle')
                    case 'Мобильный разработчик' | 'Дизайнер UX / UI':
                        grades = ('junior', 'middle', 'senior')
                    case 'QA инженер':
                        grades = ('middle', 'senior')
                    case _:
                        grades = ('student', 'lead')

                try:
                    grades = list(grades)
                    grades.remove(grade)
                    grades.append(grade)
                    grades = grades[::-1]
                except Exception as e:
                    pass

                st.selectbox(
                    'Уровень',
                    options=grades,
                    key='grade'
                )

                command = st.button('Изменить')

                if command:
                    res = change_info(staff_id, st.session_state.name, st.session_state.tg, st.session_state.role, st.session_state.grade)
                    st.write(res)

        else:

            semi_page = st.selectbox(label='Выберите режим', options=['Добавить проект сотруднику', 'Удалить проект у сотрудника'])

            col1, col2 = st.columns(2)

            staff = get_staff()
            projects = get_projects()
            relations = get_staff_to_projects()

            if semi_page == 'Добавить проект сотруднику':

                with col1:
                    person = st.selectbox(
                        'Выберите сотрудника',
                        staff['name']
                    )

                projects_for_staff = get_projects_for_staff(person, relations).tolist()

                projects_without_that_person = []

                for index, project in projects.iterrows():

                    project_name = project.loc[['description']][0]

                    if not project_name in projects_for_staff:
                        projects_without_that_person.append(project_name)

                with col2:
                    project = st.selectbox(
                        'Выберите проект',
                        projects_without_that_person
                    )

                project_id = projects.loc[projects['description'] == project]['id']
                staff_id = staff.loc[staff['name'] == person]['id']


                try:
                    staff_id = int(staff_id)
                    project_id = int(project_id)
                except Exception as e:
                    st.write('Возможно, сотрудник уже участвует во всех проектах')
                else:
                    command = st.button('Добавить')

                    if command:
                        res = insert_new_relation(staff_id, project_id)
                        st.write(res)

            else:

                with col1:
                    person = st.selectbox(
                        'Выберите сотрудника',
                        staff['name']
                    )

                projects_for_staff = get_projects_for_staff(person, relations)

                with col2:
                    project = st.selectbox(
                        'Выберите проект',
                        projects_for_staff
                    )

                project_id = projects.loc[projects['description'] == project]['id']
                staff_id = staff.loc[staff['name'] == person]['id']

                try:
                    staff_id = int(staff_id)
                    project_id = int(project_id)
                except Exception as e:
                    st.write('Возможно, сотрудник не участвует ни в одном проекте')
                else:

                    command = st.button('Удалить')

                    if command:
                        res = delete_relation(staff_id, project_id)
                        st.write(res)