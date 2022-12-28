from assertpy import assert_that
from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.patient_dashboard_page import PatientDashboardPage
from pages.search_addpatient_page import SearchOrAddPatientPage


def _init_page_object(context):
    context.login_page = LoginPage(context.driver)
    context.main_page = MainPage(context.driver)
    context.patient_page = PatientDashboardPage(context.driver)
    context.search_add_page = SearchOrAddPatientPage(context.driver)


@given(u'I have browser with openemr application')
def step_impl(context):
    context.driver = webdriver.Chrome()
    context.driver.maximize_window()
    context.driver.implicitly_wait(20)
    context.driver.get("https://demo.openemr.io/b/openemr")


@when(u'I enter username as "{text}"')
def step_impl(context, text):
    # context.driver.find_element(By.ID, "authUser").send_keys(text)
    context.login_page.enter_username(text)


@when(u'I enter password as "{text}"')
def step_impl(context, text):
    context.driver.find_element(By.ID, "clearPass").send_keys(text)
    context.login


@when(u'I select language as "{text}"')
def step_impl(context, text):
    select_lan = Select(context.driver.find_element(By.XPATH, "//select[@name='languageChoice']"))
    select_lan.select_by_visible_text(text)


@when(u'I click on login')
def step_impl(context):
    context.driver.find_element(By.ID, "login-button").click()


@then(u'I should get access to the portal with title as "{text}"')
def step_impl(context, text):
    assert_that(text).is_equal_to(context.driver.title)


@then(u'I should not get access to portal with error as "{text}"')
def step_impl(context, text):
    actual_error = context.driver.find_element(By.XPATH, "// *[contains(text(), 'Invalid')]").text
    assert_that(actual_error).contains(text)


@when(u'I click on patient menu')
def step_impl(context):
    context.driver.find_element(By.XPATH, "//div[text()='Patient']").click()


@when(u'I click on new-search menu')
def step_impl(context):
    context.driver.find_element(By.XPATH, "//div[text()='New/Search']").click()


@when(u'I fill the add patient form')
def step_impl(context):
    context.driver.switch_to.frame(context.driver.find_element(By.XPATH, "//iframe[@name='pat']"))
    context.driver.find_element(By.ID, "form_fname").send_keys(context.table[0]["firstname"])
    context.driver.find_element(By.ID, "form_lname").send_keys(context.table[0]["lastname"])
    context.driver.find_element(By.ID, "form_DOB").send_keys(context.table[0]["dob"])
    select_gender = Select(context.driver.find_element(By.ID, "form_sex"))
    select_gender.select_by_visible_text(context.table[0]["gender"])


@when(u'I click on create new patient')
def step_impl(context):
    context.driver.find_element(By.XPATH, "//button[@id='create']").click()
    context.driver.switch_to.default_content()


@when(u'I click on confirm create new patient')
def step_impl(context):
    context.driver.switch_to.frame(context.driver.find_element(By.XPATH, "//iframe[@id='modalframe']"))
    context.driver.find_element(By.XPATH, "//input[@value='Confirm Create New Patient']").click()
    context.driver.switch_to.default_content()


@when(u'I store the alert text and handle it')
def step_impl(context):
    wait = WebDriverWait(context.driver, 30)
    wait.until(expected_conditions.alert_is_present())
    actual_alert_text = context.driver.switch_to.alert.text
    context.driver.switch_to.alert.accept()
    print("actual_alert_text......", actual_alert_text)


@when(u'I close hbd popup if available')
def step_impl(context):
    if len(context.driver.find_elements(By.XPATH, "//div[@class ='closeDlgIframe']")) > 0:
        context.driver.find_element(By.XPATH, "//div[@class ='closeDlgIframe']").click()


@then(u'I should get the added patient detail as {expected_patient}')
def step_impl(context, expected_patient):
    context.driver.switch_to.frame(context.driver.find_element(By.XPATH, "//iframe[@name='pat']"))
    print("expected_patient..........", expected_patient)

    actual_added_paitent = context.driver.find_element(By.XPATH,
                                                       "//h2[contains(text(),'Medical Record Dashboard')]").text
    print("actual_added_paitent..........", actual_added_paitent)
    assert_that(expected_patient).contains(actual_added_paitent)


@then(u'I should validate the alert text contains {alert_text}')
def step_impl(context, alert_text):
    print("alert_text..........", alert_text)
    print("actual_alert_text..........", context.actual_alert_text)
    assert_that(context.actual_alert_text).contains(alert_text)
