from django.core.mail import send_mail
import random
import string


def sendVerificationMail(targetEmailAddress, password):
    subject = "پسورد اکانت کاربری شما در سایت هاسپیتال‌من"
    messageBody = "ثبت‌نام شما در سایت هاسپیتال‌من توسط مدیر تایید شد \nکلمه عبور اکانت شما برابر است با: " + str(password)

    send_mail(subject, messageBody, 'hospitalman.DB@gmail.com', [targetEmailAddress, ])


def createRandomPassword():
    N = 8
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
