import requests
from db.functional_db import checking_for_uniqueness


URL = "https://api.vk.com/method/"
HOME_PAGE = "https://vk.com/id"


# Обрабатываем сообщение запроса
def request_handler(msg):
    msg = msg[5:].split(',')
    sex = int(msg[0])
    status = int(msg[1])
    from_ = int(msg[2])
    to = int(msg[3])
    city = msg[4]
    return sex, status, from_, to, city


# Ищем id кандидата соответствующего параметрам запроса
def search_candidates(id, token: str, sex: int, status: int, age_from: int, age_to: int, hometown: str) -> list:
    url = URL + "users.search"
    params = {
            "access_token": f"{token}",
            "count": "20",
            "sex": f"{sex}",
            "hometown": f"{hometown}",
            "status": f"{status}",
            "age_from": f"{age_from}",
            "age_to": f"{age_to}",
            "has_photo": "1",
            "v": "5.131"
            }
    try:
        res = requests.get(url, params=params).json()
        res = res["response"]["items"]
    except KeyError:
        return False 
    except requests.exceptions.ConnectionError:
        print( f"Соединение было прервано.")
    else:
        if res != []:
            id_list = []
            check_list = checking_for_uniqueness(id)
            for item in res:
                if item["id"] in check_list:
                    return None
                else:
                    id_list.append(item["id"])
            return id_list
        else:
            return None


# Получаем список состоящий из адреса домашней стр. и адресов топовых фото
def get_photo_and_home_url(id, token) -> list:
    url = URL + "photos.get"
    home = HOME_PAGE + str(id)
    params = {
            'owner_id': f'{id}',
            'album_id': 'profile',
            'extended': '1',
            'access_token': f'{token}',
            'v':'5.131'
            }
    try:
        res = requests.get(url, params=params).json()
        res = res["response"]
    except KeyError:
        pass
    except requests.exceptions.ConnectionError:
        print( f"Соединение было прервано.")
    else:
        res = res["items"]
        photo_list = []
        for item in res:
            url_photo = item['sizes'][-1]['url']
            count_likes = item['likes']['count']
            photo_list.append((count_likes, url_photo))
        photo_list = sorted(photo_list, reverse=True)[:3]
        url_list = []
        for url_ in photo_list:
            url_list.append(url_[1:][0])
        url_list.append(home)
        return url_list
        
