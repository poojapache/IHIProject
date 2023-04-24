from django.db import models
import datetime
from django.utils import timezone

class User(models.Model):
    GENDER_CHOICES= [
    ('M', 'Male'),
    ('F', 'Female'), 
    ('O', 'Other')
    ]
    user_id = models.AutoField(primary_key = True)
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    pwd = models.CharField(max_length = 15)
    type_of_user = models.CharField(max_length = 2)
    gender = models.CharField(max_length = 1, choices = GENDER_CHOICES)
    date_of_birth = models.DateTimeField('DOB')
    email = models.CharField(max_length = 100, unique = True)
    phone = models.CharField(max_length = 10)
    address = models.CharField(max_length = 300)
    profilePic = models.ImageField(upload_to='uploads/', default='uploads/default.jpg', blank=True)

    def __str__(self):
       return str(self.user_id)

class Provider(models.Model):
    provider_id = models.OneToOneField(User, on_delete = models.CASCADE, unique=True)
    speciality = models.CharField(max_length = 100)
    hospital = models.CharField(max_length  = 100)

class Patient(models.Model):
    BLOOD_GROUPS= [
    ('A+', 'A+'),
    ('A-', 'A-'), 
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ]
    patient_id = models.OneToOneField(User, on_delete = models.CASCADE, unique=True, related_name = 'patient_id')
    doctor_id = models.CharField(max_length = 300)
    hospital = models.CharField(max_length = 300)
    blood_group = models.CharField(max_length = 5, choices = BLOOD_GROUPS)
    height = models.CharField(max_length = 5)
    weight = models.CharField(max_length = 5)
    medical_allergies = models.CharField(max_length = 500)
    medications = models.CharField(max_length = 500)

class PatientTest(models.Model):
    CHOICES = [
    ('1', 'Yes'),
    ('0', 'No')
    ]
    GENDER_CHOICES= [
    ('M', 'Male'),
    ('F', 'Female'),
    ]
    test_id = models.AutoField(primary_key = True)
    patient_id = models.ForeignKey(User, on_delete = models.CASCADE)
    test_date = models.DateField(auto_now_add = True)
    high_bp = models.IntegerField()
    high_chol = models.IntegerField()
    chol_check = models.IntegerField()
    bmi = models.FloatField()
    smoker = models.IntegerField()
    stroke = models.IntegerField()
    heart_disease = models.IntegerField()
    phy_activity = models.IntegerField()
    fruits = models.IntegerField()
    veggies = models.IntegerField()
    hvy_alcohol = models.IntegerField()
    any_healthcare = models.IntegerField()
    no_doc_bc_cost = models.IntegerField()
    gen_health = models.IntegerField()
    ment_health = models.IntegerField()
    phy_health = models.IntegerField()
    diff_walk = models.IntegerField()
    sex = models.CharField(max_length = 1,choices = GENDER_CHOICES)
    age = models.IntegerField()
    education = models.IntegerField()
    income = models.IntegerField()
    diab_pred = models.IntegerField(null=True, blank=True)

