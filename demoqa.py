import random
import time
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
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

    def scroll_js(self, wait_for_):
        """Цей метод переміщує курсор миші до заданого ел-та за доп JS"""
        self.driver.execute_script("arguments[0].scrollIntoView();", wait_for_)

    def remove_advertising_in_footer(self):
        """Цей метод видаляє рекламу в футері"""
        self.driver.execute_script('document.getElementById("adplus-anchor").remove();')
        self.driver.execute_script('document.getElementsByTagName("footer")[0].remove();')


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

    def click_on_btn_check_box(self):
        self.wait_for_visibility_of_el(By.XPATH, MenuBar.menu_btn_check_box).click()

    def click_on_btn_radio_button(self):
        self.wait_for_visibility_of_el(By.XPATH, MenuBar.menu_btn_radio_button).click()

    def click_on_btn_web_tables(self):
        self.wait_for_visibility_of_el(By.XPATH, MenuBar.menu_btn_web_tables).click()


class ElementsPage(Base):
    """сторінка Elements"""
    header = HeaderSection()
    menu = MenuBar()


class FakeData:
    def __init__(self):
        self.fake = Faker(locale='uk_UA')
        self.fake_full_name = self.fake.name()
        self.fake_email = self.fake.email()
        self.fake_current_address = self.fake.address()
        self.fake_permanent_address = self.fake.address()
        self.fake_first_name = self.fake.first_name()
        self.fake_last_name = self.fake.last_name()
        self.fake_age = random.randint(18, 79)
        self.fake_salary = random.randint(1000, 20000)
        self.list_departments = ['Insurance', 'Compliance', 'Legal']
        self.fake_department = self.list_departments[random.randint(0, 2)]


class TextBoxPage(Base):
    """сторінка Text Box: містить локатори веб елементів та методи для взаємодії з ними"""
    header = HeaderSection()
    menu = MenuBar()
    fake = FakeData()

    txt_full_name = 'input[id="userName"]'
    txt_email = 'input[id="userEmail"]'
    txt_current_address = 'textarea[id="currentAddress"]'
    txt_permanent_address = 'textarea[id="permanentAddress"]'
    btn_submit = 'button[id="submit"]'

    output_full_name = 'p[id="name"]'
    output_email = 'p[id="email"]'
    output_current_address = 'p[id="currentAddress"]'
    output_permanent_address = 'p[id="permanentAddress"]'

    def set_full_name(self):
        self.wait_for_visibility_of_el(By.CSS_SELECTOR, TextBoxPage.txt_full_name).send_keys(TextBoxPage.fake.fake_full_name)
        return TextBoxPage.fake.fake_full_name

    def set_email(self):
        self.wait_for_visibility_of_el(By.CSS_SELECTOR, TextBoxPage.txt_email).send_keys(TextBoxPage.fake.fake_email)
        return TextBoxPage.fake.fake_email

    def set_current_address(self):
        self.wait_for_visibility_of_el(By.CSS_SELECTOR, TextBoxPage.txt_current_address).send_keys(TextBoxPage.fake.fake_current_address)
        return TextBoxPage.fake.fake_current_address

    def set_permanent_address(self):
        self.wait_for_visibility_of_el(By.CSS_SELECTOR, TextBoxPage.txt_permanent_address).send_keys(TextBoxPage.fake.fake_permanent_address)
        return TextBoxPage.fake.fake_permanent_address

    def scroll_and_click_on_btn_submit(self):
        button_submit = self.wait_for_visibility_of_el(By.CSS_SELECTOR, TextBoxPage.btn_submit)
        self.scroll_js(button_submit)
        time.sleep(2)
        button_submit.click()

    def get_output_full_name(self):
        full_name = self.wait_for_visibility_of_el(By.CSS_SELECTOR, TextBoxPage.output_full_name).text
        split_full_name = full_name.split(sep=':')
        return split_full_name[1]

    def get_output_email(self):
        email = self.wait_for_visibility_of_el(By.CSS_SELECTOR, TextBoxPage.output_email).text
        split_email = email.split(sep=':')
        return split_email[1]

    def get_output_current_address(self):
        current_address = self.wait_for_visibility_of_el(By.CSS_SELECTOR, TextBoxPage.output_current_address).text
        split_current_address = current_address.split(sep=':')
        return split_current_address[1]

    def get_output_permanent_address(self):
        permanent_address = self.wait_for_visibility_of_el(By.CSS_SELECTOR, TextBoxPage.output_permanent_address).text
        split_permanent_address = permanent_address.split(sep=':')
        return split_permanent_address[1]


