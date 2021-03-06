from selenium import webdriver
from selenium.common import ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import config
import pandas as pd

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://edalnice.cz/en/bulk-purchase/index.html#/multi_eshop/batch")
driver.implicitly_wait(10)
time.sleep(3)

try:

    country = {
        'India': 'INDIA',
        'French Republic': 'FR',
        'United States': 'US',
        'Czech Republic': 'CZ',
        'Russia': 'RU',
    }

    df = pd.read_csv('sample.csv')

    """
        Reject cookies functionality
        """
    clickon_cookie_rejection = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '/html/body/footer/div[2]/div/div/div[2]/div/button[2]'))
    )
    clickon_cookie_rejection.click()
    # time.sleep(0.5)


    input_country = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.ID, "react-select-2-input"))

    )
    input_country.click()

    # time.sleep(0.1)
    input_country.send_keys(country[df['Country'][0]])
    time.sleep(1.5)
    input_country.send_keys(Keys.RETURN)

    """
    Date is being taken as input and then sent to the web page
    """
    input_date = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '/html/body/main/div/div/div/div/div/div/form/div/div[1]/div/div[2]/div[2]/div[1]/div/input'))
    )

    # input_date.click()

    input_date.send_keys(df['Validity Begins'][0])
    input_date.send_keys(Keys.RETURN)

    """
    License value is being taken as input and then sent to the web page
    """
    # input_license = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located(
    #         (By.XPATH, '//*[@id="root"]/div/form/div/div[1]/div[2]/div[3]/div/div/div[1]'))
    # )
    wait = WebDriverWait(driver, timeout=10, poll_frequency=1,
                         ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
    input_license = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/main/div/div/div/div/div/div/form/div/div[1]/div/div[3]/div/div/div[1]/input")))
    input_license.send_keys(df['License Plate'][0])
    input_license.send_keys(Keys.RETURN)
    # time.sleep(3)

    """
    If vehicle is powered by natural gas or bio-methane we click on the further checkboxes
    """

    """ This should go in a if statement when the value of
        `powered by` = 'natural gas' or 'biomethane' 
    """

    if df['Powered by'][0] == 'Natural Gas' or df['Powered by'][0] == 'Biomethane':
        input_clickon = WebDriverWait(driver, 10,
                                      ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
            EC.presence_of_element_located((By.ID, "0")))
        input_clickon.click()
        # time.sleep(1)

        if df['Powered by'][0] == 'Natural Gas':
            input_clickon_naturalgas = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '/html/body/main/div/div/div/div/div/div/form/div/div[1]/div/div[4]/div/div[2]/div[1]/div[1]/div/label'))
            )
            input_clickon_naturalgas.click()

        else:
            input_clickon_biomethane = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '/html/body/main/div/div/div/div/div/div/form/div/div[1]/div/div[4]/div/div[2]/div[1]/div[2]/div/label'))
            )
            input_clickon_biomethane.click()

    # payment functionality

    """
    Annual payment functionality
    """
    if df['Type of Vignette'][0] == 'Annual':
        clickon_annual_payment = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '//*[@id="root"]/div/form/div/div[1]/div/fieldset/div/div/div/div[1]/div/div/label/div'))
        )
        clickon_annual_payment.click()
        time.sleep(1)

    """ 
    30-day payment functionality
    """
    if df['Type of Vignette'][0] == '30-day':
        clickon_30day_payment = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '/html/body/main/div/div/div/div/div/div/form/div/div[1]/div/fieldset/div/div/div/div[2]/div/div/label/div'))
        )
        clickon_30day_payment.click()
        time.sleep(1)

    """
    10-days payment functionality
    """
    if df['Type of Vignette'][0] == '10-day':
        clickon_10day_payment = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '/html/body/main/div/div/div/div/div/div/form/div/div[1]/div/fieldset/div/div/div/div[3]/div/div/label/div'))
        )
        clickon_10day_payment.click()
        time.sleep(1)

    """
    New batch functionality
    """
    clickon_add_new_batch = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '/html/body/main/div/div/div/div/div/div/form/div/div[1]/div/div[5]/button'))
    )
    clickon_add_new_batch.click()

    """
    Minimizing the previous batch
    """
    clickon_hide_previous_batch = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '/html/body/main/div/div/div/div/div/div/form/div/div[1]/div[1]/div[1]/div/button[2]/span/span[2]'))
    )
    clickon_hide_previous_batch.click()

    # ----------------------------------------------------------------------------------------------------------------------

    for i in range(2, df.shape[0] + 1):
        input_country = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, f"react-select-{i + 1}-input"))

        )
        input_country.click()

        # time.sleep(0.1)
        input_country.send_keys(country[df['Country'][i-1]])
        time.sleep(1)
        input_country.send_keys(Keys.RETURN)

        """
        date
        """
        input_date = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 f'/html/body/main/div/div/div/div/div/div/form/div/div[1]/div[{i}]/div[2]/div[2]/div[1]/div/input'))
        )

        input_date.send_keys(df['Validity Begins'][i-1])
        input_date.send_keys(Keys.RETURN)

        """
        Licence plate input
        """

        wait = WebDriverWait(driver, timeout=10, poll_frequency=1,
                             ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
        input_license = wait.until(EC.element_to_be_clickable(
            (By.XPATH,
             f'/html/body/main/div/div/div/div/div/div/form/div/div[1]/div[{i}]/div[3]/div/div/div[1]/input')))

        input_license.send_keys(df['License Plate'][i-1])
        input_license.send_keys(Keys.RETURN)

        """
            fuel
            """

        if df['Powered by'][i - 1] == 'Natural Gas' or df['Powered by'][i - 1] == 'Biomethane':
            input_clickon = WebDriverWait(driver, 10,
                                          ignored_exceptions=[ElementNotVisibleException,
                                                              ElementNotSelectableException]).until(
                EC.presence_of_element_located((By.ID, f"{i - 1}")))
            input_clickon.click()
            # time.sleep(0.5)

            if df['Powered by'][i-1] == 'Natural Gas':
                input_clickon_naturalgas = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                         f'/html/body/main/div/div/div/div/div/div/form/div/div[1]/div[{i}]/div[4]/div/div[2]/div[1]/div[1]/div/label'
                         ))
                )
                input_clickon_naturalgas.click()
                # time.sleep(0.5)

            else:
                input_clickon_biomethane = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                         f'/html/body/main/div/div/div/div/div/div/form/div/div[1]/div[{i}]/div[4]/div/div[2]/div[1]/div[2]/div/label'
                         ))
                )
                input_clickon_biomethane.click()
                # time.sleep(0.5)

        """
            Annual payment functionality
            """

        if df['Type of Vignette'][i-1] == 'Annual':
            clickon_annual_payment = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     f'//*[@id="root"]/div/form/div/div[1]/div[{i}]/fieldset/div/div/div/div[1]/div/div/label/div'
                     ))
            )
            clickon_annual_payment.click()
            # time.sleep(0.5)

        """ 
        30-day payment functionality
        """
        if df['Type of Vignette'][i-1] == '30-day':
            clickon_30day_payment = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     f'//*[@id="root"]/div/form/div/div[1]/div[{i}]/fieldset/div/div/div/div[2]/div/div/label/div'
                     ))
            )
            clickon_30day_payment.click()
            # time.sleep(0.5)

        """
        10-days payment functionality
        """
        if df['Type of Vignette'][i-1] == '10-day':
            clickon_10day_payment = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     f'/html/body/main/div/div/div/div/div/div/form/div/div[1]/div[{i}]/fieldset/div/div/div/div[3]/div/div/label/div'
                     ))
            )
            clickon_10day_payment.click()
            # time.sleep(1)

        if i != (df.shape[0]):
            """
            New batch functionality
            """

            clickon_add_new_batch = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, f'/html/body/main/div/div/div/div/div/div/form/div/div[1]/div[{i}]/div[5]/button'))
            )
            clickon_add_new_batch.click()

        """
        Minimizing the previous batch
        """
        clickon_hide_previous_batch = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 f'/html/body/main/div/div/div/div/div/div/form/div/div[1]/div[{i}]/div[1]/div/button[2]/span/span[2]'))
        )
        clickon_hide_previous_batch.click()

    """
    click on continue for payment
    """
    clickon_continue = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,

             f'''//*[@id="root"]/div/form/div/div[2]/div/div[{df.shape[0] + len(pd.unique(df['Type of Vignette']))}]/div/button'''
             ))
    )
    clickon_continue.click()

    """
    click on continue for payment-summary
    """
    clickon_continue = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             f'//*[@id="multiEshop"]/div/div[2]/div/div[{4 + len(df[["Powered by","Type of Vignette"]].drop_duplicates())}]/div/button'))
    )
    clickon_continue.click()

    """
    Sending email
    """

    send_email = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="email-input"]'))
    )
    send_email.send_keys(config.EMAIL)

    send_confirmation_email = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="email-confirmation-input"]'))
    )
    send_confirmation_email.send_keys(config.EMAIL)
    # time.sleep(5)

# terms and condition for payment
    clickon_terms_condition = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="_termsAgreement-true"]'))
    )
    clickon_terms_condition.click()

    # Card payment radio button

    card_payment_radio_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="card_payment_radio_array_option"]'))
    )
    card_payment_radio_button.click()

    # terms of payment pay button

    pay_button_terms_conditions = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME,
             'kit__button__cont'))
    )
    pay_button_terms_conditions.click()


    # send card number
    send_card = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="cardnumber"]'))
    )
    send_card.send_keys(config.CARD_NUMBER)

    # send expiry of card
    send_expiry = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="expiry"]'))
    )
    send_expiry.send_keys(config.CARD_VALIDITY)

    # send cvv of card
    send_cvv = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="cvc"]'))
    )
    send_cvv.send_keys(config.CARD_CVV)

    # click on pay button to place order
    clickon_pay = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="pay-submit"]'))
    )
    clickon_pay.click()

    time.sleep(50)

finally:
    driver.quit()

driver.quit()