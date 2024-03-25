import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

from db.sql_commands.get_extra_reports_for_staff import get_extra_reports
from db.sql_commands.select_all_from_staff_projects import select_all_staff_projects_with_relations
from db.sql_commands.select_all_staff_with_id import select_all_staff_from_db
from db.sql_commands.get_reports_for_staff import get_reports
from db.sql_commands.select_all_projects_with_id import select_all_projects_with_id
from db.sql_commands.select_extra_staff_for_project import select_extra_staff_for_projects

from work_days_counter import work_days_for_month

from auth import initialize_session_state


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

def get_staff_for_project(project_name):
    all_relations = pd.DataFrame(select_all_staff_projects_with_relations(), columns=['staff name', 'project name'])
    return all_relations.loc[all_relations['project name'] == project_name]['staff name']

def get_staff():
    return pd.DataFrame(select_all_staff_from_db(), columns=['id', 'name', 'tg', 'role', 'grade'])

def get_projects():
    return pd.DataFrame(select_all_projects_with_id(), columns=['id', 'project_name'])

def get_extra_staff_for_project(project_name):
    return pd.DataFrame(select_extra_staff_for_projects(project_name), columns=['name'])


def get_reports_with_sort(id):
    main_reports = pd.DataFrame(get_reports(id), columns=['date', 'project', 'report', 'time'])
    extra_reports = pd.DataFrame(get_extra_reports(id), columns=['date', 'project', 'report', 'time'])

    return pd.concat([main_reports, extra_reports]).sort_values(by='date', ascending=False)


if __name__ == '__main__':
    initialize_session_state()
    if st.session_state["authentication_status"]:
        staff = get_staff()
        projects = get_projects()

        st.header('Здесь представлена совокупность отчетов по одному конкретному проекту')

        res = st.selectbox(
            'Выберите проект',
            (projects['project_name'])
        )

        time_format = st.selectbox(
            'Выберите режим отображения времени',
            ('По дням', 'По неделям', 'По месяцам')
        )

        project_id = projects.loc[projects['project_name'] == res]['id'].tolist()[0]

        staff_names = get_staff_for_project(res).to_list()

        extra_staff_names = select_extra_staff_for_projects(res)

        extra_staff_names = [i[0] for i in extra_staff_names]

        res_df_with_all_reports = pd.DataFrame()

        if len(extra_staff_names) != 0:
            staff_names.extend(extra_staff_names)

        for name in staff_names:

            staff_id = int(staff.loc[(staff['name'] == name)]['id'])

            reports_for_staff = get_reports_with_sort(staff_id)

            reports_for_staff = reports_for_staff.loc[(reports_for_staff['project'] == project_id)]

            if time_format == 'По дням':

                days_not_formatted = reports_for_staff['date'].to_list()
                time = reports_for_staff['time'].to_list()

                days_formatted = [day.to_pydatetime().date() for day in days_not_formatted]

                help_df = pd.DataFrame(index=days_formatted, columns=[name], data=time).T

                res_df_with_all_reports = pd.concat([res_df_with_all_reports, help_df])

            elif time_format == 'По неделям':

                curr_week_start = 0
                curr_week_end = 0
                total = 0
                df_for_one_person = pd.DataFrame(index=[name])

                if len(reports_for_staff) == 0:
                    res_df_with_all_reports = pd.concat([res_df_with_all_reports, df_for_one_person])

                else:
                    for index, report in reports_for_staff.iterrows():
                        percent = report['time']
                        date = report['date']

                        date = date.to_pydatetime().date()

                        if not curr_week_start:
                            curr_week_start = date - timedelta(days=date.weekday())
                            curr_week_end = curr_week_start + timedelta(days=6)

                        if curr_week_start <= date <= curr_week_end:
                            total += percent

                        else:

                            df_for_one_person[f'{curr_week_start} --- {curr_week_end}'] = total / 5
                            total = percent

                            curr_week_start = date - timedelta(days=date.weekday())
                            curr_week_end = curr_week_start + timedelta(days=6)

                    else:
                        if total:
                            df_for_one_person[f'{curr_week_start} --- {curr_week_end}'] = total / 5
                        else:
                            df_for_one_person[f'{curr_week_start} --- {curr_week_end}'] = None
                        res_df_with_all_reports = pd.concat([res_df_with_all_reports, df_for_one_person])

            else:

                curr_month = 0
                work_days_counter = 0
                total = 0
                df_for_one_person = pd.DataFrame(index=[name])

                if len(reports_for_staff) == 0:
                    res_df_with_all_reports = pd.concat([res_df_with_all_reports, df_for_one_person])

                else:
                    for index, report in reports_for_staff.iterrows():

                        percent = report['time']
                        date = report['date']

                        date = date.to_pydatetime().date()

                        if not curr_month:
                            curr_month = date.month
                            work_days_counter = work_days_for_month(int(date.month))

                        if date.month == curr_month:
                            total += percent

                        else:
                            if work_days_counter:
                                df_for_one_person[get_month_name(curr_month)] = total / work_days_counter

                            work_days_counter = work_days_for_month(int(date.month))
                            total = percent
                            curr_month = date.month

                    else:
                        if work_days_counter:
                            df_for_one_person[get_month_name(curr_month)] = total / work_days_counter

                        res_df_with_all_reports = pd.concat([res_df_with_all_reports, df_for_one_person])

        else:

            if len(res_df_with_all_reports) == 0:
                st.write('В проекте еще нет отчетов')
            else:
                res_df_with_all_reports = res_df_with_all_reports[~res_df_with_all_reports.index.duplicated(keep='first')]
                st.write(res_df_with_all_reports)
