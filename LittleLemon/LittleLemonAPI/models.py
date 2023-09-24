from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)

class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1, db_constraint=False)
    def __str__(self):
        return str(self.title)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE, default=1, db_constraint=False)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self):
        return str(self.user)

    class Meta:
        unique_together = ('menuitem', 'user')


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='delivery_crew', null=True)
    status = models.BooleanField(db_index=True, default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(db_index=True, auto_now_add=True)
    def __str__(self):
        return str(self.user)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=1, db_constraint=False)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE, default=1, db_constraint=False)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self):
        return str(self.order)

    class Meta:
        unique_together = ('order', 'menuitem')
