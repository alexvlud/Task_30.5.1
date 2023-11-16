from selenium import webdriver
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('d:\chrome\chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()


def test_show_my_pets():
    element = WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_element_located((By.ID, "pass"))
    )
    # Вводим email
    pytest.driver.find_element('id', 'email').send_keys('student.tester@bk.ru')
    # Вводим пароль
    pytest.driver.find_element('id', 'pass').send_keys('123')

    # Нажимаем на кнопку входа в аккаунт
    element = WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_element_located(('css selector', 'button[type="submit"]'))
    )

    pytest.driver.find_element('css selector', 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    element = WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_element_located(('css selector', 'a[href="/my_pets"]'))
    )
    pytest.driver.find_element('css selector', 'a[href="/my_pets"]').click()

    #### Присутствуют все питомцы.
    # собираем своих питомцев из таблицы
    element = WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_element_located(('xpath', '//tbody'))
    )

    my_pets_from_table = pytest.driver.find_elements('xpath', '//tbody/tr')
    # берем количество питомцев из статистики
    element = WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_element_located(('xpath', "//div[@class='.col-sm-4 left']"))
    )

    my_pets_from_info = pytest.driver.find_element('xpath', "//div[@class='.col-sm-4 left']")
    # парсим текст статистики для получения количества питомцев
    strings = my_pets_from_info.text.split("\n")
    parts = strings[1].split(":")
    # проверяем, что присутствуют все питомцы.
    assert len(my_pets_from_table) == int(parts[1])

    ### половина имеет фотки
    # собираем все тэги изображения в таблице питомцев и считаем количество непустых (питомцев с фото)
    with_photo = 0
    images = pytest.driver.find_elements('xpath', "//tbody/tr/th/img")
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            with_photo += 1

    # проверка, что хотя бы у половины питомцев есть фото.
    assert with_photo >= int(parts[1]) - with_photo

    ### таблица питомцев
    # проверка, что у всех питомцев есть имя, возраст и порода (и крестик удаления)
    my_pets_table_td = pytest.driver.find_elements('xpath', '//tbody/tr/td')
    for i in range(len(my_pets_table_td)):
        assert my_pets_table_td[i].text != ''

    # проверка, что у всех питомцев разные имена
    names = []
    count = -1
    for i in range(0, len(my_pets_table_td) - 1, 4):
        names.append(my_pets_table_td[i].text.lower())
        count += 1
        for j in range(count):
            assert my_pets_table_td[i].text.lower() != names[j]

    # проверка, что в списке нет повторяющихся питомцев.

    all_pets = []
   #объединяем все тексты, кроме последнего крестика, в строку.
    for i in range(len(my_pets_table_td)-1):
       all_pets.append(my_pets_table_td[i].text.lower())

    pets_str = ''.join(all_pets)
    # создаем список из строк с данными питомцев, разделяя общую строку по крестику
    all_pets_split = pets_str.split("×")
#    print(pets_str)
    print(all_pets_split)
# проверка, что в списке нет повторяющихся питомцев
    for i in range(len(all_pets_split)):
       for j in range(i+1, len(all_pets_split)):
          assert all_pets_split[i] != all_pets_split[j]


