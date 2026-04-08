from django.db import models

class Dish(models.Model):
    name = models.CharField(max_length=100)
    cook_time = models.IntegerField()
    prep_time = models.IntegerField()


class Account(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password