from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.shortcuts import redirect
from django.http import JsonResponse
from urllib.parse import urlparse, parse_qs
import json
from django.shortcuts import render, redirect
from .models import *
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import unquote
from rest_framework.views import APIView
# from myproject.serializer import YourModelSerializer
from .tests import *
from rest_framework.response import Response
from django.http import HttpResponseRedirect,HttpResponse

# Create your views here.
def home(request):
    substring = "one7000"
    product_container = Products_collection.find({"vendor": {"$regex": substring}})
    # return redirect('https://50d5-2409-4063-431d-be37-1076-17ae-7ae-7dc.ngrok-free.app')
    WriteIntoLog("Success","views.py","get_access_token","req retur")
    return render(request,'productlisting.html',{'product':product_container})
    return render(request,'home.html')
def oauth_shopify(req):
    shop = req.GET['shop']
    hmac = req.GET['hmac']
    print([shop,hmac])
    # scopes =  "write_inventory,write_locations,read_locations,write_merchant_managed_fulfillment_orders,read_orders,write_products,read_products,write_resource_feedbacks,read_resource_feedbacks"
    # url = "https://"+shop+"/admin/oauth/authorize?client_id=3c1c07b2bb5602cfd617bce29c628736&scope="+ scopes +"&redirect_uri=http://127.0.0.1:8000/connector/commense_auth/&state=1245"
    scopes = "write_inventory,write_locations,read_locations,write_merchant_managed_fulfillment_orders,read_orders,write_products,read_products,write_resource_feedbacks,read_resource_feedbacks"
    url = "https://" + shop + "/admin/oauth/authorize?client_id=79e8161414367fe343cadedc0d9c1013&scope=" + scopes + "&redirect_uri=https://eccom.bytelinkup.com/connector/commense_auth/&state=1245"

    response = redirect(url)
    return response
def connectorloginview(req):
    saved = str(req)
    savedata = facebookresponce.objects.create(data=saved,typee="direct")
    return HttpResponse(req)
class YourAPIView(APIView):
    def get(self, request):
        queryset = Products.objects.all()
        serializer = YourModelSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = YourModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

             
def required_data_app_shop(data, shop):
    try:
        check_for_available = app_shop_collection.find({"shop_name": shop})

        if app_shop_collection.count_documents({"shop_name": shop}) > 0:
            app_shop_collection.update_one(
                {"shop_name": shop},
                {"$set": {"shop_name": shop, "access_token": data['access_token']}}
            )
            WriteIntoLog('Updated', 'views.py', 'required_data_app_shop', f'{shop} updated => app_shop')
        else:
            app_shop_collection.insert_one({"shop_name": shop, "access_token": data['access_token']})
            WriteIntoLog('Success', 'views.py', 'required_data_app_shop', f'{shop} inserted into => app_shop')

        return True

    except Exception as e:
        WriteIntoLog('Error', 'views.py', 'required_data_app_shop', f'Error: {e}')
        # You might want to log the specific exception or handle it differently based on your requirements
        return False


def entry_user_details(shop_name,access_token):
    data = get_current_user(shop_name,access_token)

    try:
        if data is None:
            WriteIntoLog("ERROR", "views", "entry_user_details", shop_name + " current user not get ")
            raise ValueError("Error: Current user data is None.")

        entrydata = {}
        for k, v in data.items():
            entrydata[k] = v

        # user = user_details.objects.create(user_id=data['user']['id'], shop_name=shop_name, marketplace={0: {data}, 1: {}})
        user = user_details_collection.insert_many([entrydata])
        WriteIntoLog("SUCCESS", "views", "entry_user_details", "User details entry for " + shop_name + " completed")
        return True

    except Exception as e:
        WriteIntoLog("ERROR", "views", "entry_user_details", f"Error inserting user details: {e}")
        # Handle the error in a way that makes sense for your application
        # For example, you might want to log the error, send a notification, etc.
        return False
