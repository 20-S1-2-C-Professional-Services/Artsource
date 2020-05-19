from django.core.mail import send_mail  # the module used for sending email
from django.conf import settings


# send email that verify user by system
def send_notify_email(email, name, postcode, max_price, min_price,
                      max_length, min_length, max_width, min_width, max_height, min_height, additionalnotes):
    """
    """
    send_status = True

    # TODO: change the admin_email to JILL's email
    admin_email = ''
    email_title = "The user " + name + " want recommendations"
    email_body = "Email is {email}, postcode is {code} \n " \
                 "The max price is {max_price}, the min price is {min_price} \n" \
                 "The max length is {max_length}, the min length is {min_length} \n" \
                 "The max width is {max_width}, the min width is {min_width} \n" \
                 "The max height is {max_height}, the min height is {min_height} \n" \
                 "The additional notes is {notes} \n".format(
        email=email, code=postcode, max_price=max_price, min_price=min_price,
        max_length=max_length, min_length=min_length, max_width=max_width, min_width=min_width,
        max_height=max_height, min_height=min_height, notes=additionalnotes)
    send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [admin_email])

    return send_status
