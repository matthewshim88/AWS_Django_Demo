from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import Product, ProductManager

# Create your views here.
def index(request):
    all_products = Product.prodMgr.all()
    context = {
        'all_products' : all_products
    }
    return render(request, 'restful_route/index.html', context)

def new(request):
    return render(request, 'restful_route/newProduct.html')

def create(request):
    if request.method == 'POST':
        result = Product.prodMgr.createProduct(request.POST)
        #result is 'response' in models, becomes result when it's passed back
        if result['created']:
            new_product = result['new_product']
            messages.success(request, new_product.prod_name + ' was Successfully Added to Products')
        else:
            for error in result['errors']:
                messages.error(request, error)
    return redirect('/')

def show(request, id):
    result = Product.prodMgr.get(id=id)
    context = {
        'this_product': result
    }
    return render(request, 'restful_route/show.html', context)

def edit(request, id):
    result = Product.prodMgr.get(id=id)
    context = {
        'this_product': result
    }
    return render(request, 'restful_route/edit.html', context)

def update(request, id):
    if request.method == 'POST':
        update = Product.prodMgr.updateProduct(id, request.POST)
        if update['updated']:
            messages.success(request, update['return_obj'].prod_name + ' Successfully Updated')
        else:
            for error in update['errors']:
                messages.error(request, error)

    return redirect('/edit/{}'.format(id))

def delete(request, id):
    Product.prodMgr.get(id=id).delete()
    return redirect('/')
