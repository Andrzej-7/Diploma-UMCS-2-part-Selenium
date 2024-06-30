import sys
import random
import string
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QMessageBox
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt


#links
main_page_link = 'http://localhost:8000'
login_page_link = 'http://localhost:8000/login/'
register_page_link = 'http://localhost:8000/register/'
create_EO_link = 'http://localhost:8000/create_exchange_order/'




def username_generator():
    words = ["apple", "banana", "cherry", "jake", "Martini"]
    word = random.choice(words)
    number = random.randint(0, 999)
    return f"{word}{number}"


def email_generator():
    words = ["cool", "fast", "smart", "happy", "bright"]
    domains = ["example.com", "mail.com", "test.org", "demo.net", "gmail.com", "outlook.com", "yahoo.com"]

    word = random.choice(words)
    domain = random.choice(domains)
    number = random.randint(1, 9999)
    email = f"{word}{number}@{domain}"

    return email


def password_generator(length, include_special_chars, simple_password):

    easy_password = "11111"
    if not simple_password:
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        digits = string.digits
        special_chars = string.punctuation if include_special_chars else ''

        all_chars = lower + upper + digits + special_chars

        password = random.choice(lower) + random.choice(upper) + random.choice(digits)
        if include_special_chars:
            password += random.choice(special_chars)

        password += ''.join(random.choice(all_chars) for _ in range(length - len(password)))

        password = ''.join(random.sample(password, len(password)))

        return password
    else:
        return easy_password


def wallet_generator(length, include_special_chars, crypto_option):
    if include_special_chars:
        characters = string.ascii_letters + string.digits + string.punctuation
    else:
        characters = string.ascii_letters + string.digits

    random_string = ''.join(random.choice(characters) for _ in range(length))
    wallet = crypto_option + random_string

    return wallet


def register_user(driver, username, password):
    try:
        driver.get(register_page_link)

        time.sleep(1)
        username_element = driver.find_element(By.XPATH, '//*[@id="id_username"]')
        username_element.send_keys(username)

        time.sleep(1)
        email_element = driver.find_element(By.XPATH, '//*[@id="id_email"]')
        email = email_generator()
        email_element.send_keys(email)

        time.sleep(1)
        password_element1 = driver.find_element(By.XPATH, '//*[@id="id_password1"]')
        password_element1.send_keys(password)

        time.sleep(1)
        password_element2 = driver.find_element(By.XPATH, '//*[@id="id_password2"]')
        password_element2.send_keys(password)

        time.sleep(1)
        register_button = driver.find_element(By.XPATH, '/html/body/div/form/div[5]/button')
        register_button.send_keys(Keys.ENTER)

        return username, password
    except NoSuchElementException as e:
        print("element not found")
        return None, None
    except ElementNotInteractableException as e:
        print("element not interactable")
        return None, None
    except Exception as e:
        QMessageBox.warning(None, 'Error', 'Registration failed: ' + str(e))
        return None, None




def account_logOut(driver):
        try:
            headerEmail = driver.find_element(By.XPATH, '/html/body/header/div/div/div/button')
            driver.execute_script("arguments[0].scrollIntoView(true);", headerEmail)
            #js FIND SCROLL and CLICK functions, because of strange error in selenium implementation version
            driver.execute_script("arguments[0].click();", headerEmail)
            time.sleep(0.5)
            logOutButton = driver.find_element(By.XPATH, '/html/body/header/div/div/div/div/a')
            driver.execute_script("arguments[0].scrollIntoView(true);", logOutButton)
            driver.execute_script("arguments[0].click();", logOutButton)

        except NoSuchElementException:
            print("Button not found")
        except Exception as e:
            QMessageBox.warning(None, 'Error', 'log out  failed: ' + str(e))




def go_to_main_page(driver):
    driver.get(main_page_link)



def cancel_order(driver):
    try:
        cancel_order_button = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div/a')
        driver.execute_script("arguments[0].scrollIntoView();", cancel_order_button)
        cancel_order_button.click()
    except NoSuchElementException:
        print("Button not found")
    except ElementNotInteractableException:
        print("Button is not interactable")
    except Exception as e:
        QMessageBox.warning(None, 'Error', 'Cancel Order failed: ' + str(e))



