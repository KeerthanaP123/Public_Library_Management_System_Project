from http.client import HTTPResponse
from django.shortcuts import render,redirect
from django.template import loader
from home.models import register,Login

# Create your views here.
def home(request):
    return render(request,"index.html")
def about(request):
    return render(request,"about.html")
def base(request):
    return render(request,"base.html")
def contact(request):
    return render(request,"contact.html")
def service(request):
    return render(request,"services.html")
def rules(request):
    return render(request,"rules.html")

def reg(request):
    
    if request.method=="POST":
        
        #fname=request.POST.get("fname")
        #lname=request.POST.get("lname")
        #email=request.POST.get("email")
        #contact=request.POST.get("contact")
        #address=request.POST.get("address")
        #state=request.POST.get("state")
        #pincode=request.POST.get("pincode")
        #password=request.POST("password")
        #confirmpassword=request.POST.get("confirmpassword")
        #r=register()
        #r.fname=fname
        #r.lname=lname
        #r.email=email
        #r.contact=contact
        #r.address=address
        #r.state=state
        #r.pincode=pincode
        #r.password=password
        #r.confirmpassword=confirmpassword
        #r.status='pending'
        #r.save()
        return render(request,"login.html")
    else:
        return render(request,"re.html")
   

def login(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        if(login.objects.filter(email=email,password=password)):
          return render(request,"user.html")
       
    
