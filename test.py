import sys
import random
import string
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QMessageBox
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt


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
    driver.get("http://127.0.0.1:8000/register/")
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


def account_logOut(driver):
    headerEmail = driver.find_element(By.XPATH, '/html/body/header/div/div/div/button')
    actions = ActionChains(driver)

    #kursor na headerEmail
    actions.move_to_element(headerEmail).perform()

    time.sleep(1)
    logOutButton = driver.find_element(By.XPATH, '/html/body/header/div/div/div/div/a[2]')
    logOutButton.click()




def go_to_main_page(driver):
    #mainpageElement = driver.find_element(By.XPATH, '')
    driver.get("http://127.0.0.1:8000")



def cancel_order(driver, self=None):
    try:
        cancel_order_button = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div/a')
        driver.execute_script("arguments[0].scrollIntoView();", cancel_order_button)
        cancel_order_button.click()
    except NoSuchElementException:
        print("Button not found")
    except Exception as e:
        QMessageBox.warning(self, 'Error', 'Button not found')



def i_payed_order(driver, self=None):
    try:
        i_payed_order_button = driver.find_element(By.XPATH, '//*[@id="processOrderButton"]')
        driver.execute_script("arguments[0].scrollIntoView();", i_payed_order_button)
        i_payed_order_button.click()
    except NoSuchElementException:
        print("Button not found")
    except Exception as e:
        QMessageBox.warning(self, 'Error', 'Button not found')





def account_login(driver, Account):
    for username, password in Account.items():

        driver.get("http://127.0.0.1:8000/login/")
        time.sleep(0.5)

        username_field = driver.find_element(By.XPATH, '//*[@id="id_username"]')
        username_field.send_keys(username)

        time.sleep(0.5)
        password_field = driver.find_element(By.XPATH, '//*[@id="id_password"]')
        password_field.send_keys(password)

        time.sleep(0.5)
        login_button = driver.find_element(By.XPATH, '/html/body/div/form/div[3]/button')
        login_button.click()


def create_exchange_order(driver, wallet_length, special_chars_in_wallet,  crypto_from, crypto_to, agreement):
    driver.get("http://localhost:8000/create_exchange_order/")
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

        # Label
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

        #Separator line ---------------------------
        hLine = QFrame()
        hLine.setFrameShape(QFrame.HLine)
        hLine.setStyleSheet("border: 2px solid #B2EBF2;")
        mainLayout.addWidget(hLine)

        browserTitleLabel = QLabel('Tests')
        browserTitleLabel.setStyleSheet("font-size: 15px; font-weight: bold; color: #00796B; padding: 10px 0;")
        browserTitleLabel.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(browserTitleLabel)

        #Registration Test Case
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

        #Login Test Case
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

        #Create Order Test Case
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

        # Separator line ---------------------------
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
                QMessageBox.warning(self, 'Error', 'Log Out Failed: ' + str(e))


    def iPayed(self):
        i_payed_order(self.driver)


    def cancelOrder(self):
        cancel_order(self.driver)


    def mainPage(self):
        go_to_main_page(self.driver)


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
            self.create_orderCase4()
        elif create_order_case == "User agreement not confirmed":
            self.create_orderCase5()

    def testShortPassword(self):
        username = username_generator()
        password = password_generator(4, True, False)
        register_user(self.driver, username,password)

    def testSimplePassword(self):
        username = username_generator()
        password = "12345678"
        print(password)
        register_user(self.driver, username, password)

    def testUsernameSimilarToPassword(self):
        username = "banan782cccc"
        password = 'banan782cccc'
        register_user(self.driver, username, password)


    def testAlreadyUsedUsername(self):
        username = "test12"
        password = password_generator(12, True, False)
        register_user(self.driver, username, password)


    def testGoodCase_registation(self):
        self.username = username_generator()
        password = password_generator(12, True, False)
        self.username, self.password = register_user(self.driver, self.username, password)

    def goodCaseLogin(self):
        time.sleep(1)
        username = "orels"
        password = "12345"
        Account = {username: password}
        account_login(self.driver, Account)


    def incorrectLogin(self):
        time.sleep(1)
        Account = {"error": "error"}
        account_login(self.driver, Account)

    def createOrderGoodCase(self):
        create_exchange_order(self.driver, 17, False, "BTC", "USDT", True)

        #wallet bad cases
    def include_special_chars(self):
        create_exchange_order(self.driver, 17, True, "BTC", "USDT", True)

    def too_short_wallet(self):
        create_exchange_order(self.driver, 8, True, "BTC", "USDT", True)

        #crypro_to is same to crypto_from
    def create_orderCase4(self):
        create_exchange_order(self.driver, 17, False, "USDT", "USDT", True)

        #user agreement not confirmed
    def create_orderCase5(self):
        create_exchange_order(self.driver, 17, False, "XMR", "USDT", False)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SeleniumTestGUI()
    ex.show()
    sys.exit(app.exec_())