class CheckBoxPage(Base):
    """сторінка Check Box: містить локатори веб елементів та методи для взаємодії з ними"""
    header = HeaderSection()
    menu = MenuBar()

    btn_expand_all = 'button[title="Expand all"]'
    titles_of_checkboxes = '[class="rct-title"]'

    def click_on_btn_expand_all(self):
        self.wait_for_visibility_of_el(By.CSS_SELECTOR, CheckBoxPage.btn_expand_all).click()

    def click_on_random_checkboxes(self):
        """Клік рандомну непарну к-сть разів на рандомні чекбокси"""
        list_of_all_checkboxes = self.wait_for_visibility_of_all_elements(By.CSS_SELECTOR, CheckBoxPage.titles_of_checkboxes)
        for i in range(3, 9, 2):
            random_number = random.randint(1, 16)
            random_checkbox = list_of_all_checkboxes[random_number]
            self.scroll_js(random_checkbox)
            random_checkbox.click()

    def get_titles_of_checked_checkboxes(self):
        """цей метод повертає назви всіх відмічених чекбоксів"""
        checked_checkboxes = self.wait_for_visibility_of_all_elements(By.CSS_SELECTOR, '[class="rct-icon rct-icon-check"]')
        ancestor_for_checked_checkboxes = './/ancestor::span[@class="rct-text"]'
        titles_of_checked_checkboxes = []
        for i in checked_checkboxes:
            find_ancestor = i.find_element(By.XPATH, ancestor_for_checked_checkboxes)
            titles_of_checked_checkboxes.append(find_ancestor.text.lower().replace(".doc", '').replace(" ", ''))
        return titles_of_checked_checkboxes

    def get_output_result(self):
        """цей метод повертає назви чекбоксів, що виводяться в рядку 'You have selected' """
        row_of_selected_checkboxes = self.wait_for_visibility_of_all_elements(By.XPATH, '//div/span[@class="text-success"]')
        list_of_selected_checkboxes = []
        for i in row_of_selected_checkboxes:
            list_of_selected_checkboxes.append(i.text.lower().replace(" ", ''))
        return list_of_selected_checkboxes


class RadioButtonPage(Base):
    """сторінка Radio Button: містить локатори веб елементів та методи для взаємодії з ними"""
    header = HeaderSection()
    radio_buttons = "//label[contains(@class, 'custom-control-label')]"
    output_text = '[class="text-success"]'

    preceding_sibling_for_radio_btns = ".//preceding-sibling::input"

    def click_on_radio_buttons_and_get_output_text(self):
        """цей метод повертає списки: 1й містить усі назви клікнутих радіобатонів,
        2й список - назви радіобатонів, що відображались на сторінці після тексту 'You have selected' """
        list_of_radio_buttons = self.wait_for_visibility_of_all_elements(By.XPATH, RadioButtonPage.radio_buttons)
        list_of_input_titles = []
        list_of_output_titles = []
        for i in list_of_radio_buttons:
            find_a_preceding_sibling = i.find_element(By.XPATH, RadioButtonPage.preceding_sibling_for_radio_btns)
            if find_a_preceding_sibling.is_enabled():
                list_of_input_titles.append(i.text)
                i.click()
                list_of_output_titles.append(
                    self.wait_for_visibility_of_el(By.CSS_SELECTOR, RadioButtonPage.output_text).text)
        return list_of_input_titles, list_of_output_titles


