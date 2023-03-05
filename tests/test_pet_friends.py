from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()

# Тест1
def test_get_auth_key_for_empty_reg_fields(email='', password=''):
    '''Проверяем возможность входа в приложение без ввода данных электронной почты и пароля.
     Запрос API на возврат статуса 403 в связи с отсутствием в запросе данных пользователя'''

    status, result = pf.get_api_key(email, password)

    assert status == 403
    print(result)

# Тест 2
def test_get_api_key_for_not_valid_user(email=valid_email, password=invalid_password):
    """ Проверяем что при вводе неверных данных запрос api ключа возвращает статус 403"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    print('Неверно указан логин или пароль')

# Тест 3
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result
    print('Ключ:', result)

# Тест 4
def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0



# Тест 5
def test_add_new_pet_with_valid_data_without_photo(name='Соня', animal_type='собака',
                                                   age='4'):
    """Проверяем, что можно добавить питомца с корректными данными без фото"""


    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

# Тест 6
def test_add_new_empty_pet(name='', animal_type='', age=''):
    '''Проверяем возможность добавления нового питомца без данных.'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    print(result)

# Тест 7
def test_add_new_pet_invalid_age(name='Старик', animal_type='черепах', age='1000'):
    '''Проверка добавления нового питомца без фото с некорректными данными возраста.'''

    # Запрашиваем ключ API и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем ожидаемый и фактический результат
    assert status == 200
    assert result['name'] == name
    assert result['age'] != 0
    print(result)


# Тест 8
def test_successful_delete_self_pet():
    """Проверка возможности удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Булка", "собака", "1", "images/Р1040103.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    print('ID удаляемого питомца:', pet_id)
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


# Тест 9
def test_successful_update_self_pet_info_pet_id(name='Багира', animal_type='гепард', age=2):
    """Проверяем возможность обновления информации о питомце с несуществующим pet_id"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    pet_id = 'pet'
    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)

    # Проверяем что статус ответа = 400 и такого питомца не существует
    assert status == 400
    print('Предоставленные данные не верны. Проверьте правильность написания pet_id')

# Тест 10
def test_get_auth_key_with_invalid_key(filter="my_pets"):
    """ Проверяем, что запрос "моих питомцев" при запросе с неверно указанным ключом ничего не возвращает """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets({'key': '123'}, filter)
    assert status == 403
    print(result)
