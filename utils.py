# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup as bs


def get_way2sms_data(page_response, token, recipient, message):
    page_response = bs(page_response)
    inputs = page_response.findAll('input')
    pjkdws = page_response.findAll('input', attrs={'name': 'pjkdws'})
    post_data = {}

    for inp in inputs:
        if not inp.get('name'):
            continue
        elif inp['name'] == 't_15_k_5':
            post_data['t_15_k_5'] = inp['value']
            post_data[inp['value']] = token
            post_data['Token'] = token
        elif inp['name'] == 'a_m_p':
            post_data['a_m_p'] = inp['value']
        elif inp['name'] == 'm_15_b':
            post_data['m_15_b'] = inp['value']
            post_data[inp['value']] = str(recipient)
        elif inp['name'] == 'adno':
            post_data['adno'] = inp['value']
        elif inp['name'] == 'catnamedis':
            post_data['catnamedis'] = inp['value']
        elif inp['name'] == 'smsActTo':
            post_data['smsActTo'] = inp['value']
        elif inp['name'] == 'logemail':
            post_data['logemail'] = inp['value']
        print inp['name']
    
    if pjkdws:
        post_data['pjkdws'] = pjkdws[0]['value']
    
    scripts = page_response.findAll('script')
    special_script = [item for item in page_response.findAll('script')
                      if 'document.createElement("input")' in item.text]
    if special_script:
        ids = [eval(item)[1]
               for item in re.findall("(\(.*?\))", special_script[0].text) if '"id"' in item]
        special_char = [item for item in ids
                        if item not in post_data.values()][0]
        print special_char
        post_data[special_char] = ''

    post_data['textArea'] = message
    post_data['textfield2'] = '+91'
    post_data['txtLen'] = 140
    post_data['Send'] = 'Send SMS'
    post_data['hop'] = ''
    post_data['way2s'] = 'way2s'

    return post_data