class WebTablesPage(Base):
    header = HeaderSection()
    fake = FakeData()
    email_fake = fake.fake_email

    btn_add = 'button[id="addNewRecordButton"]'
    txt_first_name = 'input[id="firstName"]'
    txt_last_name = 'input[id="lastName"]'
    txt_user_email = 'input[id="userEmail"]'
    txt_age = 'input[id="age"]'
    txt_salary = 'input[id="salary"]'
    txt_department = 'input[id="department"]'
    btn_submit = 'button[id="submit"]'
    rows = 'div[class="rt-tr-group"]'

    txt_search = 'input[id="searchBox"]'
    btn_edit = '[title="Edit"]'
    btn_delete = '[title="Delete"]'
    the_checking_text = '[class="rt-noData"]'

    btn_the_quantity_of_rows = 'select[aria-label="rows per page"]'

    def click_on_btn_add(self):
        """цей метод відкриває Registration form"""
        self.wait_for_visibility_of_el(By.CSS_SELECTOR, WebTablesPage.btn_add).click()

    def fill_in_fields_on_the_registration_form(self):
        """цей метод дозволяє заповнити поля в Registration form"""
        self.wait_for_visibility_of_el(By.CSS_SELECTOR, WebTablesPage.txt_first_name).send_keys(WebTablesPage.fake.fake_first_name)
        self.wait_for_visibility_of_el(By.CSS_SELECTOR, WebTablesPage.txt_last_name).send_keys(WebTablesPage.fake.fake_last_name)
        self.wait_for_visibility_of_el(By.CSS_SELECTOR, WebTablesPage.txt_user_email).send_keys(WebTablesPage.email_fake)
        self.wait_for_visibility_of_el(By.CSS_SELECTOR, WebTablesPage.txt_age).send_keys(WebTablesPage.fake.fake_age)
        self.wait_for_visibility_of_el(By.CSS_SELECTOR, WebTablesPage.txt_salary).send_keys(WebTablesPage.fake.fake_salary)
        self.wait_for_visibility_of_el(By.CSS_SELECTOR, WebTablesPage.txt_department).send_keys(WebTablesPage.fake.fake_department)
        return f'{WebTablesPage.fake.fake_first_name} {WebTablesPage.fake.fake_last_name} {WebTablesPage.fake.fake_age} {WebTablesPage.email_fake} {WebTablesPage.fake.fake_salary} {WebTablesPage.fake.fake_department}'

    def click_on_btn_submit(self):
        self.wait_for_visibility_of_el(By.CSS_SELECTOR, WebTablesPage.btn_submit).click()

    def get_text_from_rows(self):
        """цей метод повертає список значень всіх рядків таблиці"""
        list_rows = self.wait_for_visibility_of_all_elements(By.CSS_SELECTOR, WebTablesPage.rows)
        txt_from_rows = []
        for i in list_rows:
            txt_from_rows.append(i.text.replace('\n', ' '))
        return txt_from_rows

    def perform_search_by_email(self, email=email_fake):
        """цей метод виконує пошук за ел адресою"""
        self.wait_for_visibility_of_el(By.CSS_SELECTOR, WebTablesPage.txt_search).clear()
        self.wait_for_visibility_of_el(By.CSS_SELECTOR, WebTablesPage.txt_search).send_keys(email)
        return email

    def set_new_email(self):
        """апдейт емейлу"""
        self.wait_for_visibility_of_el(By.CSS_SELECTOR, WebTablesPage.btn_edit).click()
        user_email = self.wait_for_visibility_of_el(By.CSS_SELECTOR, WebTablesPage.txt_user_email)
        user_email.clear()
        fake_data = FakeData()
        user_email.send_keys(fake_data.fake_email)
        self.click_on_btn_submit()
        return fake_data.fake_email

    def remove_record(self):
        """цей метод видаляє новий запис з таблиці"""
        self.wait_for_visibility_of_el(By.CSS_SELECTOR, WebTablesPage.btn_delete).click()

    def get_the_checking_text(self):
        """цей метод повертає текст, який підтверджує, що рядок з заданим емейлом не знайдено """
        return self.wait_for_visibility_of_el(By.CSS_SELECTOR, WebTablesPage.the_checking_text).text

    def quantity_of_rows(self):
        """цей метод: 1)змінює к-сть рядків таблиці що відображаються на сторінці;
        2) підраховує к-сть рядків, що фактично відображено в таблиці"""
        wait_for_btn_the_quantity_of_rows = self.wait_for_visibility_of_el(By.CSS_SELECTOR, WebTablesPage.btn_the_quantity_of_rows)
        select = Select(wait_for_btn_the_quantity_of_rows)
        list_of_options = select.options
        list_of_clicked_options = []
        list_of_counted_rows = []

        for i in list_of_options:
            self.scroll_js(wait_for_btn_the_quantity_of_rows)
            i.click()
            list_of_clicked_options.append(i.text.replace(' rows', ''))
            actual_quantity_rows = self.wait_for_visibility_of_all_elements(By.CSS_SELECTOR, WebTablesPage.rows)
            list_of_counted_rows.append(str(len(actual_quantity_rows)))
        return list_of_clicked_options, list_of_counted_rows


class TestBase:
    base = Base()

    def open_site(self):
        self.base.open_url()

    def close_site(self):
        # TestBase.base.close_driver()
        self.base.close_driver()


