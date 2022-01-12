from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    bio = models.TextField


class Order(models.Model):
    user = models.ForeignKey('main.UserProfile', on_delete=models.CASCADE)
    cat = models.ForeignKey('cats.Cat', on_delete=models.CASCADE)

    def __str__(self):
        return f"Order: {self.id}, Cat: {self.cat}, rented by {self.user}"
