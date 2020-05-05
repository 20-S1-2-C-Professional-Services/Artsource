from django.core.mail import send_mail  # the module used for sending email
from django.conf import settings


# send email that verify user by system
def send_notify_email(email, renter_name, artwork_name, email_type):
    """
    """
    send_status = True
    if email_type == 'book':
        email_title = "Your artwork " + artwork_name + " booked out!"
        email_body = "Renter is {renter_name}, please come to the website manage this order ".format(renter_name=renter_name)
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])

    elif email_type == 'accept':
        email_title = "The artwork " + artwork_name + " booked accepted by its owner!"
        email_body = "Congratulations! {renter_name}, please come to the website manage this order ".format(
            renter_name=renter_name)
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])

    elif email_type == 'cancel':
        email_title = "The book of artwork " + artwork_name + " was canceled"
        email_body = "Renter is {renter_name}, please come to the website manage this order ".format(renter_name=renter_name)
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])

    return send_status

