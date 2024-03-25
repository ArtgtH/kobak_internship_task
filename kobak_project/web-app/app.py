"""
Здесь лежит Flask-приложение

Endpoints:
1. get_page - получаем страницу с формой по get-запросу к приложению
2. submit - отправляем данные формы по post-запросу
3. about - запасной endpoint, потенциально в него можно пихать какую-то полезную инфу
"""
import time
from datetime import datetime, date, timedelta

from flask import Flask, render_template, request, session

from db.connection import create_connection
from db.get_projects import get_user_projects
from db.insert_week_reports import insert_user_reports
from db.search_user_id import get_user_id
from db.get_project_descriptions import get_projects
from db.get_all_projects import get_all_projects
from db.check_date import get_last_date

import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


app = Flask(__name__)
app.config["SECRET_KEY"] = "afghds443df134gadg55"
app.config["SESSION_TYPE"] = "filesystem"


def check_user_last_report(user):
    """
    Функция, которая проверяет, когда был загружен последний отчет
    params: user - ID пользователя
    return: True, если пользователь не загружал отчет на этой неделе, False, если пользователь загружал отчет
    """
    connection = create_connection()

    curr_date = date.today()

    last_report_date = get_last_date(connection, user)

    if last_report_date is None:
        return True

    last_report_date = last_report_date.date()
    start = last_report_date - timedelta(days=last_report_date.weekday())
    end = start + timedelta(days=6)

    if start <= curr_date <= end:
        return False
    return True


@app.route("/", methods=["GET"])
def get_page():
    """
    Endpoint для отображения формы;
    Берется ссылка ТГ юзера, к ней сопоставляется id юзера, далее берутся все проекты пользователя и проекты, в которых нет пользователя;
    Для этих данных составляется форма с возможностью довнесения проектов
    :return: template(form.html) 
    """
    username = "@" + str(request.args.get("username"))

    connection = create_connection()

    if not session.get("user_id"):
        user_id = get_user_id(connection, username)
        if user_id is None:
            return render_template("unknown_user.html")

        session["user_id"] = user_id
    else:
        user_id = session.get("user_id")

        logger.debug('user_id' + user_id)


    if check_user_last_report(user_id):
        user_projects = get_user_projects(connection, user_id)
        all_projects = get_all_projects(connection)

        projects_without_person = [project for project in all_projects if project not in user_projects]

        session["projects_ids"] = user_projects
        session["user_id"] = user_id

        logger.debug(session.get("projects_ids"))
        logger.debug(session.get("user_id"))

        project_descriptions = []
        for id in user_projects:
            project_descriptions.extend(get_projects(connection, id))

        project_without_person_descriptions = []
        for id in projects_without_person:
            project_without_person_descriptions.extend(get_projects(connection, id))


        projects = zip(project_descriptions, user_projects)
        projects_without_person = zip(projects_without_person, project_without_person_descriptions)

        session["projects"] = list(projects)
        session["projects_without_person"] = list(projects_without_person)


        today_date = datetime.today().date()
        curr_week_start = today_date - timedelta(days=today_date.weekday())
        curr_week_end = curr_week_start + timedelta(days=6)

        session.modified = True

        return render_template("form.html",
            projects=session.get("projects"),
            projects_without_person=session.get("projects_without_person"),
            date=f'{curr_week_start} - {curr_week_end}'
        )

    else:
        return render_template("already_created_report.html")


@app.route("/", methods=["POST"])
def submit():
    """
    Endpoint для обработки post-запросов формы
    Проверяет, чтобы сумма процентов проектов была равна 100 и добавляет внесенную инфу в бд, в 
    противном случае - возвращает на страницу с формой
    :return: template("result.html") - если все хорошо, template(form.html) - если есть ошибка
    """

    logger.debug(session)
    reports = []
    extra_reports = []

    ids = session.get("projects_ids")
    user_id = session.get("user_id")

    logger.debug(session.get("projects_ids"))
    logger.debug(session.get("user_id"))


    connection = create_connection()

    summ = 0
    all_projects_ids = list(request.form.keys())

    for id in all_projects_ids:

        time = request.form.get(str(id))
        if time:
            time = float(time)
        else:
            time = 0

        summ += time

        if int(id) in ids:
            reports.append((id, time))
        else:
            extra_reports.append((id, time))

    if summ != 100:
        error = "Суммарный процент времени по проектам не равен 100%"
        today_date = datetime.today().date()
        curr_week_start = today_date - timedelta(days=today_date.weekday())
        curr_week_end = curr_week_start + timedelta(days=6)
        return render_template(
                               "form.html",
                               projects=session.get("projects"),
                               projects_without_person=session.get("projects_without_person"),
                               error=error,
                                date=f'{curr_week_start} - {curr_week_end}'
                               )

    insert_user_reports(connection, reports=reports, extra_reports=extra_reports, user=user_id)

    return render_template("result.html")


@app.route("/about/", methods=["GET"])
def about():
    """
    Запасной Endpoint для вывода информации
    :return: template("info.html")
    """
    return render_template("info.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
