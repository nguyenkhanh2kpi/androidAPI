from django.db import models
from django.contrib.auth.models import User

class DivineCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'DivineCategory'
        verbose_name_plural = 'DivineCategories'
    def __str__(self):
        return self.name

class DivineSoftware(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image_url = models.URLField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    category = models.ForeignKey(DivineCategory, on_delete=models.SET_NULL, null=True)
    has_key = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class DivineKey(models.Model):
    key_code = models.CharField(max_length=20)
    software = models.ForeignKey(DivineSoftware, on_delete=models.CASCADE)
    is_used = models.BooleanField()

    def __str__(self):
        return self.key_code

class DivineOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return str(self.id)

class DivineOrderDetail(models.Model):
    order = models.ForeignKey(DivineOrder, on_delete=models.CASCADE)
    key = models.ForeignKey(DivineKey, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)

class DivineComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    software = models.ForeignKey(DivineSoftware, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.software.name}"


class DivineCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class DivineCartItem(models.Model):
    cart = models.ForeignKey(DivineCart, on_delete=models.CASCADE)
    software = models.ForeignKey(DivineSoftware, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)


