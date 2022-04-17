import unittest
from app_config.AppConfig import AppConfig
from tests.TestCaseBase import TestCaseBase


class TestAppConfig(TestCaseBase):

    def test_AppConfig(self):
        config = AppConfig()
        email = config.get_account_param('MS','email')
        self.assertLessEqual('michal.salwin@gmail.com',email)

        name = config.get('sendinblue','from_name')
        self.assertLessEqual('Zdrofit',name)


if __name__ == '__main__':
    unittest.main()