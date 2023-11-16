from selenium import webdriver
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('d:\chrome\chromedriver.exe')
    pytest.driver.implicitly_wait(4)
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()


def test_show_my_pets():
#    pytest.driver.implicitly_wait(4)

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
    assert pytest.driver.find_element('tag name', 'h1').text == "PetFriends"

    images = pytest.driver.find_elements('css selector', '.card-deck .card-img-top')
    names = pytest.driver.find_elements('css selector', '.card-deck .card-title')
    descriptions = pytest.driver.find_elements('css selector', '.card-deck .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0

