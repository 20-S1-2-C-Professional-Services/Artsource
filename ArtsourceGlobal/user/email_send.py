from random import Random  # generate random code
from django.core.mail import send_mail  # the module used for sending email
from user.models import EmailVerifyRecord
from django.conf import settings
from user import models
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


# TODO: change the referee_email
# send email that verify user by system
def send_code_email(email, referee_email='', send_type="register", real_name='', is_artist=False):
    """
    :param is_artist: check the register is for artist or not
    :param referee_email: the email of referee's email
    :param real_name: the real name of user when verify as artist
    :param email: the email address used for sending email
    :param send_type: retrieve or verification
    :return: True/False
    """
    email_record = EmailVerifyRecord()
    # store these info into database
    code = random_str(16)
    while models.EmailVerifyRecord.objects.filter(code=code):
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.send_time = datetime.datetime.now()
    email_record.save()

    if send_type == "register":
        if is_artist:
            email_title = "register verification for " + real_name
            email_body = "Register email is {registered_email}, use the blow link to activate {artist}'s " \
                         "account: http://127.0.0.1:8000/active/{random_code}".format(random_code=code,
                                                                                      artist=real_name,
                                                                                      registered_email=email)
            send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [referee_email])
        else:
            email_title = "register verification"
            email_body = "use the blow link to activate your account: http://127.0.0.1:8000/active/{0}".format(code)
            send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if not send_status:
            return False
    if send_type == "reset":
        email_title = "reset password"
        email_body = "The retrieve password link is: http://127.0.0.1:8000/reset/{0}".format(code)
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if not send_status:
            return False
    return True
