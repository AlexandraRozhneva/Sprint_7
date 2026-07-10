import requests


class OrderAPI:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'
    
    @staticmethod
    def create_order(first_name, last_name, address, metro_station, phone,
                     rent_time, delivery_date, comment, color=None):
        """Создание заказа"""
        payload = {
            "firstName": first_name,
            "lastName": last_name,
            "address": address,
            "metroStation": metro_station,
            "phone": phone,
            "rentTime": rent_time,
            "deliveryDate": delivery_date,
            "comment": comment
        }
        if color:
            payload["color"] = color
            
        return requests.post(
            f'{OrderAPI.BASE_URL}/orders',
            json=payload
        )
    
    @staticmethod
    def get_orders():
        """Получение списка заказов"""
        return requests.get(
            f'{OrderAPI.BASE_URL}/orders'
        )
    
    @staticmethod
    def cancel_order(track):
        """Отмена заказа по треку"""
        return requests.put(
            f'{OrderAPI.BASE_URL}/orders/cancel',
            params={'track': track}
        )