@csrf_exempt
def getwebhook(req):
    print(req)
    name_webhook = req.GET['webhook']
    # store  = req.GET['store']
    print(name_webhook)
    if req.method == 'POST':
        print("method is post")
        # request_body = req.body
        data = req.POST.dict()
        print(data)
        # respo.insert_one({"1":"aya to tha"})
        # respo.insert_one({"2":req})
        # respo.insert_one({"body":request_body})
        # Process the request_body as needed
        return JsonResponse({"message": "Request body received"})
    return True



def get_current_user(shop_name,access_token):
    try:
        url = 'https://{}/admin/api/2023-01/users/current.json'.format(shop_name)
        header = {
            'Content-Type': 'application/json',
            'X-Shopify-Access-Token': access_token
        }

        # Make the HTTP request
        r = requests.get(url=url, headers=header)
        r.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # Parse the JSON response
        data = r.json()
        WriteIntoLog("SUCCESS","views","get_current_user",shop_name+" "+"get the user")

        return data

    except requests.RequestException as e:
  
        
        WriteIntoLog("ERROR","views","get_current_user",shop_name+" "+"{e}")
        return None  # Or handle the error in a way that makes sense for your application

    except ValueError as e:
        return None 


def get_access_token(req):
    try:
        code = req.GET['code']
        WriteIntoLog('SUCCESS','views.py connector',"get_access_token",str(req))
        shop = req.GET['shop']
        url = 'https://'+shop+'/admin/oauth/access_token?client_id=79e8161414367fe343cadedc0d9c1013&client_secret=8d70580b9c8847884bfa9b86c4d6dab5&code='+code
        r = requests.post(url = url)
        data = r.json()
        get_shop = checkInstallation(shop,data['access_token'])
        if(get_shop):
            # something to do but for now posponing
            pass
            # checkEntry = entry_user_details(shop,data['access_token'])
            # if checkEntry:
            #     WriteIntoLog("Success","views","get_access_token",shop+" "+"User detail entry completed")
            #     # return False
        shop2 = str(shop)
        substring = shop2.split('.')[0]
        app_shop = required_data_app_shop(data,shop)
        webhook = create_webhook(shop,data['access_token'])
        if Products_collection.count_documents({"vendor": substring}) > 0:
            pass
        else:
            dataa = get_bulk_product_from_shopify(shop,data['access_token'])
            if dataa["success"]:
                entry_product = entry_product_container(dataa)
            else:
                dataa = get_bulk_product_from_shopify(shop,data['access_token'])
                entry_product = entry_product_container(dataa)

        shop2 = str(shop)
        substring = shop2.split('.')[0]
        product_container = Products_collection.find({"vendor": {"$regex": substring}})
        # return redirect('https://50d5-2409-4063-431d-be37-1076-17ae-7ae-7dc.ngrok-free.app')
        WriteIntoLog("Success","views.py","get_access_token","req retur")
        return render(req,'productlisting.html',{'product':product_container})
    except Exception as e:
    # Code to execute if any other exception occurs
        return HttpResponse(f"An error occurred: {e}")
    # finally:
    #     # Code to execute regardless of whether an exception occurs or not
    #     return HttpResponse("This will always execute. {e}")

def logcreation(request):
    WriteIntoLog("SuCCESS","views.py","logcreation","activated")
    return HttpResponse("hhhh")
def checkInstallation(shop_name,access_token):

    try:
        shop = user_details_collection.find({"shop_name": shop_name})
        # Check if there are any documents in the cursor
        if user_details_collection.count_documents({"shop_name": shop_name}) > 0:
            return True
        else:
            # Call the entry_user_details function if there are no documents

            checkEntry = entry_user_details(shop_name, access_token)
            if checkEntry:
                WriteIntoLog("Success","views","checkInstallation",shop_name+" "+"User detail entry completed")
                return False
            else:
                return False

    except Exception as e:
        # Handle the exception in a way that makes sense for your application
        # For example, log the error or send a notification
        WriteIntoLog("ERROR","views","checkInstallation",shop_name+" "+"{e}")

        return False

    # return shop