def i_payed_order(driver):
    try:
        i_payed_order_button = driver.find_element(By.XPATH, '//*[@id="processOrderButton"]')
        driver.execute_script("arguments[0].scrollIntoView();", i_payed_order_button)
        i_payed_order_button.click()
    except NoSuchElementException:
        print("Button not found")
    except ElementNotInteractableException:
        print("Button is not interactable")
    except Exception as e:
        QMessageBox.warning(None, 'Error', 'Payment processing failed: ' + str(e))






def account_login(driver, Account):
    try:
        for username, password in Account.items():

            driver.get(login_page_link)
            time.sleep(0.5)

            username_field = driver.find_element(By.XPATH, '//*[@id="id_username"]')
            username_field.send_keys(username)

            time.sleep(0.5)
            password_field = driver.find_element(By.XPATH, '//*[@id="id_password"]')
            password_field.send_keys(password)

            time.sleep(0.5)
            login_button = driver.find_element(By.XPATH, '/html/body/div/form/div[3]/button')
            login_button.click()

    except NoSuchElementException as e:
        print("element not found")
        return None, None
    except ElementNotInteractableException as e:
        print("element not interactable")
        return None, None
    except Exception as e:
        QMessageBox.warning(None, 'Error', 'login failed: ' + str(e))
        return None, None


def create_exchange_order(driver, wallet_length, special_chars_in_wallet,  crypto_from, crypto_to, agreement):
    try:
        driver.get(create_EO_link)


        time.sleep(1)
        email_field = driver.find_element(By.XPATH, '//*[@id="id_email"]')
        email = email_generator()
        email_field.send_keys(email)

        crypto_from_xpath = " "

        if crypto_from == "BTC":
            crypto_from_xpath = '/html/body/div/form/div[3]/select/option[1]'
        elif crypto_from == "ETH":
            crypto_from_xpath = '/html/body/div/form/div[3]/select/option[2]'
        elif crypto_from == "XMR":
            crypto_from_xpath = '/html/body/div/form/div[3]/select/option[3]'
        elif crypto_from == "DAI":
            crypto_from_xpath = '/html/body/div/form/div[3]/select/option[4]'
        elif crypto_from == "BNB":
            crypto_from_xpath = '/html/body/div/form/div[3]/select/option[5]'
        elif crypto_from == "USDT":
            crypto_from_xpath = '/html/body/div/form/div[3]/select/option[6]'
        elif crypto_from == "LTC":
            crypto_from_xpath = '/html/body/div/form/div[3]/select/option[7]'
        elif crypto_from == "XLM":
            crypto_from_xpath = '/html/body/div/form/div[3]/select/option[8]'
        elif crypto_from == "ADA":
            crypto_from_xpath = '/html/body/div/form/div[3]/select/option[9]'
        elif crypto_from == "XRP":
            crypto_from_xpath = '/html/body/div/form/div[3]/select/option[10]'


        time.sleep(0.5)
        crypto_from_field = driver.find_element(By.XPATH, crypto_from_xpath)
        crypto_from_field.click()

        amount_field = driver.find_element(By.XPATH, '//*[@id="id_amount"]')
        amount_field.send_keys(random.randint(10, 100))
        time.sleep(0.5)

        crypto_to_xpath = " "

        if crypto_to == "BTC":
            crypto_to_xpath = '/html/body/div/form/div[5]/select/option[1]'
        elif crypto_to == "ETH":
            crypto_to_xpath = '/html/body/div/form/div[5]/select/option[2]'
        elif crypto_to == "XMR":
            crypto_to_xpath = '/html/body/div/form/div[5]/select/option[3]'
        elif crypto_to == "DAI":
            crypto_to_xpath = '/html/body/div/form/div[5]/select/option[4]'
        elif crypto_to == "BNB":
            crypto_to_xpath = '/html/body/div/form/div[5]/select/option[5]'
        elif crypto_to == "USDT":
            crypto_to_xpath = '/html/body/div/form/div[5]/select/option[6]'
        elif crypto_to == "LTC":
            crypto_to_xpath = '/html/body/div/form/div[5]/select/option[7]'
        elif crypto_to == "XLM":
            crypto_to_xpath = '/html/body/div/form/div[5]/select/option[8]'
        elif crypto_to == "ADA":
            crypto_to_xpath = '/html/body/div/form/div[5]/select/option[9]'
        elif crypto_to == "XRP":
            crypto_to_xpath = '/html/body/div/form/div[5]/select/option[10]'

        crypto_to_field = driver.find_element(By.XPATH, crypto_to_xpath)
        crypto_to_field.click()
        time.sleep(0.5)


        wallet = wallet_generator(wallet_length, special_chars_in_wallet, crypto_to)


        wallet_field = driver.find_element(By.XPATH, '//*[@id="id_recipient_wallet"]')
        wallet_field.send_keys(wallet)
        time.sleep(0.5)


        if agreement:
            agreement_field = driver.find_element(By.XPATH, '//*[@id="agreementCheckbox"]')
            agreement_field.click()
            time.sleep(0.5)


        exchange_now_button = driver.find_element(By.XPATH, '//*[@id="submitBtn"]')
        exchange_now_button.click()

    except NoSuchElementException:
        print("Button not found")
        return None, None
    except ElementNotInteractableException:
        print("Button is not interactable")
        return None, None
    except Exception as e:
        QMessageBox.warning(None, 'Error', 'Payment processing failed: ' + str(e))
        return None, None




class SeleniumTestGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.driver = None

    def initUI(self):
        self.setWindowTitle('Selenium Test GUI')
        self.setGeometry(100, 100, 800, 300)

        mainLayout = QVBoxLayout()
        self.setStyleSheet("background-color: #E0F7FA;")

        #label
        browserTitleLabel = QLabel('Browser')
        browserTitleLabel.setStyleSheet("font-size: 15px; font-weight: bold; color: #00796B; padding: 10px 0;")
        browserTitleLabel.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(browserTitleLabel)

        browserLayout = QHBoxLayout()
        self.browserLabel = QLabel('Choose Browser:')
        browserLayout.addWidget(self.browserLabel)
        self.browserCombo = QComboBox()
        self.browserCombo.addItems(['Firefox', 'Chrome', 'Edge'])
        browserLayout.addWidget(self.browserCombo)
        mainLayout.addLayout(browserLayout)

        self.startBrowserButton = QPushButton('Start Browser')
        self.startBrowserButton.setStyleSheet("background-color: #cef1f8; padding: 5px;")
        self.startBrowserButton.clicked.connect(self.startBrowser)
        mainLayout.addWidget(self.startBrowserButton)

        #separator line ---------------------------
        hLine = QFrame()
        hLine.setFrameShape(QFrame.HLine)
        hLine.setStyleSheet("border: 2px solid #B2EBF2;")
        mainLayout.addWidget(hLine)

        browserTitleLabel = QLabel('Tests')
        browserTitleLabel.setStyleSheet("font-size: 15px; font-weight: bold; color: #00796B; padding: 10px 0;")
        browserTitleLabel.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(browserTitleLabel)

        #registration test case
        registrationLayout = QHBoxLayout()
        self.testCaseLabel = QLabel('Choose Registration Test Case:')
        registrationLayout.addWidget(self.testCaseLabel)
        self.testCaseCombo = QComboBox()
        self.testCaseCombo.addItems(
            ['Good Case', 'Short Password',
             'Simple Password', 'Already Used Username',
             'Username Similar to Password'])
        registrationLayout.addWidget(self.testCaseCombo)

        self.registerButton = QPushButton('Run Registration Test')
        self.registerButton.setStyleSheet("background-color:#cef1f8; padding: 5px;")
        self.registerButton.clicked.connect(self.handleRegistration)
        registrationLayout.addWidget(self.registerButton)

        mainLayout.addLayout(registrationLayout)

        #login test case
        loginLayout = QHBoxLayout()
        self.loginCaseLabel = QLabel('Choose Login Test Case:')
        loginLayout.addWidget(self.loginCaseLabel)
        self.loginCaseCombo = QComboBox()
        self.loginCaseCombo.addItems(['Good Case', 'Incorrect Login/Pass'])
        loginLayout.addWidget(self.loginCaseCombo)

        self.loginButton = QPushButton('Run Login Test')
        self.loginButton.setStyleSheet("background-color: #cef1f8; padding: 5px;")
        self.loginButton.clicked.connect(self.handleLogin)
        loginLayout.addWidget(self.loginButton)

        mainLayout.addLayout(loginLayout)

        #create order test case
        orderLayout = QHBoxLayout()
        self.orderCaseLabel = QLabel('Choose Create Order Test Case:')
        orderLayout.addWidget(self.orderCaseLabel)
        self.orderCaseCombo = QComboBox()
        self.orderCaseCombo.addItems(['Good Case', 'Incorrect Wallet Address',
                                      'Too Short Wallet Address',
                                      'Crypto From & Crypto To is same',
                                      'User agreement not confirmed'])
        orderLayout.addWidget(self.orderCaseCombo)

        self.createOrderButton = QPushButton('Run Create Order Test')
        self.createOrderButton.setStyleSheet("background-color: #cef1f8; padding: 5px;")
        self.createOrderButton.clicked.connect(self.handleCreateOrder)
        orderLayout.addWidget(self.createOrderButton)

        mainLayout.addLayout(orderLayout)

        #separator line ---------------------------
        hLine = QFrame()
        hLine.setFrameShape(QFrame.HLine)
        hLine.setStyleSheet("border: 2px solid #B2EBF2;")
        mainLayout.addWidget(hLine)

        browserTitleLabel = QLabel('Buttons')
        browserTitleLabel.setStyleSheet("font-size: 15px; font-weight: bold; color: #00796B; padding: 10px 0;")
        browserTitleLabel.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(browserTitleLabel)

        self.logOutButton = QPushButton('Log Out')
        self.logOutButton.setStyleSheet("background-color: #cef1f8; padding: 5px;")
        self.logOutButton.clicked.connect(self.logOut)
        mainLayout.addWidget(self.logOutButton)

        self.iPayedButton = QPushButton('I Payed')
        self.iPayedButton.setStyleSheet("background-color: #cef1f8; padding: 5px;")
        self.iPayedButton.clicked.connect(self.iPayed)
        mainLayout.addWidget(self.iPayedButton)

        self.cancelOrderButton = QPushButton('Cancel Order')
        self.cancelOrderButton.setStyleSheet("background-color: #cef1f8; padding: 5px;")
        self.cancelOrderButton.clicked.connect(self.cancelOrder)
        mainLayout.addWidget(self.cancelOrderButton)

        self.mainPageButton = QPushButton('Main Page')
        self.mainPageButton.setStyleSheet("background-color: #cef1f8; padding: 5px;")
        self.mainPageButton.clicked.connect(self.mainPage)
        mainLayout.addWidget(self.mainPageButton)

        self.setLayout(mainLayout)






    def startBrowser(self):

        if self.driver:
            QMessageBox.warning(self, 'Error', 'A browser is already running')
            return

        browser_choice = self.browserCombo.currentText()
        if browser_choice == 'Firefox':
            self.driver = webdriver.Firefox()
        elif browser_choice == 'Chrome':
            self.driver = webdriver.Chrome()
        elif browser_choice == 'Edge':
            self.driver = webdriver.Edge()
        else:
            QMessageBox.warning(self, 'Error', 'Unsupported browser!')
        QMessageBox.information(self, 'Browser Started', f'{browser_choice} browser has been started.')



    def logOut(self):
        if self.driver:
            try:
                account_logOut(self.driver)
            except Exception as e:
                print(f"Log Out error: {e}")
                QMessageBox.warning(self, 'Error', 'Log Out Failed: ' + str(e))


    def iPayed(self):
        if self.driver:
            try:
                i_payed_order(self.driver)
            except Exception as e:
                QMessageBox.warning(self, 'Error', 'Payment Processing failed: ' + str(e))

    def cancelOrder(self):
        if self.driver:
            try:
                cancel_order(self.driver)
            except Exception as e:
                QMessageBox.warning(self, 'Error', 'Cancel Order failed: ' + str(e))


    def mainPage(self):
        if self.driver:
            try:
                go_to_main_page(self.driver)
            except Exception as e:
                QMessageBox.warning(self, 'Error', 'navigate to main page failed: ' + str(e))


    def handleRegistration(self):
        if not self.driver:
            QMessageBox.warning(self, 'Error', 'Please start a browser first.')
            return
        test_case = self.testCaseCombo.currentText()
        if test_case == 'Short Password':
            self.testShortPassword()
        elif test_case == 'Simple Password':
            self.testSimplePassword()
        elif test_case == 'Already Used Username':
            self.testAlreadyUsedUsername()
        elif test_case == 'Username Similar to Password':
            self.testUsernameSimilarToPassword()
        elif test_case == 'Good Case':
            self.testGoodCase_registation()


    def handleLogin(self):
        if not self.driver:
            QMessageBox.warning(self, 'Error', 'Please start a browser first.')
            return
        login_case = self.loginCaseCombo.currentText()

        if login_case == 'Good Case':
            self.goodCaseLogin()
        elif login_case == 'Incorrect Login/Pass':
            self.incorrectLogin()



    def handleCreateOrder(self):
        if not self.driver:
            QMessageBox.warning(self, 'Error', 'Please start a browser first.')
            return

        create_order_case = self.orderCaseCombo.currentText()
        if create_order_case == 'Good Case':
            self.createOrderGoodCase()
        elif create_order_case == 'Incorrect Wallet Address':
            self.include_special_chars()
        elif create_order_case == 'Too Short Wallet Address':
            self.too_short_wallet()
        elif create_order_case == "Crypto From & Crypto To is same":
            self.crypto_choises_same()
        elif create_order_case == "User agreement not confirmed":
            self.user_agr_not_conf()


