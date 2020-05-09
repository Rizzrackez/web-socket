from database_query import *


def home_page(method):
    with open('templates/home_page.html') as template:
        return template.read()


def correct_page(method):
    with open('templates/correct_page.html') as template:
        return template.read()


def send_message(method):
    if method == 'GET':
        with open('templates/send_form.html') as template:
            return template.read()

    if method == 'POST':
        return get_all_messages()


def view_messages(method):
    return get_all_messages()


