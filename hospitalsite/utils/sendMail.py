from django.core.mail import send_mail
from hospitalsite import models

subject = "hospitalman password"
messageBody = "Your password is 12345678"
targetEmailAddress = "mreza.azizi74@gmail.com"

send_mail(subject, messageBody, 'hospitalman.DB@gmail.com', [targetEmailAddress,])
