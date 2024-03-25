import streamlit as st
import pandas as pd

from db.sql_commands.select_all_staff import select_all_staff_from_db
from db.sql_commands.select_all_projects import select_all_projects_from_db
from db.sql_commands.select_all_from_staff_projects import select_all_staff_projects_with_relations

from auth import initialize_session_state


def get_staff_as_tuple():
    return select_all_staff_from_db()

def get_staff():
    return pd.DataFrame(get_staff_as_tuple(), columns=['ИмяФамилия', 'ТГ', 'Роль', 'Уровень'])

def get_projects_with_staff():
    staff = get_staff_as_tuple()
    projects = select_all_projects_from_db()
    relations = select_all_staff_projects_with_relations()

    projects_dict = { project[0]: [[]] for project in projects}

    for name, project in relations:
        projects_dict[project][0].append(name)

    return pd.DataFrame(projects_dict.values(), index=projects_dict.keys(), columns=['Сотрудники'])

def get_staff_to_projects():
    return pd.DataFrame(select_all_staff_projects_with_relations(), columns=['staff name', 'project name'])


if __name__ == '__main__':
    initialize_session_state()
    if st.session_state.authentication_status:

        st.header('Общая информация')

        page = st.radio('Выберите режим', ['Общая таблица сотрудников', 'Общая таблица проектов'])


        if page == 'Общая таблица сотрудников':

            st.subheader('Список сотрудников')
            df = get_staff()
            st.write(df)

        elif page == 'Общая таблица проектов':

            staff = [person[0] for person in get_staff_as_tuple()]
            df = get_projects_with_staff()

            person = st.selectbox(
                'Фильтр по человеку',
                ['Выберите человека', *staff],
            )
            flag = st.button('Сбросить')

            if flag or person == 'Выберите человека':
                st.subheader('Общая таблица проектов')
                st.dataframe(df)

            else:
                st.subheader(f'Таблица проектов с {person}')


                src_for_res_df = []

                for index, row in df.iterrows():

                    if person in row['Сотрудники']:
                        src_for_res_df.append(row)

                if len(src_for_res_df) == 0:
                    st.write('У этого человека нет проектов')
                else:
                    res_df = pd.DataFrame(src_for_res_df)
                    st.dataframe(res_df)
