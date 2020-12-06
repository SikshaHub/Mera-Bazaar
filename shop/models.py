from django.db import models

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default='-')
    subcategory = models.CharField(max_length=50, default='-')
    price = models.FloatField(default=0.00)
    desc = models.CharField(max_length=300)
    image = models.FileField(upload_to='product/category/', null=True, blank=True)
    pub_date = models.DateField()
    created_by = models.CharField(max_length=50, null=True, blank=True)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True,null=True)

    def __str__(self):
        return self.product_name + ' - ' +  self.desc

class Contact(models.Model):
    query_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100, default='')
    phone_no = models.CharField(max_length=30, default='')
    query = models.CharField(max_length=300, default='')
    created_by = models.CharField(max_length=50, null=True, blank=True)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True,null=True)

    def __str__(self):
        return self.full_name + ' - ' +  self.query

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    total_amount = models.FloatField(default=0.00)
    full_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100, default='')
    address_line1 = models.CharField(max_length=150)
    address_line2 = models.CharField(max_length=150)
    address_line3 = models.CharField(max_length=100,blank=True,null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pin_zode = models.CharField(max_length=10)
    primary_mobile_no = models.CharField(max_length=15)
    secondary_mobile_no = models.CharField(max_length=15,blank=True,null=True)
    estimated_delivery_time = models.DateTimeField(blank=True,null=True)
    order_completed = models.BooleanField(default=False)
    created_by = models.CharField(max_length=50, null=True, blank=True)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True,null=True)

    def __str__(self):
        return str(self.order_id) + ' - ' +  self.items_json

class OrderStatus(models.Model):
    order_id = models.IntegerField()
    location = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=500, default='')
    created_by = models.CharField(max_length=50, null=True, blank=True)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        if len(self.description)>60:
            return self.description[0:60] + "..."
        else:
            return self.description



