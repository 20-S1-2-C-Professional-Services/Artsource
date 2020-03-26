from random import Random  # generate random code
from django.core.mail import send_mail  # the module used for sending email
from user.models import EmailVerifyRecord
from django.conf import settings

import datetime


# generate random string
def random_str(length=8):
    """
    random string
    :param length: length of string
    :return: String
    """
    string = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(length):
        string += chars[random.randint(0, length)]
    return string


# send email that verify user by system
def send_code_email(email, send_type="register"):
    """
    :param email: the email address used for sending email
    :param send_type: retrieve or verification
    :return: True/False
    """
    email_record = EmailVerifyRecord()
    # store these info into database
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.send_time = datetime.datetime.now()
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "register verification"
        email_body = "use the blow link to activate your account: http://127.0.0.1:8000/active/{0}".format(code)
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if not send_status:
            return False
    if send_type == "retrieve":
        email_title = "retrieve password"
        email_body = "The retrieve password link is: http://127.0.0.1:8000/retrieve/{0}".format(code)
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if not send_status:
            return False
    return True
