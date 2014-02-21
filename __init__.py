# -*- coding: utf-8 -*-

import requests


class Error(Exception):

    """
    Base class for exceptions in this module.
    """
    pass


class AuthenticationError(Error):

    "You must provide a valid username and password."


class Way2SMS(object):

    """
    API for way2sms (http://www.way2sms.com)
    """

    BASE_URL = 'http://site2.way2sms.com/'
    LOGIN_URL = 'http://site2.way2sms.com/Login1.action'

    def __init__(self, sender=None, password=None):
        super(Way2SMS, self).__init__()
        self.sender = sender
        self.password = password

    def login(self, sender=None, password=None):
        self.session = requests.session()

        if sender:
            self.sender = sender
        if password:
            self.password = password

        post_data = {
            'username': self.sender,
            'password': self.password
        }

        response = self.session.post(Way2SMS.LOGIN_URL, post_data)
        session_id = ''

        for cookie in self.session.cookies:
            if cookie.name == 'JSESSIONID':
                self.auth_cookie = cookie
                session_id = self.auth_cookie.value.split('~')[1]

        if not session_id in response.url:
            raise AuthenticationError(
                "You must provide a valid username and password.")
