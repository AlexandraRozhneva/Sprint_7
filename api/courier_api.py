import requests


class CourierAPI:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'
    
    @staticmethod
    def create_courier(login, password, first_name=None):
        """Создание курьера"""
        payload = {
            "login": login,
            "password": password
        }
        if first_name:
            payload["firstName"] = first_name
            
        return requests.post(
            f'{CourierAPI.BASE_URL}/courier',
            data=payload
        )
    
    @staticmethod
    def login_courier(login, password):
        """Авторизация курьера"""
        payload = {
            "login": login,
            "password": password
        }
        return requests.post(
            f'{CourierAPI.BASE_URL}/courier/login',
            data=payload
        )
    
    @staticmethod
    def delete_courier(courier_id):
        """Удаление курьера"""
        return requests.delete(
            f'{CourierAPI.BASE_URL}/courier/{courier_id}'
        )