from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib import messages
from .models import User, Patient, PatientTest, Provider
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.db.models import CharField, Value as V
from django.db.models.functions import Concat
from datetime import date
from .ADABoostPrediction import ADABoost
from django.contrib import messages
from django.db.models import Prefetch
from django.db.models import Q


# Create your views here.
def index(request):
    return render(request,'diabpredict/homePage.html',{})

def signup(request):
    from .forms import SignUpForm, ProviderDemographicsForm, PatientDemographicsForm
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = SignUpForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            user_type = form.cleaned_data['type_of_user']
            new_form = form.save(commit = True)
            messages.success(request, 'Form submission successful')
            if(user_type == 'PA'):
                doctors = User.objects.filter(type_of_user = 'PR').annotate(full_name = Concat('first_name', V(' ') ,'last_name')).values_list('user_id','full_name')
                form = PatientDemographicsForm(initial={'patient_id': new_form.pk , 'doctors':doctors})
                return render(request, "diabpredict/PatientDemographics.html", {"form": form})
            else:
                form = ProviderDemographicsForm(initial={'provider_id': new_form})
                return render(request, "diabpredict/ProviderDemographics.html", {"form": form})
        else:
            form = SignUpForm()
            context = {
                    'messages':["Email ID already exists. Please enter a new one."],
                    "form": form
                }
            return render(request, "diabpredict/SignUp.html", context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignUpForm()
        return render(request, "diabpredict/SignUp.html", {"form": form})


def login(request):
    from .forms import LoginForm, SignUpForm, DiabPredForm
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            user = User.objects.filter(email = form.cleaned_data['user_name'], pwd = form.cleaned_data['password'])
            if(user):
                user_attr = user.values()[0]
                user_id = user_attr['user_id']
                first_name = user_attr['first_name']
                last_name = user_attr['last_name']
                user_type = user_attr['type_of_user']
                dob = user_attr['date_of_birth']
                gender = user_attr['gender']
                email = user_attr['email']
                phone = user_attr['phone']
                profilePic = user_attr['profilePic']
                today = date.today()
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                if(user_type == 'PA'):
                    doctor = Patient.objects.filter(patient_id = user_id).values('doctor_id','height','weight')
                    doctor_id = doctor[0]['doctor_id']
                    height = doctor[0]['height']
                    weight = doctor[0]['weight']
                    doctor_name = User.objects.filter(user_id = doctor_id).values('first_name','last_name','profilePic')
                    doctor_full_name = doctor_name[0]['first_name'] + doctor_name[0]['last_name']
                    doctor_pic = doctor_name[0]['profilePic']
                    bmi = round(float(weight) / float(height)**2,2)

                    form = DiabPredForm(initial={'patient_id': user_id,
                                                'sex':gender,
                                                'age':age,
                                                'bmi':bmi})

                    context = { 'patient_id': user_id,
                                'first_name':first_name,
                                'last_name':last_name,
                                'age':age,
                                'bmi':bmi,
                                'gender':gender,
                                'email':email,
                                'phone':phone,
                                'doctor_name':doctor_full_name,
                                'doctor_pic':doctor_pic,
                                'form':form,
                                'messages':'',
                                'profilePic':profilePic,
                                }

                    request.session['patient_id'] = user_id
                    return render(request, "diabpredict/PatientDashboard.html", context)
                else:
                    doctor_info = Provider.objects.filter(provider_id = user_id).values()
                    filtered_patients = Patient.objects.all().exclude(~Q(doctor_id = user_id))
                    patients = User.objects.filter(user_id__in = filtered_patients.values_list('patient_id_id', flat=True)).values()
                    speciality = doctor_info[0]['speciality']
                    hospital = doctor_info[0]['hospital']
                    context = { 'doctor_id': user_id,
                                'first_name':first_name,
                                'last_name':last_name,
                                'age':age,
                                'gender':gender,
                                'email':email,
                                'phone':phone,
                                'speciality':speciality,
                                'hospital':hospital,
                                'patients':patients,
                                'messages':'',
                                'profilePic':profilePic,}
                    return render(request, "diabpredict/ProviderDashboard.html", context)
            else:
                form = LoginForm()
                context = {
                    'messages':["Username or password is invalid. Please re-enter."],
                    "form": form
                }
                return render(request, "diabpredict/Login.html", context)
        else:
            form = LoginForm()
            context = {
                    'messages':'',
                    "form": form
            }
            return render(request, "diabpredict/Login.html", context)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()
        context = {
                    'messages':'',
                    "form": form
                }
        return render(request, "diabpredict/Login.html", context)

def patientDemographics(request):
    from .forms import PatientDemographicsForm
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = PatientDemographicsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect("homePage.html")
        else:
            return render(request,'diabpredict/PatientDashboard.html',{})
    # if a GET (or any other method) we'll create a blank form
    else:
        return render(request,'diabpredict/PatientDemographics.html',{})

def providerDemographics(request):
    from .forms import ProviderDemographicsForm
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ProviderDemographicsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect("homePage.html")
        else:
            return render(request,'diabpredict/ProviderDashboard.html',{})
    # if a GET (or any other method) we'll create a blank form
    else:
        return render(request,'diabpredict/ProviderDemographics.html',{})  



def patientDashboard(request):
    from .forms import DiabPredForm
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = DiabPredForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # Call the ML predictor
            input_data = {
                    "HighBP": form.cleaned_data['high_bp'],
                    "HighChol":form.cleaned_data['high_chol'],
                    "CholCheck": form.cleaned_data['chol_check'],
                    "BMI": form.cleaned_data['bmi'],
                    "Smoker": form.cleaned_data['smoker'],
                    "Stroke": form.cleaned_data['stroke'],
                    "HeartDiseaseorAttack": form.cleaned_data['heart_disease'],
                    "PhysActivity": form.cleaned_data['phy_activity'],
                    "Fruits": form.cleaned_data['fruits'],
                    "Veggies": form.cleaned_data['veggies'],
                    "HvyAlcoholConsump": form.cleaned_data['hvy_alcohol'],
                    "AnyHealthcare": form.cleaned_data['any_healthcare'],
                    "NoDocbcCost": form.cleaned_data['no_doc_bc_cost'],
                    "GenHlth": form.cleaned_data['gen_health'],
                    "MentHlth": form.cleaned_data['ment_health'],
                    "PhysHlth": form.cleaned_data['phy_health'],
                    "DiffWalk": form.cleaned_data['diff_walk'],
                    "Sex": form.cleaned_data['sex'],
                    "Age": form.cleaned_data['age'],
                    "Education": form.cleaned_data['education'],
                    "Income": form.cleaned_data['income'],
            }
            obj = form.save(commit = False)
            obj.diab_pred = ADABoost().prediction(input_data)
            obj.save()
            # redirect to a new URL:
            return render(request,'diabpredict/PatientDashboard.html',{})
        else:
            return render(request,'diabpredict/PatientDashboard.html',{})
    # if a GET (or any other method) we'll create a blank form
    else:
        return render(request,'diabpredict/PatientDashboard.html',{})

def providerdashboard(request):
    return render(request,'diabpredict/ProviderDashboard.html',{})

def viewResults(request):
    user_id = request.session['patient_id']
    tests = PatientTest.objects.filter(patient_id = user_id).values('test_id','test_date','diab_pred')
    context = {'data': tests}
    return render(request,'diabpredict/ViewResults.html', context)