def entry_product_container(data):
    val = data['data']['products']
    products_to_insert = []  # Create an empty list to store the products

    for i in val:
        optn = {}  # Move the creation of optn inside the loop
        for k, j in i.items():
            optn[k] = j

        products_to_insert.append(optn)  # Append the product to the list

    if products_to_insert:
        Products_collection.insert_many(products_to_insert)


def get_bulk_product_from_shopify(shop,access_token):
    url2 = 'https://'+shop+'/admin/api/2023-07/products.json'
    headers = {
        'X-Shopify-Access-Token': access_token
    }

    response = requests.get(url2, headers=headers)
    WriteIntoLog("INFO","view connector","get_bulk_product_from_shopify",str(response))
    if response.status_code == 200:
        data = response.json()
        WriteIntoLog("INFO","view connector","get_bulk_product_from_shopify json",str(data))

        # Process the response data
        response = {
                "success": True,
                "data": data
        }
    else:
        response = {
                "success": False,
                "message": "please re import product"
        }
    return response

def create_webhook(store,access_token):
    try:
        url = "https://" + store + "/admin/api/2023-07/webhooks.json"
        # getweebhookdb = webhook_collection.find({"shop_name": store})
        print("webhook")
        if webhook_collection.count_documents({"shop_name": store}) > 0:
            WriteIntoLog('Success','views.py','create_webhook',store+" "+"webhook already exist")
            return True
        webhook = ["locations/create", "locations/update", "locations/delete","order_transactions/create","orders/create"]
        headers = {
            'X-Shopify-Access-Token': access_token,
            'Content-Type': 'application/json'
        }

        for topic in webhook:
            value = topic.replace('/', '_')
            data = {
                "webhook": {
                    "address": "https://eccom.bytelinkup.com/connector/webhook?webhook=" + value + "&store=" + store,
                    "topic": topic,
                    "format": "json"
                }
            }
            

            response = requests.post(url, json=data, headers=headers)
          
            WriteIntoLog('Success','views.py','create_webhook',store+" "+"created =>" + topic)
           
        print(response.status_code )
        print("res")
        print(response.status_code) 
        if response:
            webhook_collection.insert_one({'shop_name':store,"webook":"Register Succesfully"})
            return JsonResponse({"success": True, "message": "Webhook created successfully"})

        else:
            WriteIntoLog('Error','views.py','create_webhook',store+" "+" =>" + response.status_code)

            return JsonResponse({"success": False, "message": "Failed to create webhook"}, status=response.status_code)

    except requests.RequestException as e:
        # Handle the exception in a way that makes sense for your application
        return JsonResponse({"success": False, "message": "Failed to create webhook"}, status=500)
    except Exception as e:
        # Handle other exceptions
        return JsonResponse({"success": False, "message": "An unexpected error occurred"}, status=500)



def base_url(req):
    request_data = {
        "method": req.method,
        "path": req.path,
        "GET_params": req.GET.dict(),
        "POST_params": req.POST.dict(),
        "headers": dict(req.headers),
        "remote_addr": req.META.get('REMOTE_ADDR'),
        "user_agent": req.META.get('HTTP_USER_AGENT')
    }
    base = auth_token.insert_one(request_data)
    return HttpResponse(req)
def base2_url(req):
    request_data = {
        "method": req.method,
        "path": req.path,
        "GET_params": req.GET.dict(),
        "POST_params": req.POST.dict(),
        "headers": dict(req.headers),
        "remote_addr": req.META.get('REMOTE_ADDR'),
        "user_agent": req.META.get('HTTP_USER_AGENT')
    }
    base = auth_token.insert_one(request_data)
    return HttpResponse(req)