#!/usr/bin/python3
__version__ = "1.0.0"
__author__ = "Smartwa Caleb"


class handler:
    def __init__(self):
        pass

    def get_args(self):
        import argparse

        parser = argparse.ArgumentParser(description="Automate GPT3 login-process")
        parser.add_argument(
            "-v", "--version", action="version", version=f"%(prog)s v{__version__}"
        )
        parser.add_argument("email", help="Google mail-address")
        parser.add_argument("password", help="Passphrase for the account")
        parser.add_argument("-d", "--driver", help="Absolute path to chromedriver")
        parser.add_argument(
            "-se",
            "--session",
            help="Total session time in minutes",
            type=int,
            default=30,
        )
        parser.add_argument(
            "--incognito", help="Run browser in incognito mode", action="store_true"
        )
        return parser.parse_args()

    def log(self):
        import logging

        logging.basicConfig(
            format="%(asctime)s - %(levelname)s : %(message)s",
            datefmt="%d-%b-%Y %H:%M:%S",
            level=logging.INFO,
        )
        return logging

    def main(self):
        return self.get_args(), self.log()


args, logging = handler().main()
import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep as wait
from sys import exit


class gpt3:
    def __init__(self):
        options = webdriver.ChromeOptions()
        for val in [
            "--start-maximized",
            "--incognito" if args.incognito else None,
        ]:
            if val:
                options.add_argument(val)
        args_to_be_passed = {
            "options": options,
        }
        if args.driver:
            args_to_be_passed["driver_executable_path"] = args.driver
        self.get_error = lambda err: str(err).split("\n")[0]
        self.driver = webdriver.Chrome(**args_to_be_passed)

    def login(self, email: str, password: str):
        """Controls the login process.
        :param email: Your google e-mail account address
        :param password: E-mail address passphrase.
        """
        try:
            self.driver.get("https://platform.openai.com/playground")
            self.driver.find_element(By.CLASS_NAME, "btn-label-inner").click()
            self.driver.find_element(
                By.XPATH, '//button[@data-provider="google"]'
            ).click()
            self.enter_email(email)
            wait(2)
            self.enter_password(password)
        except Exception as e:
            exit(logging.error(self.get_error(e)))

    def enter_email(self, email: str):
        try:
            email_elm = self.driver.find_element(By.XPATH, '//input[@type="email"]')
            email_elm.send_keys(email)
            email_elm.send_keys(Keys.ENTER)
        except Exception as e:
            exit(logging.error(self.get_error(e)))

    def enter_password(self, password: str):
        logging.debug("Keying-in password")
        try:
            password_elm = self.driver.find_element(
                By.XPATH, '//input[@type="password"]'
            )
            password_elm.click()
            password_elm.send_keys(password)
            password_elm.send_keys(Keys.ENTER)
            self.driver.implicitly_wait(2)
        except Exception as e:
            exit(logging.error(self.get_error(e)))
        else:
            logging.info("Login successfully")


if __name__ == "__main__":
    logging.info("GPT3 Started")
    start = gpt3()
    try:
        start.login(email=args.email, password=args.password)
        wait(args.session * 60)
    except (KeyboardInterrupt, EOFError):
        exit(logging.info("Stopping program!"))
    except Exception as e:
        logging.critical(start.get_error(e))
    finally:
        start.driver.quit()
