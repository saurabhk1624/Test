from datetime import datetime, timezone
import json
import re
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import get_object_or_404
# from django.utils import simplejson
from Registartion.models import Register, ToDoList
# from django.db.models import Count
import pytz

def signup(request):
     if request.method=='POST':
       mydb=json.loads(request.body)
       user_name=mydb['username']
       user_email=mydb['email']
       user_password=mydb['password']
       usercon_password=['confirmpassword']
       hash=make_password(user_password)
       if not user_name or not user_email:
           return JsonResponse({'message':'All fields are required'})
     
       else:
        if not  re.match(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b',user_email) :
           return JsonResponse({'message':'Not valid Email'})
        else:
         if Register.objects.filter(email=user_email).exists():
          return JsonResponse({'message':'Email already exist'})
         else:
           if re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{8,15}$",user_password) is None:
             return JsonResponse({'message':'Password denied: Password is not valid'})
           else:
            #  if not  user_password==usercon_password:
            #   return JsonResponse({'message':'confirm password not same'})
            #  else:                 
              createuser=Register(username=user_name,email=user_email,password=hash)
              createuser.save()
              return JsonResponse({'message':'Succesfully registered'},status=201)
         
           
         
     else:
       return JsonResponse({'message':'Not Successful'})

def signin(request):
  # if Register.objects.filter(session=True).exists():
  #   return JsonResponse({'message':'Already a user is signed in'})
  # else:
    if request.method=='POST':
      acess=json.loads(request.body)
      login_email=acess['email']
      login_pass=acess['password']
    #   auth_email=Register.objects.get(email=login_email)
    #   pass1=auth_email.password
    
      if not login_email or not login_pass:
         return JsonResponse({'message':'All inputs are required'})
      
      else:  
       if Register.objects.filter(email=login_email).exists():
         auth_email=Register.objects.get(email=login_email)
         if check_password(login_pass,auth_email.password):
          if auth_email.session==True:
            return JsonResponse({'messsage':'user is already signed in'})
          else:
           auth_email.session=True
           auth_email.save()
          
           id=auth_email.id
           return JsonResponse({'id':id},status=200)
         else:
          return JsonResponse({'message':'Wrong Password'})
       else:
         return JsonResponse({'message':'Email does not exist'})  
    else:
      return JsonResponse({'message':'Wrong Method'})

def logout(request):

  if request.method=='POST':
    access=json.loads(request.body)
    id=access['id']
    
  #  if not id or to_do or update or complete or delete or logout:
  #   return JsonResponse({'message':'all fields are required'})
  #  else:
    if Register.objects.filter(id=id).exists():
 
      session_time=Register.objects.get(id=id)
      if session_time.session: 
       session_time.session=False
       session_time.save()
       return JsonResponse({'message':'Logged out'})
     
     
    else:
       return JsonResponse({'message':'Email does not exist'})
  else:
     return JsonResponse ({'message':'method not allowed'})

def todolist(request):
  
    if request.method=='POST':
       req=json.loads(request.body)
       id=req['id']
       to_do=req['description']
       ToDoList.objects.create(todolist=to_do,creationtime=datetime.now(),register_id=id)
       data=ToDoList.objects.filter(register_id=id).first()
       return JsonResponse({'creation successfully':data.id}) 
    elif request.method=='GET':
            #  req=json.loads(request.body)
            #  id=req['id']
       id=request.GET.get('id')
       if ToDoList.objects.filter(register_id=id).exists():
        todo=ToDoList.objects.filter(register_id=id ,deleted=False )
        todoshow=list(todo)
        todo_list=[{'todo':todo.todolist} for todo in todoshow ]
        return JsonResponse(todo_list,safe=False)
       else:
        return JsonResponse({'message':'user does not exist'})
    elif request.method=='PUT':
     req=json.loads(request.body)
    #  id=req['register_id']
     todoid=req['id']
    #  update=req['updation']  
     to_do=req['todolist'] 
     complete=['completion']
     if complete ==False:
      data=ToDoList.objects.get(id=todoid)
      data.todolist=to_do
      data.updation=False
      data.save()
      return JsonResponse({'message':'update successfully'})
     elif complete==True:
       data1=ToDoList.objects.get(id=todoid)
       data1. completiontime=datetime.now()
       data1.save()
       return JsonResponse({'message':'Completed successfully'})
    elif request.method=='DELETE':
      req=json.loads(request.body)
      # id=req['register_id']
      todoid=req['id']
      delete=req['deleted']
      data=ToDoList.objects.get(id=todoid) 
      data.deletedtime=datetime.now()
      data.deleted=True 
      data.save()
      return JsonResponse({'message':'deleted successfully'})
    