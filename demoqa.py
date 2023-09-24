import time

from faker import Faker
from selenium import webdriver
from selenium.webdriver import ActionChains
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

    def scroll_to_web_element(self, by, element_locator):
        # .move_by_offset(0, 50) - цим мтдом переміщаю додтково курсор миші вниз на 50 пікселів від поточнго положення
        # Цей код спершу переміщує курсор миші до заданого ел-та, а потім переміщує його вниз на 50 пікселів від поточного положення елемента.
        return ActionChains(self.driver).move_to_element(self.driver.find_element(by, element_locator)).move_by_offset(0, 50).perform()

    def scroll_into_view(self, wait_for_):
        self.driver.execute_script("arguments[0].scrollIntoView();", wait_for_)

    def remove_advertising_in_footer(self):
        self.driver.execute_script('document.getElementById("adplus-anchor").remove();')
        self.driver.execute_script('document.getElementsByTagName("footer")[0].remove();')
        # [0] - він туть тому що метод getElementsByTagName - поверт список елмнтів ElementS!
        # і з цього спску беру 0-вий (1-ший), навіть якшо він єдиний в списку


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

    txt_full_name = 'input[id="userName"]'
    txt_email = 'input[id="userEmail"]'
    txt_current_address = 'textarea[id="currentAddress"]'
    txt_permanent_address = 'textarea[id="permanentAddress"]'
    btn_submit = 'button[id="submit"]'

    fake = Faker(locale='uk_UA')
    fake_full_name = fake.name()
    fake_email = fake.email()
    fake_current_address = fake.address()
    fake_permanent_address = fake.address()


    def set_full_name(self):
        self.wait_for_visibility_of_el(By.CSS_SELECTOR, TextBoxPage.txt_full_name).send_keys(TextBoxPage.fake_full_name)

    def set_email(self):
        self.wait_for_visibility_of_el(By.CSS_SELECTOR, TextBoxPage.txt_email).send_keys(TextBoxPage.fake_email)

    def set_current_address(self):
        self.wait_for_visibility_of_el(By.CSS_SELECTOR, TextBoxPage.txt_current_address).send_keys(TextBoxPage.fake_current_address)

    def set_permanent_address(self):
        self.wait_for_visibility_of_el(By.CSS_SELECTOR, TextBoxPage.txt_permanent_address).send_keys(TextBoxPage.fake_permanent_address)

    # def scroll_to_btn_submit(self):
    #     self.scroll_to_web_element(By.CSS_SELECTOR, TextBoxPage.btn_submit)
    #
    # def click_on_btn_submit(self):
    #     self.wait_for_visibility_of_el(By.CSS_SELECTOR, TextBoxPage.btn_submit).click()

    def scroll_and_click_on_btn_submit(self):
        p = self.wait_for_visibility_of_el(By.CSS_SELECTOR, TextBoxPage.btn_submit)
        self.scroll_into_view(p)
        time.sleep(6)
        p.click()


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
        InitPage().click_on_btn_elements()
        """відклилась стрінка Elements"""
        ElementsPage().menu.click_on_btn_text_box()
        """відкрилась стрінка TextBox після кліку на кнпку text_box в меню на стрінці Elements"""
        time.sleep(3)
        textbox_pg = TextBoxPage()
        header_name_text_box_pg = textbox_pg.header.get_header_name()
        """перевірка тайтлу сторінки: """
        assert header_name_text_box_pg == 'Text Box'
        """заповнення полей: ім'я, емейл, адреса та клік submit"""
        textbox_pg.set_full_name()
        textbox_pg.set_email()
        textbox_pg.set_current_address()
        textbox_pg.set_permanent_address()
        time.sleep(4)
        textbox_pg.remove_advertising_in_footer()
        time.sleep(6)
        # textbox_pg.scroll_to_btn_submit()
        # time.sleep(4)
        # textbox_pg.click_on_btn_submit()
        textbox_pg.scroll_and_click_on_btn_submit()
        time.sleep(4)
        # self.close_site()



