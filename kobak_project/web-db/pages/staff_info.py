import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

from db.sql_commands.select_all_staff_with_id import select_all_staff_from_db
from db.sql_commands.get_reports_for_staff import get_reports
from db.sql_commands.select_all_projects_with_id import select_all_projects_with_id
from db.sql_commands.get_extra_reports_for_staff import get_extra_reports

from work_days_counter import work_days_for_month

from auth import initialize_session_state


def check_months_days(number):
    if number in (1, 3, 5, 7, 8, 10, 12):
        return 31
    elif number in (4, 6, 9, 11):
        return 30
    else:
        return 29


def get_month_name(month_number):
    match month_number:
        case 1:
            return "Январь"
        case 2:
            return "Февраль"
        case 3:
            return "Март"
        case 4:
            return "Апрель"
        case 5:
            return "Май"
        case 6:
            return "Июнь"
        case 7:
            return "Июль"
        case 8:
            return "Август"
        case 9:
            return "Сентябрь"
        case 10:
            return "Октябрь"
        case 11:
            return "Ноябрь"
        case 12:
            return "Декабрь"
        case _:
            return "Неверный номер месяца"

def get_staff():
    return pd.DataFrame(select_all_staff_from_db(), columns=['id', 'name', 'tg', 'role', 'grade'])

def get_projects():
    return pd.DataFrame(select_all_projects_with_id(), columns=['id', 'project_name'])

def get_reports_with_sort(id):
    main_reports = pd.DataFrame(get_reports(id), columns=['date', 'project', 'report', 'time'])
    extra_reports = pd.DataFrame(get_extra_reports(id), columns=['date', 'project', 'report', 'time'])

    return pd.concat([main_reports, extra_reports]).sort_values(by='date', ascending=False)


if __name__ == '__main__':
    initialize_session_state()
    if st.session_state["authentication_status"]:
        staff = get_staff()
        projects = get_projects()

        st.header('Здесь представлены отчеты по одному конкретному сотруднику')

        res = st.selectbox(
            'Выберите сотрудника',
            (staff['name'])
        )

        staff_id = staff.loc[staff['name'] == res]['id']
        staff = staff.loc[staff['name'] == res]

        staff_id = int(staff_id)

        role = staff['role'].iloc[0]
        grade = staff['grade'].iloc[0]

        st.write(f'Роль: {role}')
        st.write(f'Уровень: {grade}')

        res_df = get_reports_with_sort(staff_id)
        # res_df = pd.DataFrame(get_reports(int(staff_id)), columns=['date', 'project', 'report', 'percent'])

        if len(res_df) == 0:
            st.write('Нет отчетов')

        else:

            reports_form = st.selectbox(
                'Выбрать режим отображения',
                ('По неделе', 'По месяцу')
            )

            if reports_form == 'По неделе':
                flag = True
            else:
                flag = False

            res_dict = {}

            if flag:
                curr_week_start = 0
                curr_week_end = 0
                work_days_counter = []

                for index, row in res_df.iterrows():

                    report = row['report']
                    project_id = row['project']
                    percent = row['time']
                    date = row['date']


                    help_table = projects.loc[(projects['id'] == project_id)]['project_name']
                    project_name = help_table.iat[0]

                    if not len(work_days_counter):
                        work_days_counter = [project_name, 0]

                    day = date.to_pydatetime().date()

                    if not curr_week_start:
                        curr_week_start = day - timedelta(days=day.weekday())
                        curr_week_end = curr_week_start + timedelta(days=6)

                    if curr_week_start <= day <= curr_week_end:
                        if project_name == work_days_counter[0]:
                            work_days_counter[1] += 1

                        if project_name in res_dict.keys():
                            res_dict[project_name] += percent
                        else:
                            res_dict[project_name] = percent

                    else:
                        res_dict = {name : (value / work_days_counter[1]) for name, value in res_dict.items()}

                        df_with_projects_time = pd.DataFrame(index=list(res_dict.keys()), data=res_dict.values(), columns=['Время в процентах'])
                        st.write(f'{curr_week_start} --- {curr_week_end}')
                        st.write(df_with_projects_time)

                        curr_week_start = day - timedelta(days=day.weekday())
                        curr_week_end = curr_week_start + timedelta(days=6)
                        res_dict = {project_name: percent}
                        work_days_counter = [project_name, 1]

                else:
                    res_dict = {name: (value / work_days_counter[1]) for name, value in res_dict.items()}

                    df_with_projects_time = pd.DataFrame(index=list(res_dict.keys()), data=res_dict.values(), columns=['Время в процентах'])
                    st.write(f'{curr_week_start} --- {curr_week_end}')
                    st.write(df_with_projects_time)

            else:
                curr_month = 0
                work_days_counter = 0
                prev_day = 0

                for index, row in res_df.iterrows():

                    report = row['report']
                    project_id = row['project']
                    percent = row['time']
                    date = row['date']

                    date = date.to_pydatetime().date()

                    help_table = projects.loc[(projects['id'] == project_id)]['project_name']
                    project_name = help_table.iat[0]

                    if not curr_month:
                        curr_month = date.month
                        work_days_counter = work_days_for_month(int(date.month))

                    if date.month == curr_month:

                        # if date.day != prev_day:
                        #     work_days_counter += 1
                        #     prev_day = date.day

                        if project_name in res_dict.keys():
                            res_dict[project_name] += percent

                        else:
                            res_dict[project_name] = percent

                    else:

                        res_dict = {name: (value / work_days_counter) for name, value in res_dict.items()}
                        df_with_projects_time = pd.DataFrame(index=list(res_dict.keys()), data=res_dict.values(), columns=['Время в процентах'])
                        st.write(f'Месяц: {get_month_name(curr_month)}, количество рабочих дней: {work_days_counter}')
                        st.write(df_with_projects_time)

                        curr_month = date.month
                        res_dict = {project_name: percent}
                        work_days_counter = work_days_for_month(int(date.month))

                else:
                    res_dict = {name: (value / work_days_counter) for name, value in res_dict.items()}
                    df_with_projects_time = pd.DataFrame(index=list(res_dict.keys()), data=res_dict.values(), columns=['Время в процентах'])
                    st.write(f'Месяц: {get_month_name(curr_month)}, количество рабочих дней: {work_days_counter}')
                    st.write(df_with_projects_time)
