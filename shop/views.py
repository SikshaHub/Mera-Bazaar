from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from payTm import Checksum
from .models import Product, Contact, Order, OrderStatus
from math import ceil
import json
# MERCHANT_ID = "SDIaeg73517065027042"
# MERCHANT_KEY = "yZz9yWGhPb7_0Ck@"
MERCHANT_ID = "QHHczy75217157650137"
MERCHANT_KEY = "NSSpcw6Gi!9rxLt%"

# Create your views here.
def index(request):
    template = 'shop/index.html'
    allProducts = []
    prod_catg = Product.objects.values('category','id')
    categories = {item['category'] for item in prod_catg}
    for category in categories:
        products = Product.objects.filter(category= category)
        n = len(products)
        no_of_slides = n//4 + ceil((n/4)-(n//4))
        allProducts.append([products, range(1,no_of_slides),no_of_slides])

    context = {
        'allProds': allProducts,
    }
    return render(request,template,context)

def searchMatch(query, item):
    # Return True only if query matches the item
    query = query.lower()
    if (query in item.desc.lower()) or (query in item.product_name.lower()) or (query in item.category.lower()):
        return True
    else:
        return False

def search(request):
    template = 'shop/search.html'
    query = request.GET.get('search')
    allProducts = []
    message = ""
    prod_catg = Product.objects.values('category','id')
    categories = {item['category'] for item in prod_catg}
    for category in categories:
        prodtemp = Product.objects.filter(category= category)
        products = [item for item in prodtemp if searchMatch(query, item)]
        n = len(products)
        if n!= 0:
            no_of_slides = n//4 + ceil((n/4)-(n//4))
            allProducts.append([products, range(1,no_of_slides),no_of_slides])

    if len(allProducts) == 0:
        message = "Please make sure to enter relevent search query."

    context = {
        'allProds': allProducts,
        'message': message,
    }

    return render(request,template,context)

def about(request):
    template = 'shop/about.html'
    return render(request,template)

def contact(request):
    template = 'shop/contact.html'
    if request.method=="POST":
        name = request.POST.get('full_name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone_no','')
        query = request.POST.get('query','')
        contact = Contact(full_name=name, email=email, phone_no=phone, query=query, created_by="vin.nasik")
        contact.save()
    return render(request,template)

def tracker(request):
    template = 'shop/tracker.html'
    if request.method=="POST":
        order_id = request.POST.get('orderId','')
        email_id = request.POST.get('emailId','')
        try:
            order = Order.objects.filter(order_id=order_id, email=email_id)
            if order:
                status = OrderStatus.objects.filter(order_id=order_id)
                status_list = []
                for item in status:
                    status_list.append({'status':item.description, 'time':item.creation_time})
                    
                response = json.dumps({"status": "Success", "updates": status_list, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status": "Failed"}')
        except:
            return HttpResponse('{"status": "Error"}')
    return render(request,template)

def products(request):
    template = 'shop/product.html'
    return render(request,template)

def product(request, prid):
    template = 'shop/product.html'
    product = Product.objects.filter(id=prid)
    print(product)
    context = {
        'product': product[0],
    }
    return render(request,template,context)

def checkout(request):
    template = 'shop/checkout.html'
    orderPlaced = False
    orderId = -1
    if request.method=="POST":
        itemsJson = request.POST.get('itemsJson','')
        total_amount = request.POST.get('totalAmount','')
        full_name = request.POST.get('full_name','')
        email_id = request.POST.get('email_id','')
        address1 = request.POST.get('address1','')
        address2 = request.POST.get('address2','')
        address3 = request.POST.get('address3','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_zode = request.POST.get('zip_zode','')
        pri_mob = request.POST.get('pri_mob','')
        sec_mob = request.POST.get('sec_mob','')
        order = Order(items_json=itemsJson, total_amount=total_amount, full_name=full_name, email=email_id, address_line1=address1, 
                    address_line2=address2, address_line3=address3, city=city,state=state,pin_zode=zip_zode,primary_mobile_no=pri_mob,
                    secondary_mobile_no=sec_mob,created_by="vin.nasik")
        order.save()
        orderId = order.order_id
        orderPlaced = True

        status = OrderStatus(order_id=orderId, description="The order has been placed.", created_by="vin.nasik")
        status.save()

        # Request PayTM to transfer the amount to your account after payment done by User
        payment_dict = {
            "MID": MERCHANT_ID,
            "ORDER_ID": str(orderId),
            "CUST_ID": order.email,
            "TXN_AMOUNT": str(order.total_amount),
            "CHANNEL_ID": "WEB",
            "INDUSTRY_TYPE_ID": "Retail",
            "WEBSITE": "WEBSTAGING",
            "CALLBACK_URL": 'http://127.0.0.1:8000/shop/handle-request/',
        }
        payment_dict["CHECKSUMHASH"] =  Checksum.generate_checksum(payment_dict, MERCHANT_KEY)

        return render(request, 'shop/payment_handle.html', {'payment_dict': payment_dict})

    context = {
        'order_placed': orderPlaced,
        'order_id': orderId,
    }
    return render(request,template,context)

@csrf_exempt
def handlePaytmRequest(request):
    # PayTM will send Post Request here after receiving payment request
    template = 'shop/payment_status.html'
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == "CHECKSUMHASH":
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print("Order Successful")
        else:
            print("Order unsuccessful because" + response_dict['RESPMSG'])
    else: 
	    print("Order unsuccessful because" + response_dict['RESPMSG'])

    context = {
        'response': response_dict,
    }

    return render(request, template, context)
