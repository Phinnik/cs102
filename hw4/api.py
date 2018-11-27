import requests
import time
import config
from api_models import User, Message
from typing import List


def get(url:str, params:dict={}, timeout:int=5, max_retries:int=5, backoff_factor:int=0.3) -> dict:
    """ Выполнить GET-запрос c экспоненциальным нарастанием задержки при ошибке """
    request_status = False
    retries = 1
    while (request_status == False) and (retries < max_retries):
        try:
            r = requests.get(url, params)
            request_status = True
        except requests.RequestException as e:
            time.sleep(timeout * backoff_factor * retries)
            retries += 1
    return r.json()['response']


def is_api_ok() -> dict:
    # функция для отладки. Проверка, доступно ли api
    url = "https://api.vk.com/method/friends.get"
    parameters = {'access_token': config.VK['VK_ACCESS_TOKEN'],
                  'user_id': config.VK['MY_ID'],
                  'fields': '',
                  'count': 1,
                  'v': config.VK['API_VERSION']}
    r = requests.get(url, params=parameters).json()
    print(r)
    return r


def execute(code: str) -> dict:
    # run excecute method wich alows to make 25 API requests in one time
    url = 'https://api.vk.com/method/execute'
    parameters = {'code':code,
                  'access_token': config.VK['VK_ACCESS_TOKEN'],
                  'v': config.VK['API_VERSION']}
    result = get(url, params=parameters)
    return result


def get_friends(user_id: int, fields: str='bdate', count:int=5, offset:int=0) -> List[User]:
    """ Вернуть данныe о друзьях пользователя """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    url = "https://api.vk.com/method/friends.get"
    parameters = {'access_token': config.VK['VK_ACCESS_TOKEN'],
                  'user_id': user_id,
                  'offset': offset,
                  'fields': fields,
                  'count': count,
                  'v': config.VK['API_VERSION']}

    friends = get(url, params=parameters)['items']
    for i in range(len(friends)):
        friends[i] = User(**friends[i])
    return friends


def get_friends_with_execute(user_ids: List[int]) -> List[List[User]]:
    print('executing friends')
    friends_list = []
    for i in range(len(user_ids) // 25 + 1):
        code = """
                  var users = {};
                  var friends = [];
                  var i = 0;
                  while (i < users.length) {{
                    var user_friends = API.friends.get( {{"user_id":users[i], "fields":"online"}})["items"];
                    friends.push(user_friends);
                    i = i+1;
                  }}
                  return friends;
               """.format(user_ids[i*25:(i+1)*25])
        user_friends_list = execute(code)
        friends_list.extend(user_friends_list)

    # deleting deactivated users and makink users model list
    deactivated = []
    for i in range(len(friends_list)):
        if friends_list[i] is None:
            deactivated.append(i)
            continue
        for j in range(len(friends_list[i])):
            friends_list[i][j] = User(**friends_list[i][j])
    for ind in deactivated:
        friends_list.pop(ind)
    return friends_list


def messages_get_history(user_id: int, offset: int=0, count: int=200, rev:int=0) -> List[Message]:
    """ Получить историю переписки с указанным пользователем """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    
    url = "https://api.vk.com/method/messages.getHistory"
    parameters = {
        'access_token': config.VK['VK_ACCESS_TOKEN'],
        'user_id': user_id,
        'offset': offset,
        'count': count,
        'rev' : rev,
        'v': config.VK['API_VERSION']
    }
    messages_history = get(url, params=parameters)
    return messages_history


def get_messages_with_execute(user_id:int, count:int=10000, offset:int=0) -> List[Message]:
    messages = []
    code = '''var messages = [];
              var methods_count = 0;
              while (methods_count < 25) {{
                  var mes = API.messages.getHistory({{"user_id":{},
                                                      "count": {},
                                                      "offset": methods_count * 200 + {} }});
                  messages.push(mes["items"]);
                  methods_count = methods_count + 1;
              }}
              return messages;
           '''

    for i in range(count//(25*200)+1):
        messages_executed = execute(code.format(user_id, 200, i*5000 + offset))
        
        for j in range(len(messages_executed)):
            messages_executed.extend(messages_executed[0])
            messages_executed.pop(0)

        messages.extend(messages_executed)

    for i in range(len(messages) - count):
        messages.pop(-1)
    return messages

def main():
    pass

main()