#registration tests
    def testShortPassword(self):
        username = username_generator()
        password = password_generator(4, True, False)
        register_user(self.driver, username,password)

    def testSimplePassword(self):
        username = username_generator()
        password = "12345678"
        register_user(self.driver, username, password)

    def testUsernameSimilarToPassword(self):
        username = "banan782cccc"
        password = 'banan782cccc'
        register_user(self.driver, username, password)


    def testAlreadyUsedUsername(self):
        username = "adminUMCS"
        password = password_generator(12, True, False)
        register_user(self.driver, username, password)

    def testGoodCase_registation(self):
        self.username = username_generator()
        password = password_generator(12, True, False)
        self.username, self.password = register_user(self.driver, self.username, password)



#login tests

    def goodCaseLogin(self):
        time.sleep(1)
        username = "adminUMCS"
        password = "12345"
        Account = {username: password}
        account_login(self.driver, Account)


    def incorrectLogin(self):
        time.sleep(1)
        Account = {"error": "error"}
        account_login(self.driver, Account)



#create order tests
    def createOrderGoodCase(self):
        create_exchange_order(self.driver, 17, False, "BTC", "USDT", True)

    def include_special_chars(self):
        create_exchange_order(self.driver, 17, True, "BTC", "USDT", True)

    def too_short_wallet(self):
        create_exchange_order(self.driver, 8, True, "BTC", "USDT", True)

    def crypto_choises_same(self):
        create_exchange_order(self.driver, 17, False, "USDT", "USDT", True)

    def user_agr_not_conf(self):
        create_exchange_order(self.driver, 17, False, "XMR", "USDT", False)


#to close browser when gui closed
    def closeBrowser(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def closeEvent(self, event):
        self.closeBrowser()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SeleniumTestGUI()
    ex.show()
    sys.exit(app.exec_())
