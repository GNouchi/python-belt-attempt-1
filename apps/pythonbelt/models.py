from django.db import models
from django.core.validators import validate_email 
import datetime
import bcrypt 


class UserManager(models.Manager):
    def validateUser(self, postData):
        result = {'errors' :[]}
# check for pw mismatch
        if postData['password'] != postData['confirm_password']:
            result['errors'].append("Passwords do not match")
# handles case where password input is deleted 
        if len(postData['password']) < 8:
            result['errors'].append("Passwords must be 8 or more characters")
# handles case where first_name input is deleted 
        if len(postData['first_name']) < 1:
            result['errors'].append("First Name must be 2 or more characters")            
# handles case where last_name input is deleted 
        if len(postData['last_name']) < 1:
            result['errors'].append("Last Name must be 2 or more characters")
        try:
            if postData['last_name'].isalpha() ==False or postData['first_name'].isalpha() ==False:
                result['errors'].append("Name fields can only be english letters")
                print("---------not alpha------------")
        except:
            pass
# EMAIL
        try:
            validate_email(postData['email'])
        except:
            result['errors'].append("Invalid email")
# escape function if errors exist
        if len(result['errors']) > 0:
            print("errors found, escaping now...")
            return result
        else:
            print("User create pass")
#  LAST THING HERE CHECK IF EMAIL EXISTS in DB  
            throwaway =  User.objects.filter(email = postData['email'])
            if len(throwaway) > 0:
                result['errors'].append("Please use another email")
                return result
            hash1 = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            hash1 = hash1.decode()
            newUser = User.objects.create(
                first_name=postData['first_name'] , 
                last_name=postData['last_name'],
                email = postData['email'],
                password = hash1
                )
            result['user_id'] = newUser.id
            print(result['user_id'])
            return result

    def LoginValidator(self, postData):
        result = {'errors' :[]}
        throwaway =  User.objects.filter(email = postData['email'])
        if len(throwaway) == 0:
            result['errors'].append("User or Password incorrect")
            return result
        else:
            if bcrypt.checkpw(postData['password'].encode(),throwaway[0].password.encode()):
                result['user_id'] = throwaway[0].id
                return result
            result['errors'].append("User or Password incorrect")
            return result

class User(models.Model):
    first_name = models.CharField(max_length= 50)
    last_name = models.CharField(max_length= 50)
    email = models.CharField(max_length= 255)
    password = models.CharField(max_length= 255)
    created_d = models.DateTimeField(auto_now_add = True)
    updated_d = models.DateTimeField(auto_now = True)
    objects = UserManager()
# -----------------------------------------------
# -----------------------------------------------
# -----------------------------------------------
class TripManager (models.Manager):
    def ValidateTrip(self, postData):
        result = {'errors' :[]}
# description length 
        if len(postData['description']) < 1:
            result['errors'].append("Please enter a description")
# destination length
        if len(postData['destination']) < 1:
            result['errors'].append("Please enter a destination")            
# trip_from
# --------------------
# VALIDATE START IF IN THE FUTURE
        if len(postData['trip_from']) < 1:
            result['errors'].append("Please enter a Start date")
        else:
            tf = datetime.datetime.strptime(postData['trip_from'], "%Y-%m-%d").date()
            today = datetime.datetime.today().date()
            if tf < today:
                result['errors'].append("Start Date should be today or later")

# trip_from
# --------------------
# VALIDATE END IS IN THE FUTURE
        if len(postData['trip_to']) < 1:
            result['errors'].append("Please enter an End Date")            
        else:
            if len(postData['trip_from']) > 0:
                tf = datetime.datetime.strptime(postData['trip_from'], "%Y-%m-%d").date()
                tt = datetime.datetime.strptime(postData['trip_to'], "%Y-%m-%d").date()
                today = datetime.datetime.today().date()
                if tt < tf or tt < today :
                    result['errors'].append("End date should be a future date after the start of your trip")
            else:
                tt = datetime.datetime.strptime(postData['trip_to'], "%Y-%m-%d").date()
                today = datetime.datetime.today().date()
                if tt <= today :
                    result['errors'].append("End date should be after today")

# escape function if errors exist
        if len(result['errors']) > 0:
            print("errors found, escaping now...")
            return result
        else:
            print("Trip create pass")
#  LAST THING HERE CHECK IF EMAIL EXISTS in DB  
            throwaway =  User.objects.filter(id = postData['user_id'])
            if len(throwaway) == 0:
                result['errors'].append("user not found??")
                return result
            newTrip = Trip.objects.create(
                owner=throwaway[0] , 
                description=postData['description'],
                destination = postData['destination'],
                trip_from =postData['trip_from'],
                trip_to=postData['trip_to'],
                )
            result['tripid'] = newTrip.id
            print("good job created  trip ",result['tripid'])
            return result

class Trip(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    users = models.ManyToManyField(User, related_name = "trips")
    description = models.CharField(max_length= 50)
    destination = models.CharField(max_length= 50)
    trip_from = models.DateTimeField(auto_now_add = True)
    trip_to = models.DateTimeField(auto_now_add = True)
    created_d = models.DateTimeField(auto_now_add = True)
    objects = TripManager()