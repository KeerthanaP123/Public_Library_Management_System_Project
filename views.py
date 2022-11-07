from django.shortcuts import render,redirect
from django.contrib.auth.models import auth , models
from django.http import HttpResponse
from home.models import Account,Book
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User,auth,models
from . models import User
from django.views.decorators.cache import cache_control
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from home.forms import BookForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout, authenticate
#
# # Create your views here.
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
def user(request):
    return render(request,"user.html")
def librarian(request):
    return render(request,"librarian.html")

def reg(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        contact=request.POST['contact']
        address=request.POST['address']
        city=request.POST['city']
        state=request.POST['state']
        pincode=request.POST['pincode']
        dob=request.POST['dob']
        roles=request.POST['roles']
        password=request.POST['password']
        is_customer=is_librarian=False
        if roles=='is_customer':
            is_customer=True
        else:
            is_librarian=True
        if Account.objects.filter(email=email).exists():
            messages.info(request,'Email already Exists')
            return redirect('reg')
        user=Account.objects.create_user(fname=fname,lname=lname,email=email,contact=contact,address=address,city=city,state=state,pincode=pincode,dob=dob,is_customer=is_customer,is_librarian=is_librarian,password=password)
        # user.is_customer=True
        user.save()
        messages.success(request,'Thankyou for registering with us Please Login')
        current_site = get_current_site(request)
        message = render_to_string('Account_verification.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        send_mail(
            'Please activate your account',
            message,
            'ajcelibrary2023b@gmail.com',
            [email],
            fail_silently=False,
        )


        return redirect('/login/?command=verification&email=' + email)

#     return redirect('/login')
    return render(request,'reg.html')

def login(request):
    if request.method =='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        print(email,password)
        user=auth.authenticate(email=email,password=password)
        print(user)
        if user is not None:
            auth.login(request,user)
            request.session['email']=email
            if user.is_admin:
                return redirect('/admin')
            elif user.is_customer:
                return redirect('/user')
            elif user.is_librarian:
                return redirect('/librarian')
            # elif user.is_librarian:
            #     return redirect('user/')
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('login')
    return render(request,'login.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)

    return redirect('/')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email

            current_site = get_current_site(request)
            message = render_to_string('ResetPassword_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            send_mail(
                'Please activate your account',
                message,
                'ajcelibrary2023b@gmail.com',
                [email],
                fail_silently=False,
            )

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'Forgot_Password.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'ResetPassword.html')
def changepassword(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(email__exact=request.user.email)
        success = user.check_password(current_password)
        if success:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password updated successfully.')
            return redirect('login')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('changepassword')
    return render(request, 'changepassword.html')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('http://127.0.0.1:8000/login/')
    else:
        messages.error(request, 'In-valid activation link')
        return redirect('reg')






def display(request):
    return render(request,'display.html',{
        'books':Book.objects.all()
    })
def bookdisplay(request):
        obj = Book.objects.all
        return render(request,'bookdisplay.html',{'result':obj})
        # 'books':Book.objects.all()
def view(request,bk_id):
    book=Book.objects.get(pk=bk_id)
    return HttpResponseRedirect(reverse('display'))
def add(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            bk_title = form.cleaned_data['bk_title']
            bk_author = form.cleaned_data['bk_author']
            bk_publisher = form.cleaned_data['bk_publisher']
            bk_pubyear = form.cleaned_data['bk_pubyear']
            bk_pubagency = form.cleaned_data['bk_pubagency']
            bk_edition = form.cleaned_data['bk_edition']
            bk_isbn = form.cleaned_data['bk_isbn']
            bk_noofpages = form.cleaned_data['bk_noofpages']
            bk_price = form.cleaned_data['bk_price']
            bk_stno = form.cleaned_data['bk_stno']
            b = Book(bk_title=bk_title,
                    bk_author=bk_author,
                    bk_publisher=bk_publisher,
                    bk_pubyear=bk_pubyear,
                    bk_pubagency=bk_pubagency,
                    bk_edition=bk_edition,
                    bk_isbn=bk_isbn,
                    bk_noofpages=bk_noofpages,
                    bk_price=bk_price,
                    bk_stno=bk_stno
                     )
            b.save()
            return render(request,'add.html',{
                'form': BookForm(),
                'success': True
            })
    else:
        form = BookForm()
    return render(request,'add.html', {
        'form': BookForm()
    })



def edit(request, bk_id):
  if request.method == 'POST':
    book = Book.objects.get(pk=bk_id)
    form = BookForm(request.POST, instance=book)
    if form.is_valid():
      form.save()
      return render(request, 'edit.html', {
        'form': form,
        'success': True
      })
  else:
    book= Book.objects.get(pk=bk_id)
    form = BookForm(instance=book)
  return render(request, 'edit.html', {
    'form': form
  })

def delete(request,bk_id):
  if request.method == 'POST':
   book = Book.objects.get(pk=bk_id)
   book.delete()
  return HttpResponseRedirect(reverse('display'))
