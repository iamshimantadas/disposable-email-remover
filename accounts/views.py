from django.shortcuts import render, redirect
from django.http import HttpResponse
from core.models import User, ValidEmail, InvalidEmail
from django.contrib.auth import authenticate, login, logout
import dns.resolver
import re
import os
import csv
from datetime import datetime


def Register(request):
    if request.method == "POST":
        data = request.POST
        fname = data.get("first_name")
        lname = data.get("last_name")
        email = data.get("email")
        passwd = data.get("password")

        try:
            user = User.objects.create(first_name=fname, last_name=lname, email=email)
            user.set_password(passwd)
            user.save()
            login(request, user)
            return redirect("/account/dashboard/")
        except Exception as e:
            print(e)
            return HttpResponse("error occured! submit again!")
    else:
        return render(request, "register.html")


def Login(request):
    if request.method == "POST":
        data = request.POST
        email = data.get("email")
        passwd = data.get("password")

        user = authenticate(email=email, password=passwd)
        if user:
            login(request, user)
            return redirect("/account/dashboard/")
        else:
            return HttpResponse("credentials not match")
    else:
        if request.user.is_authenticated:
            return redirect("/account/dashboard/")
        else:
            return render(request, "login.html")


def Dashboard(request):
    if request.user.is_authenticated:
        if not request.user.is_manager:
            id = request.user.id
            valids = ValidEmail.objects.filter(userid=id).count()
            invalids = InvalidEmail.objects.filter(userid=id).count()
            context = {"valid_email": valids, "invalid_email": invalids}
            return render(request, "dashboard/dashboard.html", context)
        else:
            return redirect("/account/login/")
    else:
        return redirect("/account/login/")


def Validate(request):
    if request.method == "POST":
        data = request.POST
        emails = data.get("emails")

        def load_domains(file_path):
            with open(file_path, "r") as file:
                domains = [line.strip() for line in file]
            return domains

        def check_domain(domain, domain_list):
            return domain in domain_list

        if os.path.exists("emails.conf"):
            file_path = "emails.conf"

            domain_list = load_domains(file_path)

            email_list = [
                email.strip() for email in emails.split("\n") if email.strip()
            ]  # Split by newline and remove empty strings
            print(email_list)

            for x in email_list:
                regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
                email = x
                if re.fullmatch(regex, email):
                    addressToVerify = x

                    splitAddress = addressToVerify.split("@")
                    domain = str(splitAddress[1])
                    print("Domain:", domain)

                    try:
                        records = dns.resolver.resolve(domain, "MX")
                        mxRecord = records[0].exchange
                        mxRecord = str(mxRecord)
                        mxRecord = True
                    except Exception as e:
                        print(e)
                        mxRecord = False

                    if mxRecord:
                        if check_domain(domain, domain_list):
                            print("email invalid => ", email)
                            try:
                                user_obj = User.objects.get(id=request.user.id)
                                email_obj = InvalidEmail.objects.create(
                                    email=email,
                                    userid=user_obj,
                                    datetime=datetime.now(),
                                )
                                email_obj.save()
                            except Exception as e:
                                print(e)

                        else:
                            print("email valid => ", email)
                            try:
                                user_obj = User.objects.get(id=request.user.id)
                                email_obj = ValidEmail.objects.create(
                                    email=email,
                                    userid=user_obj,
                                    datetime=datetime.now(),
                                )
                                email_obj.save()
                            except Exception as e:
                                print(e)
                    else:
                        print("email not valid")
                else:
                    print("Invalid Email")

            return redirect("/account/dashboard/")

        else:
            print("file not found")
            return HttpResponse("module error -> file not found")
    else:
        return render(request, "dashboard/validate.html")


def ValidMails(request):
    if request.user.is_authenticated:
        if not request.user.is_manager:
            id = request.user.id
            num = ValidEmail.objects.filter(userid=id).count()
            email_obj = ValidEmail.objects.filter(userid=id)
            context = {"email": email_obj, "value": num}
            return render(request, "dashboard/validmails.html", context)
        else:
            return redirect("/account/login/")
    else:
        return redirect("/account/login/")


def InvalidMails(request):
    if request.user.is_authenticated:
        if not request.user.is_manager:
            id = request.user.id
            num = InvalidEmail.objects.filter(userid=id).count()
            email_obj = InvalidEmail.objects.filter(userid=id)
            context = {"email": email_obj, "value": num}
            return render(request, "dashboard/invalidmails.html", context)
        else:
            return redirect("/account/login/")
    else:
        return redirect("/account/login/")


def ValidMailsCSV(request):
    if request.user.is_authenticated:
        if not request.user.is_manager:
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="users.csv"'

            writer = csv.writer(response)
            writer.writerow(
                [
                    "EMAIL",
                    "USER",
                    "DATE",
                ]
            )

            users = ValidEmail.objects.all().values_list("email", "userid", "datetime")
            for user in users:
                writer.writerow(user)

            return response
        else:
            return redirect("/account/login/")
    else:
        return redirect("/account/login/")


def InvalidMailsCSV(request):
    if request.user.is_authenticated:
        if not request.user.is_manager:
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="users.csv"'

            writer = csv.writer(response)
            writer.writerow(
                [
                    "EMAIL",
                    "USER",
                    "DATE",
                ]
            )

            users = InvalidEmail.objects.all().values_list(
                "email", "userid", "datetime"
            )
            for user in users:
                writer.writerow(user)

            return response
        else:
            return redirect("/account/login/")
    else:
        return redirect("/account/login/")


def Logout(request):
    if request.user.is_authenticated:
        if not request.user.is_manager:
            logout(request)
            return redirect("/")
        else:
            return redirect("/account/login/")
    else:
        return redirect("/account/login/")  