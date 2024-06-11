from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.sessions.models import Session

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
import xgboost as xgb
import pickle
from .chatbot import *
from django.views import View
from django.http import JsonResponse
from django.db.models import Q
import re
# User Views

# Create your views here.


def Home(request):
    return render(request, "Home.html", {})


def Base(request):
    return render(request, "Base.html", {})


def about(request):
    return render(request, 'about.html')


def User_Login(request):
    if request.method == "POST":
        C_user = request.POST['username']
        C_password = request.POST['password']
        if loggedin.objects.filter(Username=C_user, Password=C_password).exists():
            users = loggedin.objects.all().filter(Username=C_user, Password=C_password)
            messages.info(request, ' logged in')
            request.session['type_id'] = 'User'
            request.session['login'] = "Yes"
            return redirect("/")
        elif loggedin.objects.filter(Email=C_user).exists():
            messages.error(request, 'wrong password')
            return render(request, "User_Login.html", {})
        else:
            messages.error(request, 'Please Register')
            return redirect("/User_Registration")
    else:
        return render(request, 'User_Login.html', {})


def Admin_Login(request):
    if request.method == "POST":
        A_username = request.POST['username']
        A_password = request.POST['password']
        if AdminDetails.objects.filter(Username=A_username, Password=A_password).exists():
            ad = AdminDetails.objects.get(
                Username=A_username, Password=A_password)
            messages.info(request, 'Your login is Sucessfull')
            request.session['type_id'] = 'Admin'
            request.session['login'] = "Yes"
            return redirect("/")
        else:
            messages.error(request, 'Error wrong username/password')
            return redirect("/")
    else:
        return render(request, 'Admin_Login.html', {})


def User_Registration(request):
    if request.method == "POST":
        Name = request.POST['Name']
        Phone = request.POST['Phone']
        Email = request.POST['Email']
        Address = request.POST['Address']
        State = request.POST['State']
        City = request.POST['City']
        Username = request.POST['Username']
        Password = request.POST['Password']
        if loggedin.objects.filter(Email=Email, Username=Username).exists():
            myObjects = loggedin.objects.all().filter(Email=Email, Username=Username)
            name = myObjects[0].Username
            messages.error(request, 'Already Registered Please Login')
            return render(request, 'login.html', {})
        else:
            Data = loggedin(Name=Name, Phone=Phone, Email=Email, Username=Username,
                            Password=Password, Address=Address, State=State, City=City)
            Data.save()
            messages.info(request, 'Registered Sucessfully')
            return redirect("/User_Login/")
    else:
        return render(request, 'User_Registration.html', {})


def Logout(request):
    Session.objects.all().delete()
    return redirect("/")


def view_users(request):
    details = loggedin.objects.all()
    return render(request, "view_users.html", {'details': details})


def view_hospitals(request):
    data = Hospitals_Data.objects.all()
    return render(request, "view_hospitals.html", {'data': data})


def hospitals(request):
    if request.method == 'POST':
        hospital_name = request.POST.get('hospital_name')
        contact_number = request.POST.get('contact_number')
        emergency_contact = request.POST.get('emergency_contact')
        address = request.POST.get('address')
        area = request.POST.get('Area')
        city = request.POST.get('City')
        state = request.POST.get('State')
        specialties = request.POST.get('specialties')
        website = request.POST.get('website')
        hospital = Hospitals_Data(
            hospital_name=hospital_name,
            contact_number=contact_number,
            emergency_contact=emergency_contact,
            address=address,
            Area=area,
            City=city,
            State=state,
            specialties=specialties,
            website=website)
        hospital.save()
        return redirect('/hospitals')
    else:
        data = Hospitals_Data.objects.all()
        return render(request, "hospitals.html", {'data': data})


def update_hospital(request):
    if request.method == 'POST':

        modal_id = request.POST.get("modalid")
        hospital_name = request.POST.get("modalhospitalName")
        contact_number = request.POST.get("modalcontactNumber")
        print(contact_number)
        emergency_contact = request.POST.get("modalemergencyContact")
        print(emergency_contact)
        specialties = request.POST.get("modalspecialties")
        address = request.POST.get("modalAddress")
        area = request.POST.get("modalArea")
        state = request.POST.get("modalState")
        city = request.POST.get("modalCity")
        website = request.POST.get("modalwebsite")

        hospital1 = Hospitals_Data.objects.get(id=modal_id)
        hospital1.hospital_name = hospital_name
        hospital1.contact_number = contact_number
        hospital1.emergency_contact = emergency_contact
        hospital1.specialties = specialties
        hospital1.address = address
        hospital1.area = area
        hospital1.state = state
        hospital1.city = city
        hospital1.website = website
        hospital1.save()
        messages.error(request, 'Hospital details updated successfully.')
        return redirect('/hospitals')
    else:
        data = Hospitals_Data.objects.all()
    return render(request, "hospitals.html", {'data': data})


def delete_doctor(request):

    if request.method == "POST":
        Test_id = request.POST['id']
        print(Test_id)
        test = Hospitals_Data.objects.filter(id=Test_id)
        test.delete()
        messages.success(request, 'Hospital has been deleted successfully.')
        return redirect('/hospitals')
    else:
        return redirect('/hospitals')


def prediction(request):
    return render(request, "prediction.html", {})


def chatbot(request):
    return render(request, "chatbot.html", {})


