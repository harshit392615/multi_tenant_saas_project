from .models import Organization , Membership , Subscription
from common.exceptions import PermissionDenied ,ValidationError 
from accounts.models import User
import hashlib
import uuid
from django.conf import settings

def Create_Org(*,user,name,type):
    organization = Organization.objects.create(
        name = name,
        type = type,
    )
    membership = Membership.objects.create(
        user = user,
        organization = organization,
        role = 'owner',
    )

    return organization

def Update_Org(*,slug,actor,name):
    if actor.role != "owner":
        raise PermissionDenied("you are not allowed to perform this action")
    try:
        organization = Organization.objects.get(
            slug = slug
        )
    except Organization.DoesNotExist:
        raise ValidationError("invalid organization id")
    
    organization.name = name

    organization.save(update_fields=['name'])

    return organization

def Delete_Org(*,id,actor):
    if actor.role != 'owner':
        raise PermissionDenied("you are not allowed to perform this action")
    
    try:
        organization = Organization.objects.get(
            id = id
        )
    except Organization.DoesNotExist:
        raise ValidationError("invalid organization id")
    
    organization.is_deleted =  True

    organization.save(update_fields=['is_deleted'])

def Archive_Org(*,slug,actor):
    if actor.role not in ['owner','admin']:
        raise PermissionDenied("You cannot archive a workspace")
    try:
        organization = Organization.objects.get(
            slug = slug
        )
    except Organization.DoesNotExist:
        raise ValidationError("invalid organization id")
    organization.is_archived = True
    organization.save(update_fields = ['is_archived'])

# fix this api asap 

def Add_Membership(actor , organization , serializer):
    if actor.role not in ['owner','admin']:
        raise PermissionError("you are not allowed to make this request")
    
    if serializer['role'] not in ['admin','member','viewer']:
        raise ValidationError("not a valid role")
    
    user = User.objects.get(
        email = serializer['email']
    )
    membership = Membership.objects.create(  
        organization = organization,
        user = user,
        role = serializer['role']
    )

    return membership

def Update_Membership(actor , organization , serializer):
    if actor.role not in ['owner','admin']:
        raise PermissionError("you are not allowed to make this request")
    
    if serializer['role'] not in ['admin','member','viewer']:
        raise ValidationError("not a valid role")
    
    user = User.objects.get(
        email = serializer['email']
    )
    membership = Membership.objects.get(  
        organization = organization,
        user = user,
    )
    if membership.role == "owner":
        raise PermissionDenied("you cannot change role of owner")
    membership.role = serializer['role']
    membership.save()

    return membership

def Add_Subscription(user , actor , organization , data):
    key = settings.PAYU_KEY
    salt = settings.PAYU_SALT
    print(data)
    if actor.role != "owner":
        raise PermissionError("you are not allowed to make this request")
    
    firstname = user.username
    
    if data['title'] not in ['basic','standard','premium']:
        raise ValidationError("invalid subscription")
    
    txnid = uuid.uuid4().hex[:25]
    
    subs = {
        "basic":{
            "price":500,
            "rate_limit":"10/hour",
            "duration":30
        },
        "standard":{
            "price":1000,
            "rate_limit":"15/hour",
            "duration":60
        },
        "premium":{
            "price":5000,
            "rate_limit":"20/hour",
            "duration":365
        }
    }

    hash_str = f"{key}|{txnid}|{subs[data['title']]['price']}|subscription|{firstname}|{data['email']}|||||||||||{salt}"

    
    hash = hashlib.sha512(hash_str.encode()).hexdigest()

    
    Subscription.objects.create(
        organization = organization,
        title = data['title'],
        price = subs[data['title']]['price'],
        rate_limit = subs[data['title']]['rate_limit'],
        duration = subs[data['title']]['duration'],
        txnid = txnid,
        is_active = False
    )
    
    context = {
            "payu_url": "https://test.payu.in/_payment",
            "key": settings.PAYU_KEY,
            "txnid": txnid,
            "amount": subs[data['title']]['price'],
            "productinfo": "subscription",
            "firstname": firstname,
            "email": data['email'],
            "phone": "9999999999",
            "surl": "http://10.164.97.174:8000/api/organization/subscription/verify/",
            "furl": "http://127.0.0.1:5500/multi_tenant_saas_project/frontend/html/login.html",
            "hash": hash,
        }
    return context
    
def Verify_Subscription(data):
    key = settings.PAYU_KEY
    salt = settings.PAYU_SALT
    subscription = Subscription.objects.get(txnid=data["txnid"])
    print(data)

    hash_str = (
        f"{salt}|{data['status']}||||||{data['udf5']}|{data['udf4']}|{data['udf3']}|{data['udf2']}|{data['udf1']}|{data['email']}|{data['firstname']}|{data['productinfo']}|{data['amount']}|{data['txnid']}|{data['key']}"
    )

    calculated_hash = hashlib.sha512(
        hash_str.encode("utf-8")
    ).hexdigest()

    print(data)

    if calculated_hash != data["hash"]:
        raise ValidationError("Invalid PayU hash")

    if data["status"] == "success":
        subscription.is_active = True
        subscription.save()
        