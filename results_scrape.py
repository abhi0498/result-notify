import requests
from bs4 import BeautifulSoup
import smtplib
from app import Mail
import time


def send_mail(sem):
    students = list(Mail.query.filter_by(sem=sem))
    student_mail = [student.email for student in students]
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login("randyabhi65@gmail.com", "ksmnsffgwxictrqj")

    subject = "Results are out"
    body = "Check your results here: https://results.vtu.ac.in/"
    msg = f"Subject:{subject}\n\n {body}"
    for student in student_mail:
        server.sendmail(
            "randyabhi65@gmail.com",
            student,
            msg
        )
    server.close()


def check():
    data = requests.get("https://results.vtu.ac.in/", verify=False)

    page = BeautifulSoup(data.content, 'html.parser')

    classes = page.findAll(lambda tag: tag.name ==
                           'div' and tag['class'] == ['panel-heading'])

    recent_result = classes[0].get_text()

    for i in range(1, 9):

        if "B.E" in recent_result and str(i) in recent_result:
            send_mail(i)


while(True):
    check()
    time.sleep(60*60*60)
