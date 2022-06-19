from db.create_db import SearchQueries, User, session


# Проверяем есть ли пользователь с таким айди в БД
def check_for_registration(id: int): 
    response = session.query(User.id_vk).filter(User.id_vk==id).all() 
    if response == []:
        return False
    return True


# Регистрация нового пользователя
def reg_new_user(id: int, action: str, names: str, tokens: str):
    user = User(id_vk=id, action=action, name=names, token=tokens)
    session.add(user)
    session.commit()


# Удаляем пользователя из БД, который отказался регистрироваться
def delete_user(id: int):
    session.query(User).filter(User.id_vk == id).delete()
    session.commit()


# Получаем действия пользователя
def get_action_user(id: int):
    response = session.query(User.action).filter(User.id_vk==id)[0][0]
    return response


# Обновляем флаг 
def update_action_user(id: int, act: str):
    session.query(User).filter(User.id_vk == id).update({"action": f"{act}"})
    session.commit()


# Обновляем данные о пользователе  
def upload_data_user(id: int, column: str, msg: str):
    session.query(User).filter(User.id_vk == id).update({f"{column}": f"{msg}"})
    session.commit()


# Добавляем запросы в БД, чтобы в дальнейшем избежать повторяющихся ответов
def append_queries(candidates: int, id_quer: int):
    new_list = []
    new_list.append(candidates)
    for id in new_list:
        data = SearchQueries(id_response=id, id_queries=id_quer)
        session.add(data)
    session.commit()


# Получаем токен пользователя
def get_token(id):
    response = session.query(User.token).filter(User.id_vk==id).first()[0]
    return response
    

# Проверяем ответ запроса на уникальность
def checking_for_uniqueness(id):
    search_list = []
    response = session.query(SearchQueries.id_response).filter(SearchQueries.id_queries==id).all()
    for id in response:
        search_list.append(id[0])
    return search_list

    