def liver(request):
    if request.method == 'POST':
        age = request.POST['age']
        gender = request.POST['gender']
        total_bilirubin = request.POST['total_bilirubin']
        direct_bilirubin = request.POST['direct_bilirubin']
        alkaline_phosphatase = request.POST['alkaline_phosphatase']
        alt = request.POST['alt']
        ast = request.POST['ast']
        total_proteins = request.POST['total_proteins']
        albumin = request.POST['albumin']
        albumin_globulin_ratio = request.POST['albumin_globulin_ratio']

        user_input = {'Age': age, 'Gender': gender, 'Total_Bilirubin': total_bilirubin, 'Direct_Bilirubin': direct_bilirubin, 'Alkaline_Phosphotase': alkaline_phosphatase,
                      'Alamine_Aminotransferase': alt, 'Aspartate_Aminotransferase': ast, 'Total_Protiens': total_proteins, 'Albumin': albumin, 'Albumin_and_Globulin_Ratio': albumin_globulin_ratio}
        print(user_input)
        with open('models/random_forest_model_liver.pkl', 'rb') as model_file:
            loaded_model = pickle.load(model_file)
        user_input_list = [user_input[column] for column in user_input]
        predicted_class = loaded_model.predict([user_input_list])[0]
        print(predicted_class)

        description = "You are likely to have liver disease." if predicted_class == 1 else "You are likely not to have liver disease."
        print(description)
        messages.info(request, description)

        if predicted_class == 1:
            data = Hospitals_Data.objects.all().filter(specialties="Liver")
            return render(request, "view_hospitals.html", {'data': data})
        else:
            return redirect('/liver')
    else:
        return render(request, "liver.html", {})


def heart(request):
    if request.method == 'POST':
        age = request.POST.get('age')
        sex = request.POST.get('sex')
        chest_pain = request.POST.get('chest_pain')
        resting_bp = request.POST.get('resting_bp')
        cholesterol = request.POST.get('cholesterol')
        fasting_sugar = request.POST.get('fasting_sugar')
        resting_ecg = request.POST.get('resting_ecg')
        max_heart_rate = request.POST.get('max_heart_rate')
        exercise_angina = request.POST.get('exercise_angina')
        oldpeak = request.POST.get('oldpeak')
        st_segment = request.POST.get('st_segment')
        num_vessels = request.POST.get('num_vessels')
        thal = request.POST.get('thal')
        user_input = {'age': age, 'sex': sex, 'chest pain type': chest_pain, 'resting blood pressure': resting_bp, 'serum cholestoral': cholesterol, 'fasting blood sugar': fasting_sugar,
                      'resting electrocardiographic results': resting_ecg, 'max heart rate': max_heart_rate, 'exercise induced angina': exercise_angina, 'oldpeak': oldpeak, 'ST segment': st_segment, 'major vessels': num_vessels, 'thal': thal}
        with open('models/random_forest_model_heart.pkl', 'rb') as model_file:
            loaded_model = pickle.load(model_file)
        user_input_list = [user_input[column] for column in user_input]
        predicted_class = loaded_model.predict([user_input_list])[0]
        print(predicted_class)
        description = "You are likely to have heart disease." if predicted_class == 1 else "You are likely not to have heart disease."
        print(description)
        messages.info(request, description)

        if predicted_class == 1:
            data = Hospitals_Data.objects.all().filter(specialties="heart")
            return render(request, "view_hospitals.html", {'data': data})
        else:
            return redirect('/heart')
    else:
        return render(request, "heart.html", {})


def diabetes(request):
    if request.method == 'POST':
        # Get data from the form
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        polyuria = request.POST.get('polyuria')
        polydipsia = request.POST.get('polydipsia')
        sudden_weight_loss = request.POST.get('sudden_weight_loss')
        weakness = request.POST.get('weakness')
        polyphagia = request.POST.get('polyphagia')
        genital_thrush = request.POST.get('genital_thrush')
        visual_blurring = request.POST.get('visual_blurring')
        itching = request.POST.get('itching')
        irritability = request.POST.get('irritability')
        delayed_healing = request.POST.get('delayed_healing')
        partial_paresis = request.POST.get('partial_paresis')
        muscle_stiffness = request.POST.get('muscle_stiffness')
        alopecia = request.POST.get('alopecia')
        obesity = request.POST.get('obesity')

        user_input = {
            'Age': age,
            'Gender': gender,
            'Polyuria': polyuria,
            'Polydipsia': polydipsia,
            'sudden weight loss': sudden_weight_loss,
            'weakness': weakness,
            'Polyphagia': polyphagia,
            'Genital thrush': genital_thrush,
            'visual blurring': visual_blurring,
            'Itching': itching,
            'Irritability': irritability,
            'delayed healing': delayed_healing,
            'partial paresis': partial_paresis,
            'muscle stiffness': muscle_stiffness,
            'Alopecia': alopecia,
            'Obesity': obesity
        }
        with open('models/random_forest_model.pkl', 'rb') as model_file:
            loaded_model = pickle.load(model_file)
        user_input_list = [user_input[column] for column in user_input]
        predicted_class = loaded_model.predict([user_input_list])[0]
        print(predicted_class)
        description = ("You are likely to have diabetes." if predicted_class ==
                       1 else "You are likely not to have diabetes.")
        print(description)

        messages.info(request, description)

        if predicted_class == 1:
            data = Hospitals_Data.objects.all().filter(specialties="diabetes")
            return render(request, "view_hospitals.html", {'data': data})
        else:
            return redirect('/diabetes')
    else:
        return render(request, "diabetes.html", {})


class Message(View):

    def post(self, request):
        msg = request.POST.get('text')
        response = chatbot_response(msg)

        valid = validators.url(response)
        if valid == True:
            data1 = 'True'
            data = {
                'respond': response, 'respond1': data1
            }
            return JsonResponse(data)
        else:
            data1 = 'False'
            data = {
                'respond': response, 'respond1': data1
            }
            return JsonResponse(data)
