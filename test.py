import sys
import random
import string
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QMessageBox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
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


def password_generator(length, include_special_chars):
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


def register_user(driver, username, password_length=12, include_special_chars=True):
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
    password = password_generator(password_length, include_special_chars)
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



def account_login(driver, Account):
    for username, password in Account.items():
        login_header_button = driver.find_element(By.XPATH, '//*[@id="login-button"]')
        login_header_button.click()
        time.sleep(0.5)

        username_field = driver.find_element(By.XPATH, '//*[@id="id_username"]')
        username_field.send_keys(username)

        time.sleep(0.5)
        password_field = driver.find_element(By.XPATH, '//*[@id="id_password"]')
        password_field.send_keys(password)

        time.sleep(0.5)
        login_button = driver.find_element(By.XPATH, '/html/body/div/form/div[3]/button')
        login_button.click()


def create_exchange_order(driver):
    driver.get("http://localhost:8000/create_exchange_order/")
    time.sleep(1)
    email_field = driver.find_element(By.XPATH, '//*[@id="id_email"]')
    email = email_generator()
    email_field.send_keys(email)



class SeleniumTestGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.driver = None

    def initUI(self):
        self.setWindowTitle('Selenium Test GUI')
        self.setGeometry(100, 100, 500, 250)

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
        self.startBrowserButton.setStyleSheet("background-color: #B2EBF2; padding: 5px;")
        self.startBrowserButton.clicked.connect(self.startBrowser)
        mainLayout.addWidget(self.startBrowserButton)

        # Separator line ---------------------------
        hLine = QFrame()
        hLine.setFrameShape(QFrame.HLine)
        hLine.setStyleSheet("border: 2px solid #B2EBF2;")
        mainLayout.addWidget(hLine)

        browserTitleLabel = QLabel('Tests')
        browserTitleLabel.setStyleSheet("font-size: 15px; font-weight: bold; color: #00796B; padding: 10px 0;")
        browserTitleLabel.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(browserTitleLabel)

        testCaseLayout = QHBoxLayout()
        self.testCaseLabel = QLabel('Choose Registration Test Case:')
        testCaseLayout.addWidget(self.testCaseLabel)
        self.testCaseCombo = QComboBox()
        self.testCaseCombo.addItems(
            ['Short Password', 'Simple Password', 'Already Used Username', 'Username Similar to Password', 'Good Case'])
        testCaseLayout.addWidget(self.testCaseCombo)
        mainLayout.addLayout(testCaseLayout)

        loginCaseLayout = QHBoxLayout()
        self.loginCaseLabel = QLabel('Choose Login Test Case:')
        loginCaseLayout.addWidget(self.loginCaseLabel)
        self.loginCaseCombo = QComboBox()
        self.loginCaseCombo.addItems(['Good Case', 'Incorrect Login/Pass'])
        loginCaseLayout.addWidget(self.loginCaseCombo)
        mainLayout.addLayout(loginCaseLayout)

        orderCaseLayout = QHBoxLayout()
        self.orderCaseLabel = QLabel('Choose Create Order Test Case:')
        orderCaseLayout.addWidget(self.orderCaseLabel)
        self.orderCaseCombo = QComboBox()
        self.orderCaseCombo.addItems(['Good Case', 'Incorrect Wallet Address'])
        orderCaseLayout.addWidget(self.orderCaseCombo)
        mainLayout.addLayout(orderCaseLayout)

        # Separator line ---------------------------
        hLine = QFrame()
        hLine.setFrameShape(QFrame.HLine)
        hLine.setStyleSheet("border: 2px solid #B2EBF2;")
        mainLayout.addWidget(hLine)

        browserTitleLabel = QLabel('Buttons')
        browserTitleLabel.setStyleSheet("font-size: 15px; font-weight: bold; color: #00796B; padding: 10px 0;")
        browserTitleLabel.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(browserTitleLabel)

        self.registerButton = QPushButton('Run Registration Test')
        self.registerButton.clicked.connect(self.handleRegistration)
        mainLayout.addWidget(self.registerButton)

        self.loginButton = QPushButton('Run Login Test')
        self.loginButton.clicked.connect(self.handleLogin)
        mainLayout.addWidget(self.loginButton)

        self.createOrderButton = QPushButton('Run Create Order Test')
        self.createOrderButton.clicked.connect(self.handleCreateOrder)
        mainLayout.addWidget(self.createOrderButton)

        self.logOutButton = QPushButton('Log Out')
        self.logOutButton.clicked.connect(self.logOut)
        mainLayout.addWidget(self.logOutButton)

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
            self.testGoodCase()

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
            self.createOrderIncorrectWallet()

    def testShortPassword(self):
        username = username_generator()
        register_user(self.driver, username, 4, True)

    def testSimplePassword(self):
        pass

    def testAlreadyUsedUsername(self):
        time.sleep(1)
        username = "test12"
        register_user(self.driver, username, 12, True)

    def testUsernameSimilarToPassword(self):
        pass

    def testGoodCase(self):
        time.sleep(1)
        self.username = username_generator()
        self.username, self.password = register_user(self.driver, self.username, 12, True)

    def goodCaseLogin(self):
        time.sleep(1)
        Account = {self.username: self.password}
        #print(Account)
        account_login(self.driver, Account)

    def incorrectLogin(self):
        time.sleep(1)
        Account = {"error": "error"}
        account_login(self.driver, Account)

    def createOrderGoodCase(self):
        time.sleep(1)
        create_exchange_order(self.driver)

    def createOrderIncorrectWallet(self):
        pass





        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SeleniumTestGUI()
    ex.show()
    sys.exit(app.exec_())
