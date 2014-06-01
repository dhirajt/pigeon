# -*- coding: utf-8 -*-

import requests

from .utils import get_way2sms_data

class Error(Exception):

    """
    Base class for exceptions in this module.
    """
    pass


class AuthenticationError(Error):

    """
    You must provide a valid number and password.
    """
    pass


class SendError(Error):

    """
    You must provide a valid number and message.
    """
    pass


class MessageLengthExceededError(Error):

    """
    Message length cannot be more than 140 characters.
    """
    pass

class Way2SMS(object):

    """
    API for way2sms (http://www.way2sms.com)
    """

    BASE_URL = 'http://site2.way2sms.com/'
    LOGIN_URL = 'http://site2.way2sms.com/Login1.action'
    SMSKEYS_URL = 'http://site2.way2sms.com/singles.action'
    SMS_URL = 'http://site2.way2sms.com/smstoss.action'

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
                self.token = self.auth_cookie.value.split('~')[1]

        if not self.token in response.url:
            raise AuthenticationError(
                "You must provide a valid number and password.")

    def sendsms(self, receipient=None, message=None):
        if not receipient or not message:
            raise SendError("You must provide a valid number and message.")

        if len(message)>140:
            raise MessageLengthExceededError("Message length cannot be more than 140 characters.")
        
        response = self.session.get(Way2SMS.SMSKEYS_URL,params={'Token':self.token})
        
        post_data = get_way2sms_data(response.text,self.token,receipient,message)
        
        response = self.session.post(Way2SMS.SMS_URL, post_data)