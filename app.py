from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from token_group import token_group
from commands_app import request_handler, search_candidates, get_photo_and_home_url
from db.functional_db import append_queries, check_for_registration, reg_new_user,\
     delete_user, get_action_user, update_action_user, upload_data_user, get_token
from db.create_db import create_table

vk = vk_api.VkApi(token=token_group)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,
                                                    'random_id': randrange(10 ** 7),})

def message_handler():
    user_act = " "
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                id = event.user_id
                msg = event.text.lower()
                session_api = vk.get_api()
                user_get = session_api.users.get(user_ids=event.user_id)
                name = user_get[0]['first_name']
                if check_for_registration(id) is False:
                    write_msg(id, f"Здравствуйте, {name}.\n"
                                  f"Меня зовут - Vkinder\n"
                                  f"Я чат - бот для знакомств.\n"
                                  f"Добро пожаловать!\n"
                                  f"Как вижу Вы ещё не зарегистрированы.\n"
                                  f"Вы готовы пройти регистрацию? - (да или нет)")
                    reg_new_user(id, "new_user", name, "")
                else:
                    user_act = get_action_user(id)
                    if user_act == "new_user" and msg == "да" or \
                       user_act == "yes" and "токен" not in msg:
                        update_action_user(id, "yes")
                        write_msg(id, f"Для завершения регистрации необходим token.\n"
                                      f"Введите:\n"
                                      f"токен (здесь токен без скобок)\n"
                                      f"Пример:\n"
                                      f"токен qwc5678ebdvpfb8cbd\n"
                                      f"Для получения токена следуйте по инструкции ниже.\n"
                                      f"Создаем приложение\n"
                                      f"1) Нажимаете на кнопку создать приложение\n"
                                      f"2) Выбираете standalone приложение, указываете "
                                      f"название приложения\n"  
                                      f"https://sun9-60.userapi.com/c857736/v857736671/14acdc/66pnWpKHRmM.jpg\n"
                                      f"3) Переходите в настройки, включаете Open API\n"
                                      f"4) В поле *адрес сайта* вводите http://localhost\n"
                                      f"5) В поле базовый домен вводите localhost\n"
                                      f"https://sun9-4.userapi.com/c857736/v857736671/14acee/6qdLYkpdBl4.jpg\n"
                                      f"6) Сохраняете изменения\n"
                                      f"7) Копируете id приложения\n" 
                                      f"8) В ссылку\n" 
                                      f"https://oauth.vk.com/authorize?client_id=1&display=page&scope=stats,offline&response_type=token&v=5.131"
                                      f" вместо 1 вставьте id **вашего** приложения." 
                                      f"Не забудьте указать scope: https://vk.com/dev/permissions\n"
                                      f"9) Нажимаете разрешить\n"
                                      f"10) Сохраняете токен\n"
                                      f"https://sun9-29.userapi.com/c857736/v857736671/14acf8/2c-F9g7w0jA.jpg")
                    elif user_act == "new_user" and msg == "нет":
                        delete_user(id)
                        write_msg(id, f"{name}, жаль, что мы с Вами так быстро прощаемся\n"
                                      f"Я надеялся, что Вы задержитесь подольше.\n"
                                      f"С нетерпением жду Вашего скорейшего возвращения.\n"
                                      f"Bye, bye!")
                    elif user_act == "yes" and "токен" in msg:
                        msg_list_ = msg.split(" ")
                        reg_token = msg_list_[1]
                        upload_data_user(id, column="token", msg=reg_token)
                        update_action_user(id, "end")
                        write_msg(id, f"Поздравляю! Вы успешно завершили регистрацию!\n"
                                      f"Теперь Вам доступен поиск.\n"
                                      f"пол. Возможные значения:\n" 
                                      F"1 — женщина;\n"
                                      f"2 — мужчина;\n"
                                      f"семейное положение. Возможные значения:\n"
                                      f"1 — не женат (не замужем);\n"
                                      f"2 — встречается;\n"
                                      f"3 — помолвлен(-а);\n"
                                      f"4 — женат (замужем);\n"
                                      f"5 — всё сложно;\n"
                                      f"6 — в активном поиске;\n"
                                      f"7 — влюблен(-а);\n"
                                      f"8 — в гражданском браке.\n"
                                      f"Форма запроса: пол, семейное положение,\n"
                                      f"возраст от, возраст до, город\n"
                                      f"Пример:\nпоиск 1,6,25,30,Москва")
                    elif user_act == "end" and "поиск" in msg:
                        token = get_token(id)
                        item = request_handler(msg)
                        candidates = search_candidates(id, token, item[0], item[1], item[2],
                                                                                item[3], item[4])
                        if candidates is False :
                            update_action_user(id, "token")
                            write_msg(id, f"При регистрации был указан неверный токен!\n"
                                          f"Будем обновлять токен?\n"
                                          f"Введите - (обновляем или не обновляем)\n")
                        elif candidates is None:
                            write_msg(id, f"Попробуйте другой запрос.\n"
                                          f"пол. Возможные значения:\n" 
                                          F"1 — женщина;\n"
                                          f"2 — мужчина;\n"
                                          f"семейное положение. Возможные значения:\n"
                                          f"1 — не женат (не замужем);\n"
                                          f"2 — встречается;\n"
                                          f"3 — помолвлен(-а);\n"
                                          f"4 — женат (замужем);\n"
                                          f"5 — всё сложно;\n"
                                          f"6 — в активном поиске;\n"
                                          f"7 — влюблен(-а);\n"
                                          f"8 — в гражданском браке.\n"
                                          f"Форма запроса: пол, семейное положение,\n"
                                          f"возраст от, возраст до, город\n"
                                          f"Пример:\nпоиск 1,6,25,30,Москва")
                        else:
                            count = 0
                            for cand in candidates:
                                append_queries(cand, id)
                                url = get_photo_and_home_url(cand, token)
                                if url is not None:
                                    count += 1
                                    write_msg(id, f"Вариант №{count}\n"
                                                  f"Домашняя страница: {url[-1]}\n"
                                                  f"{url[:-1]}")
                    elif user_act == "token" and  "обновляем" not in msg or \
                            user_act == "token" and  "не обновляем" not in msg:
                        write_msg(id, f"При регистрации был указан неверный токен!\n"
                                      f"Будем обновлять токен?\n"
                                      f"Введите - (обновляем или не обновляем)\n")    
                    elif user_act == "token" and  msg == "обновляем" or \
                            user_act == "update" and  "новый токен" not in msg:
                        update_action_user(id, "update")
                        write_msg(id, f"Введите:\n"
                                      f"новый токен (здесь токен без скобок)\n"
                                      f"Пример:\n"
                                      f"новый токен qwc5678ebdvpfb8cbd\n")
                    elif user_act == "update" and  "новый токен" in msg:
                        update_action_user(id, "end")
                        msg_list = msg.split(" ")
                        new_token = msg_list[-1]
                        upload_data_user(id, column="token", msg=new_token)
                        write_msg(id, f"Токен успешно обновлен!\n"
                                      f"Теперь Вам доступен поиск.\n"
                                      f"пол. Возможные значения:\n" 
                                      F"1 — женщина;\n"
                                      f"2 — мужчина;\n"
                                      f"семейное положение. Возможные значения:\n"
                                      f"1 — не женат (не замужем);\n"
                                      f"2 — встречается;\n"
                                      f"3 — помолвлен(-а);\n"
                                      f"4 — женат (замужем);\n"
                                      f"5 — всё сложно;\n"
                                      f"6 — в активном поиске;\n"
                                      f"7 — влюблен(-а);\n"
                                      f"8 — в гражданском браке.\n"
                                      f"Форма запроса: пол, семейное положение,\n"
                                      f"возраст от, возраст до, город\n"
                                      f"Пример:\nпоиск 1,6,25,30,Москва")
                    elif user_act == "token" and  msg == "не обновляем":
                        write_msg(id, f"Жаль! Но мы сможем сделать это чуть позже.\n"
                                      f"Для этого напишите - (обновляем)")
                    elif user_act == "end" and "поиск" not in msg:
                            write_msg(id, f"Неверная команда!\n"
                                          f"пол. Возможные значения:\n" 
                                          F"1 — женщина;\n"
                                          f"2 — мужчина;\n"
                                          f"семейное положение. Возможные значения:\n"
                                          f"1 — не женат (не замужем);\n"
                                          f"2 — встречается;\n"
                                          f"3 — помолвлен(-а);\n"
                                          f"4 — женат (замужем);\n"
                                          f"5 — всё сложно;\n"
                                          f"6 — в активном поиске;\n"
                                          f"7 — влюблен(-а);\n"
                                          f"8 — в гражданском браке.\n"
                                          f"Форма запроса: пол, семейное положение,\n"
                                          f"возраст от, возраст до, город\n"
                                          f"Пример:\nпоиск 1,6,25,30,Москва")


if __name__ == "__main__":
    create_table()
    message_handler()
    
    


               