class TestElements(TestBase):
    def test_text_box_page(self):
        self.open_site()
        """відкрилась URL"""
        InitPage().click_on_btn_elements()
        """відклилась стрінка Elements"""
        ElementsPage().menu.click_on_btn_text_box()
        """відкрилась стрінка TextBox після кліку на кнпку text_box в меню на стрінці Elements"""
        time.sleep(3)
        textbox_pg = TextBoxPage()
        textbox_pg_header_name = textbox_pg.header.get_header_name()
        """перевірка тайтлу сторінки: """
        assert textbox_pg_header_name == 'Text Box'
        """заповнення полей: ім'я, емейл, адреса та клік submit"""
        input_full_name = textbox_pg.set_full_name()
        input_email = textbox_pg.set_email()
        input_current_address = textbox_pg.set_current_address()
        input_permanent_address = textbox_pg.set_permanent_address()
        textbox_pg.remove_advertising_in_footer()
        textbox_pg.scroll_and_click_on_btn_submit()
        """поміщаю в змінні вихідні дані: ім'я, емейл, адреси"""
        output_full_name = textbox_pg.get_output_full_name()
        output_email = textbox_pg.get_output_email()
        output_current_address = textbox_pg.get_output_current_address()
        output_permanent_address = textbox_pg.get_output_permanent_address()

        assert output_full_name == input_full_name
        assert output_email == input_email
        assert output_current_address == input_current_address
        assert output_permanent_address == input_permanent_address
        # self.close_site()

    def test_check_box_page(self):
        self.open_site()
        InitPage().click_on_btn_elements()
        ElementsPage().menu.click_on_btn_check_box()
        time.sleep(3)
        checkbox_pg = CheckBoxPage()
        checkbox_pg_header_name = checkbox_pg.header.get_header_name()
        """перевірка тайтлу сторінки: """
        assert checkbox_pg_header_name == 'Check Box'
        checkbox_pg.click_on_btn_expand_all()
        time.sleep(2)
        checkbox_pg.click_on_random_checkboxes()
        time.sleep(2)
        """назви всіх відмічених чекбоксів"""
        titles_of_checked_checkboxes = checkbox_pg.get_titles_of_checked_checkboxes()
        """назви чекбоксів, що виводяться в рядку 'You have selected' """
        output_result = checkbox_pg.get_output_result()

        assert titles_of_checked_checkboxes == output_result
        # self.close_site()

    def test_radio_button_page(self):
        self.open_site()
        InitPage().click_on_btn_elements()
        ElementsPage().menu.click_on_btn_radio_button()
        radiobutton_pg = RadioButtonPage()
        radiobutton_pg_header_name = radiobutton_pg.header.get_header_name()
        """перевірка тайтлу сторінки: """
        assert radiobutton_pg_header_name == 'Radio Button', 'there is an error in the title on the Radio Button page'

        """асьорт списків, де 1й список містить усі назви клікнутих радіобатонів , 
        а 2й список - назви радіобатонів, що відображались на сторінці після тексту 'You have selected' """
        list_of_input_titles, list_of_output_titles = radiobutton_pg.click_on_radio_buttons_and_get_output_text()
        assert list_of_input_titles == list_of_output_titles
        # self.close_site()

    def test_web_tables_page(self):
        self.open_site()
        InitPage().click_on_btn_elements()
        ElementsPage().menu.click_on_btn_web_tables()
        web_tables_pg = WebTablesPage()
        web_tables_pg_header_name = web_tables_pg.header.get_header_name()
        """перевірка тайтлу сторінки: """
        assert web_tables_pg_header_name == "Web Tables", 'there is an error in the title on the Web Tables page'

        """додавання нового запису в таблицю"""
        web_tables_pg.click_on_btn_add()
        input_data = web_tables_pg.fill_in_fields_on_the_registration_form()
        web_tables_pg.click_on_btn_submit()
        output_data = web_tables_pg.get_text_from_rows()
        """перевірка чи новий запис додано в таблицю"""
        assert input_data in output_data

        """виконання пошуку по емейлу"""
        the_search_email = web_tables_pg.perform_search_by_email()
        output_data_after_performing_the_search = web_tables_pg.get_text_from_rows()
        first_result_field = output_data_after_performing_the_search[0]
        """перевірка чи є емейл в першому рядку результату пошуку"""
        assert the_search_email in first_result_field

        """апдейт емейлу"""
        new_email = web_tables_pg.set_new_email()
        """пошук по новому емейлу, перевірка чи є він в першому рядку результату пошуку"""
        web_tables_pg.perform_search_by_email(new_email)
        output_data_after_performing_the_search_with_a_new_email = web_tables_pg.get_text_from_rows()
        first_result_field_with_a_new_email = output_data_after_performing_the_search_with_a_new_email[0]
        assert new_email in first_result_field_with_a_new_email

        """видалення реклами в футері"""
        web_tables_pg.remove_advertising_in_footer()
        """видалення нового запису з таблиці"""
        web_tables_pg.remove_record()
        the_checking_text = web_tables_pg.get_the_checking_text()
        assert the_checking_text == 'No rows found', 'after removing a new record, the message "No rows found" does not appear'

        """перевірка чи обрані опції к-сті рядків відповідають фактичній к-сті рядків відображених на сторінці"""
        list_of_clicked_options, list_of_counted_rows = web_tables_pg.quantity_of_rows()
        assert list_of_clicked_options == list_of_counted_rows
        # self.close_site()

