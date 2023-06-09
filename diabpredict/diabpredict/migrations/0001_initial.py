# Generated by Django 3.2.5 on 2023-04-24 00:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('pwd', models.CharField(max_length=15)),
                ('type_of_user', models.CharField(max_length=2)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('date_of_birth', models.DateTimeField(verbose_name='DOB')),
                ('email', models.CharField(max_length=100, unique=True)),
                ('phone', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=300)),
                ('profilePic', models.ImageField(blank=True, default='uploads/default.jpg', upload_to='uploads/')),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('speciality', models.CharField(max_length=100)),
                ('hospital', models.CharField(max_length=100)),
                ('provider_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='diabpredict.user')),
            ],
        ),
        migrations.CreateModel(
            name='PatientTest',
            fields=[
                ('test_id', models.AutoField(primary_key=True, serialize=False)),
                ('test_date', models.DateField(auto_now_add=True)),
                ('high_bp', models.IntegerField()),
                ('high_chol', models.IntegerField()),
                ('chol_check', models.IntegerField()),
                ('bmi', models.FloatField()),
                ('smoker', models.IntegerField()),
                ('stroke', models.IntegerField()),
                ('heart_disease', models.IntegerField()),
                ('phy_activity', models.IntegerField()),
                ('fruits', models.IntegerField()),
                ('veggies', models.IntegerField()),
                ('hvy_alcohol', models.IntegerField()),
                ('any_healthcare', models.IntegerField()),
                ('no_doc_bc_cost', models.IntegerField()),
                ('gen_health', models.IntegerField()),
                ('ment_health', models.IntegerField()),
                ('phy_health', models.IntegerField()),
                ('diff_walk', models.IntegerField()),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('age', models.IntegerField()),
                ('education', models.IntegerField()),
                ('income', models.IntegerField()),
                ('diab_pred', models.IntegerField(blank=True, null=True)),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diabpredict.user')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor_id', models.CharField(max_length=300)),
                ('hospital', models.CharField(max_length=300)),
                ('blood_group', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], max_length=5)),
                ('height', models.CharField(max_length=5)),
                ('weight', models.CharField(max_length=5)),
                ('medical_allergies', models.CharField(max_length=500)),
                ('medications', models.CharField(max_length=500)),
                ('patient_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patient_id', to='diabpredict.user')),
            ],
        ),
    ]
