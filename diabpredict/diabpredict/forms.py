from django.forms import ModelForm
from django import forms
from .models import User, Provider, Patient, PatientTest
from django.db.models import CharField, Value as V
from django.db.models.functions import Concat
from django_range_slider.fields import RangeSliderField
from django.utils.safestring import mark_safe

USER_TYPE= [
    ('PR', 'Provider'),
    ('PA', 'Patient')
    ]

ANSWER_CHOICES = [
    (0,'No'),
    (1,'Yes')
]

GENDER_CHOICES= [
    ('M', 'Male'),
    ('F', 'Female'),
    ]
class DateInput(forms.DateInput):
    input_type = 'date'

class SignUpForm(ModelForm):
    type_of_user = forms.ChoiceField(choices=USER_TYPE, widget=forms.RadioSelect())
    date_of_birth = forms.DateField(widget = DateInput, label = "Date of Birth")
    pwd = forms.CharField(widget=forms.PasswordInput(), label = "Enter Password")
    class Meta:
        model = User
        fields = ('first_name','last_name','email','pwd','repwd','type_of_user','gender','date_of_birth','phone','address','profilePic')
        labels = {'first_name':'First Name',
                    'last_name':'Last Name',
                    'email':'Email',
                    'pwd':'Enter Password',
                    'repwd':'Renter Password',
                    'type_of_user':'Type of User',
                    'gender':'Gender',
                    'date_of_birth':'Date of Birth',
                    'phone':'Phone',
                    'address':'Address',}
        exclude = ['repwd']

class LoginForm(forms.Form):
    user_name = forms.CharField(label="Username (Email Id)", max_length = 100)
    password = forms.CharField(label="Password", max_length = 15, widget=forms.PasswordInput())

class PatientDemographicsForm(forms.ModelForm):
    doctors = User.objects.filter(type_of_user = 'PR').annotate(full_name = Concat('first_name', V(' ') ,'last_name')).values_list('user_id','full_name')
    doctor_id = forms.CharField(widget = forms.Select(choices = doctors))
    patient_id = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = Patient
        # doctors = User.objects.filter(type_of_user = 'PR').annotate(full_name = Concat('first_name', V(' ') ,'last_name')).values_list('user_id','full_name')
        # doctor_id = forms.CharField(widget = forms.Select(choices = doctors))
        fields = ('patient_id','doctor_id','hospital','blood_group','height','weight','medical_allergies','medications',)
        labels = {'patient_id':"Patient ID",
                    'doctor_id':"Doctor's Name",
                    'hospital':'Hospital Name',
                    'blood_group':'Blood Group',
                    'height':'Height',
                    'weight':'Weight',
                    'medical_allergies':'Medical Allergies (if any)',
                    'medications':'Ongoing Medications (if any)',
                    }

class ProviderDemographicsForm(ModelForm):
    provider_id = forms.IntegerField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = Provider
        fields = ('provider_id','speciality','hospital')
        labels: {
            'provider_id':'Doctor ID',
            'speciality':'Speciality',
             'hospital':'Hospital',
        }

class DiabPredForm(ModelForm):
    high_bp = forms.ChoiceField(label='1. To the best of your knowledge, do you have a history of high blood pressure?', choices = ANSWER_CHOICES, widget = forms.RadioSelect(attrs={'class': 'inline'}))
    high_chol = forms.ChoiceField(label='2. To the best of your knowledge, do you have a history of high cholesterol?', choices = ANSWER_CHOICES, widget = forms.RadioSelect())
    chol_check = forms.ChoiceField(label='3. Has your cholesterol been checked in the last 5 years?', choices = ANSWER_CHOICES, widget = forms.RadioSelect())
    smoker = forms.ChoiceField(label='4. Do you have a history of smoking cigarettes or do you currently smoke?', choices = ANSWER_CHOICES, widget = forms.RadioSelect())
    stroke = forms.ChoiceField(label='5. Have you ever had a stroke?', choices = ANSWER_CHOICES, widget = forms.RadioSelect())
    heart_disease = forms.ChoiceField(label='6. Have you ever been diagnosed with coronary heart disease (CHD) or myocardial infarction (MI)?', choices = ANSWER_CHOICES, widget = forms.RadioSelect())
    phy_activity = forms.ChoiceField(label='7. Have you participated in physical activity in past 30 days not including job?', choices = ANSWER_CHOICES, widget = forms.RadioSelect())
    fruits = forms.ChoiceField(label='8. Do you consume fruits 1 or more times per day?', choices = ANSWER_CHOICES, widget = forms.RadioSelect())
    veggies = forms.ChoiceField(label='9. Do you consume vegetables 1 or more times per day?', choices = ANSWER_CHOICES, widget = forms.RadioSelect())
    hvy_alcohol = forms.ChoiceField(label='10. Are you a heavy drinker? (adult men having more than 14 drinks per week and adult women having more than 7 drinks per week)?', choices = ANSWER_CHOICES, widget = forms.RadioSelect())
    any_healthcare = forms.ChoiceField(label='11. Do you have any kind of health care coverage, including health insurance, prepaid plans such as HMO, etc.?', choices = ANSWER_CHOICES, widget = forms.RadioSelect())
    no_doc_bc_cost = forms.ChoiceField(label='12. Was there a time in the past 12 months when you needed to see a doctor but could not because of cost?', choices = ANSWER_CHOICES, widget = forms.RadioSelect())
    gen_health = forms.IntegerField(label="13. How would you rate your general health?",widget=forms.NumberInput(attrs={'type':'range', 'step': '1', 'min': '1', 'max': '5', 'id':'genhealthSlider', 'value':'1'}), required = True)
    ment_health = forms.IntegerField(label="14. Now thinking about your mental health, which includes stress, depression, and problems with emotions, for how many days during the past 30 days was your mental health poor?")
    phy_health = forms.IntegerField(label="15. Now thinking about your mental health, which includes stress, depression, and problems with emotions, for how many days during the past 30 days was your general health poor?")
    diff_walk = forms.ChoiceField(label='16. Do you have serious difficulty walking or climbing stairs?', choices = ANSWER_CHOICES, widget = forms.RadioSelect())
    education= forms.IntegerField(label="17. What is the highest level of education that you have completed?",widget=forms.NumberInput(attrs={'type':'range', 'step': '1', 'min': '1', 'max': '6', 'id':'educationSlider', 'value':'1'}), required = True)
    income = forms.IntegerField(label="18. What is your income?")
    class Meta:
        model = PatientTest
        fields = (
            'patient_id',
            'high_bp',
            'high_chol',
            'chol_check',
            'bmi',
            'smoker',
            'stroke',
            'heart_disease',
            'phy_activity',
            'fruits',
            'veggies',
            'hvy_alcohol',
            'any_healthcare',
            'no_doc_bc_cost',
            'gen_health',
            'ment_health',
            'phy_health',
            'diff_walk',
            'sex',
            'age',
            'education',
            'income',
            'diab_pred',
        )