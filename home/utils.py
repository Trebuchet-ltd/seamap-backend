import threading
import time

from django.conf import settings
from django.core.mail import send_mail


class EmailThread(threading.Thread):
    def __init__(self, subject, content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.content = content
        threading.Thread.__init__(self)

    def run(self):
        send_mail(self.subject, self.content, settings.EMAIL_HOST_USER, self.recipient_list, fail_silently=False)
        print(f'Mail [{self.subject}] sent to {self.recipient_list}')


def send_async_mail(subject, content, recipient_list):
    print(content)
    EmailThread(subject, content, recipient_list).start()


class BulkEmail(threading.Thread):
    def __init__(self, objects):
        self.objects = objects
        threading.Thread.__init__(self)

    def run(self):
        count = 0
        for i in self.objects:
            print(i[1])
            thre = EmailThread(i[0], i[1], i[2])
            thre.start()
            thre.join()
            time.sleep(3)
            if count > 50:
                time.sleep(200)
                count = 0
            count += 1
            print(f'Mail to all')


def send_bulk_async_mail(objects):
    print(len(objects))
    BulkEmail(objects).start()
