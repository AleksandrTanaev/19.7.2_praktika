import os

from api import PetFriends
from settings import valid_email, valid_password
from settings import invalid_email, invalid_password


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result



def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key,filter)
    assert status == 200
    assert len(result['pets']) > 0



def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")



def test_add_pets_with_valid_data_without_photo(name='КотБезФото', animal_type='кот', age='6'):
        '''Проверяем возможность добавления нового питомца без фото'''
        _, api_key = pf.get_api_key(valid_email, valid_password)
        status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

        assert status == 200
        assert result['name'] == name



def test_add_photo_at_pet(pet_photo='images/Cat1.jpg'):
        '''Проверяем возможность добавления новой фотографии питомца'''
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        _, api_key = pf.get_api_key(valid_email, valid_password)
        _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

        if len(my_pets['pets']) > 0:
            status, result = pf.add_photo_of_pet(api_key, my_pets['pets'][0]['id'], pet_photo)

            _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

            assert status == 200
            assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
        else:
            raise Exception("Питомцы отсутствуют")



def test_get_api_key_with_wrong_password_and_correct_mail(email=valid_email, password=invalid_password):
        '''Проверяем запрос с невалидным паролем и с валидным емейлом.
        Проверяем нет ли ключа в ответе'''
        status, result = pf.get_api_key(email, password)
        assert status == 403
        assert 'key' not in result


def test_get_api_key_with_wrong_email_and_correct_password(email=invalid_email, password=valid_password):
        '''Проверяем запрос с невалидным паролем и с валидным емейлом.
        Проверяем нет ли ключа в ответе'''
        status, result = pf.get_api_key(email, password)
        assert status == 403
        assert 'key' not in result

