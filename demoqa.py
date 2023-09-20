import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome()


class Base:
    def __init__(self):
        self.driver = driver
        self.url = 'https://demoqa.com/'
        self.wait = WebDriverWait(self.driver, timeout=10)

    def open_url(self):
        self.driver.maximize_window()
        self.driver.get(self.url)

    def close_driver(self):
        self.driver.quit()

    def wait_for_visibility_of_el(self, by, element_locator):
        """Цей метод очікує, поки е-нт стане видимим на стрінці"""
        return self.wait.until(EC.visibility_of_element_located((by, element_locator)))

    def wait_for_visibility_of_all_elements(self, by, element_locator):
        """Цей метод очікує, поки ЕЛЕМЕНТИ стануть видимии на стрінці"""
        return self.wait.until(EC.visibility_of_all_elements_located((by, element_locator)))


class InitPage(Base):
    """початкова сторінка: містить локатори веб елементів та методи для взаємодії з ними"""
    btn_elements = '//*[@id="app"]/div/div/div[2]/div/div[1]'

    def click_on_btn_elements(self):
        self.wait_for_visibility_of_el(By.XPATH, InitPage.btn_elements).click()


class HeaderSection(Base):
    """хедер сайту: містить локатори веб елементів та методи для взаємодії з ними"""
    header = 'div[class="main-header"]'

    def get_header_name(self):
        return self.wait_for_visibility_of_el(By.CSS_SELECTOR, HeaderSection.header).text


class MenuBar(Base):
    """панель меню: містить локатори веб елементів та методи для взаємодії з ними"""
    menu_btn_text_box = '//span[text()="Text Box"]'
    menu_btn_check_box = '//span[text()="Check Box"]'
    menu_btn_radio_button = '//span[text()="Radio Button"]'
    menu_btn_web_tables = '//span[text()="Web Tables"]'

    def click_on_btn_text_box(self):
        self.wait_for_visibility_of_el(By.XPATH, MenuBar.menu_btn_text_box).click()


class ElementsPage(Base):
    """сторінка Elements"""
    header = HeaderSection()
    menu = MenuBar()


class TextBoxPage(Base):
    header = HeaderSection()
    menu = MenuBar()


class TestBase:
    base = Base()

    def open_site(self):
        self.base.open_url()

    def close_site(self):
        # TestBase.base.close_driver()
        self.base.close_driver()


class TestElements(TestBase):
    def test_text_box(self):
        self.open_site()
        """відкрилась URL"""
        time.sleep(3)
        InitPage().click_on_btn_elements()
        """відклилась стрінка Elements"""
        time.sleep(3)
        ElementsPage().menu.click_on_btn_text_box()
        """відкрилась стрінка TextBox після кліку на кнпку text_box в меню на стрінці Elements"""
        time.sleep(3)
        header_name_text_box_pg = TextBoxPage().header.get_header_name()
        """перевірка тайтлу сторінки: """
        assert header_name_text_box_pg == 'Text Box'


