from django.shortcuts import render,redirect
from django.template import loader
from myapp.models import *
from django.contrib import auth
from django.contrib.auth import authenticate,login
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.core.mail import send_mail
import random
from myapp.models import Book

from django.urls import reverse
from datetime import datetime
from django.contrib import messages
def index(request):
        return render(request,'index.html')
def login(request):
        return render(request,'login.html')
def register(request):
        return render(request,'register.html')
def about(request):
        return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')
def detail(request):
    return render(request,'detail.html')

#-------------------------------------------------------------

#----------------------
from django.contrib.auth.decorators import login_required

@login_required
def cancel(request):
    # Retrieve bookings only for the logged-in user
    user_bookings = Book.objects.filter(user=request.user)
    
    if request.method == 'POST':
        pnr_to_cancel = request.POST.get('id')
        try:
            booking_to_cancel = user_bookings.get(pk=pnr_to_cancel)
            # Process cancellation logic here, e.g., refund, cancellation confirmation, etc.
            booking_to_cancel.delete()  # Deleting the booking for simplicity in this example
            messages.success(request, f'Ticket with PNR {pnr_to_cancel} has been canceled.')
        except Book.DoesNotExist:
            messages.error(request, f'Booking with PNR {pnr_to_cancel} does not exist or you are not authorized to cancel it.')
        return redirect('myapp:cancel')

    context = {'bookings': user_bookings}
    return render(request, 'Cancel_ticket.html', context)

def search(request):
    all_from_stations = Station.objects.values_list('From_Station', flat=True).distinct()
    all_destinations = Station.objects.values_list('Destination', flat=True).distinct()
    stations = None  # Default value when the request method is not POST
    
    if request.method == 'POST':
        from_station = request.POST.get('from')
        to_station = request.POST.get('to')

        stations = Station.objects.filter(
            From_Station__icontains=from_station,
            Destination__icontains=to_station
        )

    stationss = Station.objects.all()
    return render(request, 'search_train.html', {'stations': stations,'stationss': stationss,'all_from_stations': all_from_stations, 'all_destinations': all_destinations})


def fsearch(request):
    return render(request,'first_search.html')
from myapp.models import Book

def pnr(request):
    train_number = request.POST.get('train_number')
    booking_details = None
    train_details = None

    if request.method == 'POST':
        try:
            
            booking_details = Book.objects.filter(Train_Number=train_number, user=request.user)
            booking_details = booking_details.order_by('-DepartureDate').first()

            try:
                train_details = Station.objects.get(Train_Number=train_number)
            except Station.DoesNotExist:
                messages.error(request, f'Train with number {train_number} does not exist.')
        except Book.DoesNotExist:
            messages.error(request, f'You have not booked the train with number {train_number}.')

    return render(request, 'pnr_status.html', {'booking_details': booking_details, 'train_details': train_details})# def book(request):

from django.contrib.auth.decorators import login_required

@login_required
def book(request):
    train_info = Station.objects.values_list('From_Station', 'Destination', 'Train_Number', 'Train_Name').distinct()

    if request.method == 'POST':
        user = request.user  # Get the currently logged-in user
        From = request.POST.get('From')
        To = request.POST.get('To')
        Phonenumber = request.POST.get('Phonenumber')
        Email = request.POST.get('Email')
        DepartureDate_str = request.POST.get('DepartureDate')
        Noofseats = request.POST.get('No.ofseats')
        Quotas = request.POST.get('Quotas')
        Train_Number = request.POST.get('Train_Number')  # Get the selected train number from the dropdown

        # Check if the user has already booked the selected train
        existing_booking = Book.objects.filter(user=user, Train_Number=Train_Number).first()
        if existing_booking:
            messages.error(request, 'You have already booked this train.')
            return render(request, 'book.html', {'train_info': train_info})

        if DepartureDate_str:
            try:
                DepartureDate = datetime.strptime(DepartureDate_str, '%Y-%m-%d').date()
            except ValueError:
                return HttpResponse("Invalid date format")

            book_instance = Book(
                user=user,
                From=From,
                To=To,
                Phonenumber=Phonenumber,
                Email=Email,
                DepartureDate=DepartureDate,
                Noofseats=Noofseats,
                Quotas=Quotas,
                Train_Number=Train_Number,  # Save the selected train number
            
            )

            book_instance.save()
            messages.success(request, 'Your ticket is successfully booked!')
            return render(request, 'book.html', {'train_info': train_info})  

    return render(request, 'book.html', {'train_info': train_info})



def send_otp(email, otp):
    subject = 'OTP Verification'
    message = f'Your OTP for registration is: {otp}'
    send_mail(subject, message, None, [email])


from django.http import HttpResponseRedirect

# ...

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('myapp:register')

        otp_number = random.randint(1000, 9999)
        otp = str(otp_number)

        send_otp(email, otp)
        request.session['username'] = username
        request.session['email'] = email
        request.session['password'] = password
        request.session['otp'] = otp  # Add this line to store OTP in the session

        #Construct the URL using HttpResponseRedirect
        #return HttpResponseRedirect(f'/otp/{otp}/{username}/{password}/{email}/')
        # Alternatively, you can use reverse:
        return HttpResponseRedirect(reverse('myapp:otp', args=[otp, username, password, email]))

    else:
        return render(request, 'register.html')


def otp(request, otp, username, password, email):
    if request.method == "POST":
        uotp = request.POST['otp']
        otp_from_session = request.session.get('otp')

        if uotp == otp_from_session:
            username = request.session.get('username')
            email = request.session.get('email')
            password = request.session.get('password')

            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return redirect('myapp:login')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('myapp:otp', otp=otp, username=username, password=password, email=email)

    return render(request, 'otp.html',{'otp': otp, 'username': username, 'password': password, 'email': email})



def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('myapp:detail')
        else:
            messages.info(request,'Invalid user credentials')
            return redirect('myapp:login')
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout (request)
    return redirect('/')


def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        msg=request.POST['msg']
        contact=Contact(name=name,email=email,msg=msg)
        contact.save()
        messages.success(request,'Your message has been sent successfully')
        return redirect('myapp:contact')
        
    else:
         return render(request,'Contact.html')





