from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth 
from .models import FarmerData
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TimeSlot
import datetime, time
from django.utils import timezone


# Create your views here.
def login(request):
    if request.method == "POST":
        userName = request.POST['userName']
        password = request.POST['password']

        user = auth.authenticate(username=userName, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Invalid Credentials")
            return redirect('login')
 
    return render(request, 'farmers/login.html')

def signup(request):
    if request.method == "POST":
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        aadharNo = request.POST['aadharNo']
        password = request.POST['password']
        if User.objects.filter(username=aadharNo).exists():
            messages.info(request, "Aadhar Taken")
            return redirect('signup')

        else:
            user = User.objects.create_user(first_name=firstName, last_name=lastName ,username=aadharNo, password=password)
            user.save()
            return redirect('login')
        

    else:
        return render(request, 'farmers/signup.html')
    
def logout(request):
    auth.logout(request)
    return redirect('/')

def token(request):
    if request.method == 'POST':
        v1 = request.POST.get('v1') == 'on'
        v2 = request.POST.get('v2') == 'on'
        v3 = request.POST.get('v3') == 'on'
        v4 = request.POST.get('v4') == 'on'
        quantity = request.POST.get('quantity',0)
        pinCode = request.POST.get('pinCode',0)
        
        # Create a FarmerData instance and save it
        if FarmerData.objects.filter(user=request.user).exists():
            messages.info(request, "Token Already generated")
            print(FarmerData.objects.get(user=request.user).time_slot.start_time)
            return render(request,'success.html',{'farmer':FarmerData.objects.get(user=request.user)})
        else:
            farmer_data = FarmerData(user=request.user, v1=v1, v2=v2, v3=v3, v4=v4, quantity=quantity, pinCode=pinCode)
            farmer_data.save()
            next_time_slot = TimeSlot.objects.filter(is_available=True).first()

            if next_time_slot:
                # Allocate the time slot to the farmer and mark it as unavailable
                millisec = int(round(time.time() * 1000))
                farmer_data.time_slot = next_time_slot
                farmer_data.token = str(millisec)
                farmer_data.save()
                next_time_slot.is_available = False
                next_time_slot.save()

                

                return render(request, 'success.html',{'farmer':FarmerData.objects.get(user=request.user)})
            else:
                messages.info(request, "No available time slots")
                return  redirect('token')
            
    else:
        return render(request, 'cart.html')
    
@csrf_exempt
def initialize_time_slots(request):
    # Define the time slots (9 am to 5 pm with a break from 1 pm to 2 pm)
    start_time = datetime.time(9, 0)
    end_time = datetime.time(17, 0)
    break_start = datetime.time(13, 0)
    break_end = datetime.time(14, 0)

    # Clear all existing time slots
    TimeSlot.objects.all().delete()

    current_time = start_time
    while current_time < end_time:
        if current_time < break_start or current_time >= break_end:
            # Create a time slot for every 20 minutes
            slot_start = datetime.datetime(datetime.date.today().year, datetime.date.today().month, datetime.date.today().day, current_time.hour, current_time.minute, tzinfo=timezone.get_current_timezone())
            slot_end = slot_start + datetime.timedelta(minutes=20)
            TimeSlot.objects.create(start_time=slot_start.time(), end_time=slot_end.time())


        current_time = (datetime.datetime.combine(datetime.date.today(), current_time) + datetime.timedelta(minutes=20)).time()

    return JsonResponse({"message": "Time slots initialized."})