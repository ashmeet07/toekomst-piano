#My Views
from .utils import saveprofilepic, get_profile_pic
from django.http import HttpResponse
from .models import ProfileSettingsForm, ExperienceForm
from django.db import Error as db_error
from .models import Payment as PaymentModel  # Rename Payment to PaymentModel
from .models import Payment
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render
import razorpay
from django.http import JsonResponse
from .models import ContactMessage
from django.shortcuts import render, redirect
from django.utils import timezone
from django.shortcuts import redirect, render, reverse
from django.http import JsonResponse, HttpResponse
from .models import UserRegistration, InviteCode, ThemePreference
from bs4 import BeautifulSoup
import base64
import csv
import os
import pandas as pd
import mysql.connector as db
from .utils import *

def INDEX(request):
    return render(request, 'HOME.html')

def SERVICES(request):
    return render(request, 'service.html')

def ABOUT(request):
    return render(request, 'aboutus.html')

def GRADINGSYSTEM(request):
    return render(request, 'GradingSystem.html')

def FEEDBACK(request):
    return render(request, 'feedbackform.html')

def TERMS(request):
    return render(request, 't&c.html')

def about(request):
    return render(request, 'about.html')

def profilepage(request):
    return render(request, 'accountmanager.html')

def UH(request):
    return render(request, 'USERHOME.html')

def Main(request):
    if request.session.get('email'):
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.session.get('email')
            message = request.POST.get('msg')

            # Create a new ContactMessage object and save it to the database
            contact_message = ContactMessage.objects.create(
                name=name, email=email, message=message)

        return render(request,"USERTWO.html")  # Redirect to a success page
    else:
        return redirect("LOGIN")

def Payment(request):
    if request.session.get("email"):
        return render(request, "ServicePayment.html")
    else:
        return redirect("LOGIN")

def cp(request):
    if request.method == 'POST':
        email = request.POST.get('hiddenEmail')
        print(email)
    return render(request, "ForegetPassword.html")

def LOGOUT(request):
    if 'username' in request.session:
        del request.session['username']
    if 'email' in request.session:
        del request.session['email']
    return redirect('INDEX')

def SiteMap(request):
    if request.session.get("emial"):
        return render(request, "SiteMap.html")
    else:
        return redirect("LOGIN")

def INBOX(request):
    return render(request,"inbox.html")

def profile_saved(request):
    # Render a success page template
    # You can customize this template to display a success message with an alert box
    return render(request, 'profile_saved.html')

def HOME(request):
    if 'username' in request.session:
        del request.session['username']
    if 'email' in request.session:
        del request.session['email']
    if 'invite_code' in request.session:
        del request.session['invite_code']
    if 'profile_pic' in request.session:
        del request.session['profile_pic']
    return render(request, 'index.html')

def COUNTRY(request):
    return render(request, 'Countries.html')

