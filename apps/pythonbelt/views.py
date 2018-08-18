from django.shortcuts import render, redirect
from django.contrib import messages
import datetime
from .models import *
# take out datetime later

def travels(request):
    print("*"*25, " At Travels " , "*"*25)
    if 'user_id' not in request.session:
        return redirect ('/')
    current_user=User.objects.get(id = request.session['user_id'])
# trips im in
    my_trips =User.objects.get(id = request.session['user_id']).trips.all()
# trips im not in 
    other_trips = Trip.objects.all().difference(my_trips)
    if 'user_id' in request.session:
        dis = "Welcome back " + current_user.first_name
    context=  {
        'current_user':  current_user,
        'Banner' : dis,
        'my_trips':my_trips,
        'other_trips':other_trips , 
    }         
    return render(request, 'travels.html', context)

def index(request):
    print("*"*25, " At Index " , "*"*25)
    request.session.flush()
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        print("*"*25, " At Login " , "*"*25)
        result = User.objects.LoginValidator(request.POST)
        if len(result['errors']) > 0:
            print("errors are  : ",  result['errors'])
            for error in result['errors']:
                messages.error(request, error)
            return redirect('/')
        else:
            request.session['user_id']  = result['user_id']
            return redirect('/travels')
    else:
        return redirect('/')
    return redirect('/')

def register(request):
    if request.method == 'POST':
        print("*"*25, " At Register " , "*"*25)
        result = User.objects.validateUser(request.POST)
        if len(result['errors']) > 0:
            print("errors are  : ",  result['errors'])
            for error in result['errors']:
                messages.error(request, error)
            return redirect('/')
        else:
            request.session['user_id']  = result['user_id']
            return redirect('/travels')
    else:
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')
        
def addtrip(request):
    print("*"*25, " At Addtrip " , "*"*25)
    if 'user_id' not in request.session:
        return redirect ('/')
    return render(request, "addtrip.html")

def newtrip(request):
    if request.method != 'POST':
        return redirect('/addtrip')
    print("-"*50)
    print("post is ", request.POST)
    print("-"*50)
# start Create/Validation
    result = Trip.objects.ValidateTrip(request.POST)
    if len(result['errors']) > 0:
        # print("errors are  : ",  result['errors'])
        for error in result['errors']:
            messages.error(request, error)
        return redirect('/addtrip')
    else:
        print("no errors")
        messages.error(request, ("Successfully created Trip ID:"+ str(result['tripid'])))
        return redirect('/travels')

def show(request, id):
    if 'user_id' not in request.session:
        return redirect ('/')
# define trip and owner
    show_trip = Trip.objects.get(id = id )
    this_owner = Trip.objects.get(id = id ).owner
# find all users in trip
    trip_users = Trip.objects.get(id = id ).users.all()
# subtract owner in trip from total users
    non_owner_users = trip_users.exclude(id=show_trip.owner.id).exclude(id =request.session['user_id'])
    context = {
        'show_trip': show_trip, 
        'non_owner_users':non_owner_users,
    }
    return render(request, 'show.html' , context)

def destroy(request, id):
    if 'user_id' not in request.session:
        return redirect ('/')
    delete_trip = Trip.objects.get(id = id)
    if request.session['user_id'] == delete_trip.owner.id:
        print("destroying trip ", delete_trip.id)
        delete_trip.delete()
    return redirect('/travels')

def join(request, id):
    if 'user_id' not in request.session:
        return redirect ('/')
    print("-"*25, "at join")
    this_user = User.objects.get(id =request.session['user_id'] )
    this_trip = Trip.objects.get(id = id)
    this_trip.users.add(this_user)
    print("joining trip ", this_trip.id)
    return redirect('/travels')


def cancel(request, id):
    if 'user_id' not in request.session:
        return redirect ('/')
    print("-"*25, "at cancel","-"*25,)
    print("trip id is ", id)
    this_user = User.objects.get(id =request.session['user_id'] )
    this_trip = Trip.objects.get(id = id)
    print("*"*25,"before ",this_trip.users.all())
    this_trip.users.remove(this_user)
    print("*"*25,"after ",this_trip.users.all())
    return redirect('/travels')
