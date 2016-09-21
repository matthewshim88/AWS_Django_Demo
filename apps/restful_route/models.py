from __future__ import unicode_literals
from django.db import models

class ProductManager(models.Manager):
    def createProduct(self, data):
        response = {}
        errors = self.validateProduct(data)
        if len(errors) > 0:
            response['created']=False
            response['errors'] = errors
        else:
            new_product = Product.prodMgr.create(prod_name=data['name'], description = data['description'], price = data['price'])
            new_product.save()
            response['created'] = True
            response['new_product'] = new_product
        return response

    def updateProduct(self, id, data):
        response = {}
        errors = self.validateUpdate(data)
        if len(errors) > 0:
            response['updated'] = False
            response['errors'] = errors
        else:
            updated_prod = Product.prodMgr.get(id=id)
            updated_prod.prod_name = data['name']
            updated_prod.description = data['description']
            updated_prod.price = data['price']
            updated_prod.save()
            response['updated'] = True
            response['return_obj'] = updated_prod
        return response

    #helper method to validate Product
    def validateProduct(self,data):
        errors=[]
        #checks if product already exists in DB
        existing_product = self.filter(prod_name=data['name'])
        if existing_product:
            errors.append('Product already exists, Edit or create New')
        if len(data['name']) < 1:
            errors.append('Product Name Cannot be Empty')
        if len(data['price']) < 1:
            errors.append('Product must set a price')
        # if not data['price'].isnumeric():
        #     errors.append('Price can only be numeric')
        return errors

    #had to make a second validate, the first one checks if it
    #exists and doesn't allow update
    def validateUpdate(self, data):
        errors=[]
        if len(data['name']) < 1:
            errors.append('Product Name Cannot be Empty')
        if len(data['price']) < 1:
            errors.append('Product must set a price')
        return errors

# Create your models here.
class Product(models.Model):
    prod_name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    prodMgr = ProductManager()
