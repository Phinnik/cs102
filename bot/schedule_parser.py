import requests
from bs4 import BeautifulSoup
from typing import List

DOMAIN = 'http://www.ifmo.ru/ru/schedule/0'


def get_page(group: str, week: str = '') -> BeautifulSoup:
    """ Returns BS page from groupnumber and week """
    if week:
        week += '/'

    url = '{domain}/{group}/{week}/raspisanie_zanyatiy_{group}.htm'.format(
        domain=DOMAIN,
        group=group,
        week=week
        )
    response = requests.get(url)
    web_page = response.text
    soup_page = BeautifulSoup(web_page, "html5lib")
    return soup_page


def get_dayly_schedule(day: int, page: BeautifulSoup) -> List[dict]:
    """ Parse BS page and return daily schedule by day number """
    """ If there is no such group returns None """
    try:
        lessons_table = page.find('table', {'id': '{}day'.format(day)})
        lessons_list = lessons_table.findAll('tr')

        for i in range(len(lessons_list) - 1):
            lessons_list[i] = {
                'time': lessons_list[i].find('td', {'class': 'time'}).find('span').text,
                'lesson_name': lessons_list[i].find('td', {'class': 'lesson'}).find('dd').text,
                'building': lessons_list[i].find('dt', {'class': 'rasp_corp_mobile'}).find('span').text,
                'room': lessons_list[i].find('td', {'class': 'room'}).find('dd').text,
                'week': lessons_list[i].find('td', {'class': 'time'}).find('dt').text
            }
            if lessons_list[i]['week'] == 'нечетная неделя':
                lessons_list[i]['week'] = 1

            elif lessons_list[i]['week'] == 'четная неделя':
                lessons_list[i]['week'] = 2
            else:
                lessons_list[i]['week'] = 0
        lessons_list.pop(-1)
        return lessons_list
    except Exception:
        return None


def get_all_schedule(group: str) -> List[List[dict]]:
    """ Returns all schedule of group or None if there is no such group"""
    page = get_page(group, week=0)
    days = [get_dayly_schedule(i, page) for i in range(1, 7)]
    if days == [None]*6:
        return None
    else:
        return days