def REGISTRATION_FORM(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('Email')
        password = request.POST.get('password')

        # Check if the email already exists in the database
        if UserRegistration.objects.filter(email=email).exists():
            # If email exists, render a registration failure page or redirect back to the registration form with an error message
            return render(request, 'registration_failure.html')
            # or
            # return redirect('REGISTRATION_FORM')
        else:
            # Hash the password before saving it
            hashed_password = hash_password(password)

            # Save user profile
            # Assuming hashed_password is already defined
            user_profile = UserRegistration.objects.create(
                name=name,
                email=email,
                password=hashed_password,
                # date_of_birth=dob  # Uncomment if needed and if 'dob' is defined
            )


            # Generate and save invite code
            invite_code = code(name, email)
            send_email_to_client(name,email,invite_code)
            InviteCode.objects.create(
                email=email,
                invite_code=invite_code
            )

            # Redirect to registration success page or login page
            # return redirect('registration_success')

    return render(request, 'registration.html')
    
def LOGIN(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if email and password are provided
        if not (password and email):
            return render(request, "LOGIN.html")

        try:
            # Fetch user object from the database based on the provided email
            user = UserRegistration.objects.get(email=email)
            passwordget = user.password  # Accessing password attribute of the user object

            # Check if the provided password matches the user's password
            if passwordget and verify_password(password, passwordget):
                # Retrieve associated invite code if exists
                invite_code = InviteCode.objects.filter(email=email).first()
                if invite_code:
                    # Set username, email, and invite_code in session
                    request.session['username'] = user.name
                    request.session['email'] = email
                    request.session['invite_code'] = invite_code.invite_code

                    # Retrieve theme preference from database
                    theme_preference = ThemePreference.objects.get(email=email)
                    print(theme_preference.theme_preference)
                    # Set theme_preference in session
                    request.session['theme_preference'] = theme_preference.theme_preference

                    profile_pic_data = get_profile_pic(email, cursor)

                    # Check if profile_pic_data is not None
                    if profile_pic_data:
                        # Encode the profile picture data to base64
                        profile_pic = base64.b64encode(profile_pic_data).decode('utf-8')
            
                        # Store the profile picture data in the session
                        request.session['profile_pic'] = profile_pic
                    else:
                        profile_pic = None

                    # Redirect to user home page
                    return redirect(reverse('USERHOME'))
                else:
                    # Handle case where invite code is not found
                    pass  # Placeholder, replace with appropriate action
        except UserRegistration.DoesNotExist as e:
            print(f"Error fetching user: {e}")
            print(f"Email: {email}")
            # Handle case where user with provided email does not exist
            pass  # Placeholder, replace with appropriate action

    return render(request, 'LOGIN.html')

def USERHOME(request):
    if request.method == 'POST':
        theme_preference = request.POST.get('theme_preference')
        email = request.POST.get('email')
        try:
            # Create or update theme preference in the database
            ThemePreference.objects.update_or_create(
                email=email, defaults={'theme_preference': theme_preference})

            # Create session for theme preference
            request.session['theme_preference'] = theme_preference

            return JsonResponse({'success': True})
        except Exception as e:
            print("Failed to store theme preference:", e)
            return JsonResponse({'success': False, 'error': 'Failed to store theme preference'})
    else:
        username = request.session.get('username')
        email = request.session.get('email')
        invite_code = request.session.get('invite_code')

        # Retrieve theme preference from session
        theme_preference = request.session.get('theme_preference')

        if not username:
            return redirect(reverse('LOGIN'))

        # Check if profile settings exist for the user
        try:
            profile_settings = ProfileSettingsForm.objects.get(email=email)
            # If profile settings exist, create sessions for each column
            request.session['name'] = profile_settings.name
            request.session['mobile_number'] = profile_settings.mobile_number
            request.session['address_line_1'] = profile_settings.address_line_1
            request.session['address_line_2'] = profile_settings.address_line_2
            request.session['country'] = profile_settings.country
            request.session['state_region'] = profile_settings.state_region
        except ProfileSettingsForm.DoesNotExist:
            # Handle case where profile settings do not exist
            pass

        return render(request, "USERHOME.html", {'name': username, 'email': email, 'invite_code': invite_code, 'theme_preference': theme_preference})

def VISA(request):
    country_dropdown_data = []
    csv_file_path = 'C:\\Users\\ashme\\OneDrive\\Documents\\Minor Project\\MinorProject\\ToekomstPiano\\static\\Files\\visacountries.csv'

    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            country_dropdown_data.append({'value': row[0], 'label': row[1]})

    return render(request, 'visa.html', {'country_dropdown_data': country_dropdown_data})

def Account(request):
        try:
                 # Read country data from CSV
             country_data = []
             csv_file = 'C:\\Users\\ashme\\OneDrive\\Documents\\Minor Project\\MinorProject\\ToekomstPiano\\static\\Files\\visacountries.csv'
             with open(csv_file, newline='', encoding='utf-8') as csvfile:
                 reader = csv.DictReader(csvfile)
                 for row in reader:
                     country_data.append(row)

             if request.method == 'POST':
                 # Get the user's email from the session
                 email = request.session.get('email')

                 # Delete previous details associated with the email
                 ProfileSettingsForm.objects.filter(email=email).delete()
                 ExperienceForm.objects.filter(email=email).delete()

                 # Handle form submission
                 name = request.session.get('username')
                 mobile_number = request.POST.get('mobile_number')
                 address_line_1 = request.POST.get('address_line_1')
                 address_line_2 = request.POST.get('address_line_2')
                 country = request.POST.get('country')
                 state_region = request.POST.get('state_region')

                 # Save ProfileSettingsForm instance
                 profile_settings = ProfileSettingsForm(
                     name=name,
                     email=email,
                     mobile_number=mobile_number,
                     address_line_1=address_line_1,
                     address_line_2=address_line_2,
                     country=country,
                     state_region=state_region
                 )
                 profile_settings.save()
                 # Save ExperienceForm instance
                 if request.POST.get("submit2"):
                     experience = ExperienceForm(
                         email=email,
                         designing_experience=designing_experience,
                         additional_details=additional_details
                     )
                     experience.save()

                 # Redirect to a success page after handling the form submission
                 return redirect("Account")

             # Get the user's email from the session
             email = request.session.get('email')

             # Fetch the profile picture data from the database
             profile_pic_data = get_profile_pic(email, cursor)

             # Check if profile_pic_data is not None
             if profile_pic_data:
                 # Encode the profile picture data to base64
                 profile_pic = base64.b64encode(profile_pic_data).decode('utf-8')
             else:
                 profile_pic = None

             # Pass the profile picture data and country data to the template
             return render(request, 'Account.html', {'profile_pic': profile_pic, 'country_data': country_data})

        except db.Error as e:
             # Handle database errors
             print(f"MySQL Error: {e}")

        finally:
             # Close cursor and database connection
             if 'cursor' in locals() and cursor is not None:
                 cursor.close()
             if 'conn' in locals() and conn is not None:
                 conn.close()

def documents(request):
    # Path to your Excel file
    excel_file_path = os.path.join(os.path.dirname(
        __file__), 'static', 'Files', 'Academic_Documents.xlsx')

    # Read data from the Excel file using pandas
    sections_df = pd.read_excel(excel_file_path)

    # Convert DataFrame to a list of dictionaries with updated keys
    sections = []
    for index, row in sections_df.iterrows():
        section = {
            'name': row['Name'],
            'id': row['ID'],
            'class': row['Class'],
            'image': row['Image'],
            'image_class': row['Image Class'],
            'description': row['Description'],
            'details': row['Details'].split(', ') if pd.notnull(row['Details']) else [],
            'optional_details': row['Optional Details'].split(', ') if pd.notnull(row['Optional Details']) else [],
            'additional_details': row['Additional Details'].split(', ') if pd.notnull(row['Additional Details']) else [],
            'alternate_option': {
                'description': row['Alternate Option'] if pd.notnull(row['Alternate Option']) else '',
                # Assuming 'Alternate Option' contains both the name and link separated by ':'
                'name': row['Alternate Option'].split(':')[0].strip() if pd.notnull(row['Alternate Option']) else '',
                'link': row['Alternate Option'].split(':')[1].strip() if pd.notnull(row['Alternate Option']) else ''
            }
        }
        sections.append(section)

    # Pass the sections data to the HTML template
    return render(request, 'documents.html', {'sections': sections})

@csrf_exempt
def submit_service_form(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        service = request.POST.get('service')
        address_line1 = request.POST.get('address-line1')
        address_line2 = request.POST.get('address-line2')
        pin_code = request.POST.get('pin-code')
        experience_title = request.POST.get('experience-title')
        years_of_experience = request.POST.get('years-of-experience')

        # Create Razorpay order
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY_ID))
        currency = "INR"
        # You can use a more appropriate receipt ID
        receipt = f"receipt_{name}"
        order = client.order.create(
            {'amount': 0, 'currency': currency, 'receipt': receipt})

        return JsonResponse({'order_id': order['id']})
    else:
        return JsonResponse({'error': 'Invalid request'})

def success_view(request):
    if request.method == 'GET':
        # Extract payment details from query parameters
        payment_id = request.GET.get('razorpay_payment_id')
        order_id = request.GET.get('razorpay_payment_order_id')
        signature = request.GET.get('razorpay_payment_signature')

        # Store payment details in the database using the Payment model
        payment = PaymentModel.objects.create(  # Use PaymentModel instead of Payment
            payment_id=payment_id,
            order_id=order_id,
            signature=signature
        )

        # Render success template or redirect as needed
        return render(request, 'success.html', {'payment': payment})

def razorpay_callback(request):
    if request.method == 'POST':
        # Handle Razorpay callback
        data = request.POST
        razorpay_payment_id = data['razorpay_payment_id']
        razorpay_order_id = data['razorpay_order_id']
        razorpay_signature = data['razorpay_signature']
        # Verify the signature using your Razorpay secret key
        # Implement your own logic here to verify the payment and update your database accordingly
        return JsonResponse({'status': 'success'})
    else:
        return render(request, 'error.html')

def VisaRequiredDocuments(request):
    country_dropdown_data = []
    csv_file_path = 'C:\\Users\\ashme\\OneDrive\\Documents\\Minor Project\\MinorProject\\ToekomstPiano\\static\\Files\\visacountries.csv'

    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            country_dropdown_data.append({'value': row[0], 'label': row[1]})

    return render(request, 'VisaRequireDocuemnt.html', {'country_dropdown_data': country_dropdown_data})
    
# def h(request):
#     try:
#         # Get the user's email from the session
#         email = request.session.get('email')

#         # Fetch the profile picture data from the database
#         profile_pic_data = get_profile_pic(email, cursor)

#         # Check if profile_pic_data is not None
#         if profile_pic_data:
#             # Encode the profile picture data to base64
#             profile_pic = base64.b64encode(profile_pic_data).decode('utf-8')
#         else:
#             profile_pic = None

#         # Store the profile picture data in the session
#         request.session['profile_pic'] = profile_pic

#         return render(request, 'h.html')

#     except db.Error as e:
#         # Handle database errors
#         print(f"MySQL Error: {e}")

#     finally:
#         # Close cursor and database connection
#         if 'cursor' in locals() and cursor is not None:
#             cursor.close()
#         if 'conn' in locals() and conn is not None:
#             conn.close()


# def REGISTRATION_FORM(request):
#     global name, email, password, remember
#     try:
#         if request.method == "POST":
#             d = request.POST
#             for key, value in d.items():
#                 if key == 'name':
#                     name = value
#                 if key == 'Email':
#                     email = value
#                 if key == 'password':
#                     password = value
#             if name == '' and password == '' and email == '':
#                 return render(request, "Registration.html")
#             else:
#                 invite_code = code(name, email)
#                 sent_mail = send_email_to_client(name, email, invite_code)
#                 signup(email, password, t=1)
#     except ConnectionError:
#         print(ConnectionError)
#     return render(request, 'Registration.html')

# def USERHOME(request):
#     if request.method == 'POST':
#         theme_preference = request.POST.get('theme_preference')
#         email = request.POST.get('email')
#         try:
#             # Create or update theme preference in the database
#             ThemePreference.objects.update_or_create(
#                 email=email, defaults={'theme_preference': theme_preference})
#             return JsonResponse({'success': True})
#         except Exception as e:
#             print("Failed to store theme preference:", e)
#             return JsonResponse({'success': False, 'error': 'Failed to store theme preference'})
#     else:
#         username = request.session.get('username')
#         email = request.session.get('email')
#         invite_code = request.session.get('invite_code')
#         if not username:
#             return redirect(reverse('LOGIN'))
#         return render(request, "USERHOME.html", {'name': username, 'email': email, 'invite_code': invite_code})

# def Account(request):
#     try:
#         if request.method == 'POST' and request.FILES.get('image'):
#             # Handle image upload
#             image = request.FILES['image']
#             email = request.session.get('email')
#             saveprofilepic(image, email, cursor, conn)

#             # Redirect to a success page after handling the image upload
#             return redirect('/profile_saved')

#         # Get the user's email from the session
#         email = request.session.get('email')

#         # Fetch the profile picture data from the database
#         profile_pic_data = get_profile_pic(email, cursor)

#         # Check if profile_pic_data is not None
#         if profile_pic_data:
#             # Encode the profile picture data to base64
#             profile_pic = base64.b64encode(profile_pic_data).decode('utf-8')

#             # Store the profile picture data in the session
#             request.session['profile_pic'] = profile_pic
#         else:
#             profile_pic = None

#         # Pass the profile picture data to the template
#         return render(request, 'Account.html', {'profile_pic': profile_pic})

#     except db.Error as e:
#         # Handle database errors
#         print(f"MySQL Error: {e}")

#     finally:
#         # Close cursor and database connection
#         if 'cursor' in locals() and cursor is not None:
#             cursor.close()
#         if 'conn' in locals() and conn is not None:
#             conn.close()

# from django.contrib.sessions.models import Session
# from .utils import login, get_theme_preference,hash_password, get_theme_preference
# from .utils import store_theme_preference
# from .utils import preprocess_data
# from .ml_utils import get_profile_pic
# from django.core.mail import send_mail
# from .utils import get_profile_pic, saveprofilepic,verify_password,hash_password,code, send_email_to_client
# Global variables
