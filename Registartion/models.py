
from django.db import models
class Register(models.Model):
    username = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    session=models.BooleanField(default=False)
    id=models.AutoField(primary_key=True)
class ToDoList(models.Model):
    register=models.ForeignKey(Register,on_delete=models.PROTECT)
    todolist=models.CharField(max_length=200)
    creationtime=models.DateTimeField(auto_now_add=True, blank=True,null=True) 
    updation=models.BooleanField(default=False)
    updationtime=models.DateTimeField(auto_now=True,blank=True,null=True)
    completion=models.BooleanField(default=False)
    completiontime=models.DateTimeField(auto_now_add=False,blank=True,null=True)
    deleted=models.BooleanField(default=False)
    deletedtime=models.DateTimeField(auto_now_add=False,blank=True,null=True)


