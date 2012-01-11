from datetime import date
from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    image_link = models.CharField(max_length = 150, blank=True, null=True)
    author = models.CharField(max_length = 50)
    title = models.CharField(max_length = 250)
    barcode = models.CharField(max_length = 40, blank=True, null=True)
    loaned = models.BooleanField(default = False)
    loaned_to = models.ForeignKey(User, blank=True, null=True)
    
    def loan_book(self, user):
        if self.loaned == False:
            self.loaned_to = user
            self.loaned = True
            self.save()
            return True
        else:
            return False
    
    def return_book(self, user):
        if self.loaned_to == user:
            self.loaned = False
            self.loaned_to = None
            self.save()
            return True
        else:
            return False
    
    def __unicode__(self):
        return self.title

def create_book(post):
    book = Book(image_link = post['image_link'],
                author = post['author'],
                title = post['title'],
                barcode = post['barcode'])
    book.save()

