import requests
import random
import string


def generate_random_string(length=10):
    """Генерирует случайную строку из букв нижнего регистра"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def register_new_courier_and_return_login_password():
    """
    Регистрирует нового курьера и возвращает список [логин, пароль, имя]
    Если регистрация не удалась, возвращает пустой список
    """
    login_pass = []
    
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    
    response = requests.post(
        'https://qa-scooter.praktikum-services.ru/api/v1/courier',
        data=payload
    )
    
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)
    
    return login_pass


def delete_courier(courier_id):
    """Удаляет курьера по ID"""
    if courier_id:
        response = requests.delete(
            f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}'
        )
        return response


def login_courier(login, password):
    """Авторизует курьера и возвращает его ID"""
    payload = {
        "login": login,
        "password": password
    }
    response = requests.post(
        'https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
        data=payload
    )
    if response.status_code == 200:
        return response.json().get('id')
    return None