from django.shortcuts import render, redirect # for rendering templates and redirecting users
from django.core.files.storage import FileSystemStorage # for handling file uploads
from pdfminer.high_level import extract_text as extract_pdf_text # for extracting text from PDF files
import docx # for handling DOCX files
import os # for handling file paths
from .resume_parser import parse_resume, score_resume # for parsing resumes and scoring them
from .models import Parsed_Resume # for saving parsed resumes to the database

from django.contrib.auth import authenticate, login, logout # for user authentication
from django.contrib.auth.models import User # for user model
from django.contrib import messages # for displaying messages to users
import random # for generating random OTPs
from django.core.mail import send_mail # for sending mails
from .models import TempUser # for storing temporary user data
import google.generativeai as genai # for using google gemini api
import json # for handling json data
from django.http import JsonResponse # for returning json responses
from django.conf import settings 
from django.views.decorators.csrf import csrf_exempt # for handling csrf tokens
import traceback # for handling exceptions and printing stack traces
from django.db import IntegrityError # for handling database integrity errors
from .forms import ResumeForm, JobMatcherForm
from .utils import generate_pdf # for generating pdf files
from django.http import HttpResponse


# Create your views here.

genai.configure(api_key = settings.GEMINI_API_KEY) # configuring the google gemini api with the api key from settings
@csrf_exempt # to exempt this view from csrf verification
def gemini_chatbot(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body) # parsing the json body of the request
            user_message = body.get('message') # getting the user message from the request body

            model = genai.GenerativeModel('gemini-1.5-pro') # initializing the gemini model
            response = model.generate_content(user_message) # generating content using the gemini api

            print('==== Response from Gemini API ====') # logging the response from the gemini api
            print(response) # printing the response to the console

            print("Response text: ", getattr(response, 'text', 'No text found'))

            ai_text = getattr(response, 'text', None) # getting the text from the response
            if not ai_text:
                return JsonResponse({
                    'response': 'No response from the AI model.'
                })
            
            return JsonResponse({
                'response': ai_text, # returning the response text from the gemini api
            })
        except Exception as e:
            print("Exception occurred: ")
            traceback.print_exc()
            return JsonResponse({
                'error': str(e), # returning the error message if any exception occurs
            }, status = 500) # returning a 500 status code for server error
    else:
        return JsonResponse({
            'error': 'Invalid request method.'
        }, status = 405) # returning a 405 status code for method not allowed

            




def extract_text_from_docx(file_path):
    doc = docx.Document(file_path) # opening the Docx file
    full_text = [] # initializing an empty list to store text

    # iterating through each paragraph in the document
    for para in doc.paragraphs:
        full_text.append(para.text) # appending the text of each paragraph to the list
    
    return '\n'.join(full_text) # joining the list into a single string with new lines



def homepage(request):
    extracted_text = None # to store the extracted text from the resume
    parsed_data = None # to store the parsed data from the resume

    # this block handles the POST request when a user uploads a resume file
    if request.method == 'POST':
        resume_file = request.FILES.get('resume_file')
        fs = FileSystemStorage()
        filename = fs.save(resume_file.name, resume_file)
        file_url = fs.url(filename)
        file_path = fs.path(filename)

        if filename.endswith('.pdf'):
            extracted_text = extract_pdf_text(file_path)
        elif filename.endswith('.docx'):
            extracted_text = extract_text_from_docx(file_path)
        else:
            extracted_text = "Unsupported file format! Please upload a PDF or DOCX file"

        if extracted_text and "Unsupported file format" not in extracted_text:
            parsed_data = parse_resume(extracted_text)
        else:
            parsed_data = {
                'name': "Not found",
                'email': "Not found",
                'phone': "Not found",
                'skills': [],
                'education': [],
                'experience': [],
                'projects': [],
                'certifications': []
            }

        # ⬇️ Score the resume
        resume_score, improvement_tips = score_resume(parsed_data)

        # ⬇️ Save to DB
        Parsed_Resume.objects.create(
            name=parsed_data['name'],
            email=parsed_data['email'],
            phone=parsed_data['phone'],
            skills=', '.join(parsed_data['skills']) if parsed_data['skills'] else None,
            education='\n'.join(parsed_data['education']) if parsed_data['education'] else None,
            experience='\n'.join(parsed_data['experience']) if parsed_data['experience'] else None,
            projects='\n'.join(parsed_data['projects']) if parsed_data['projects'] else None,
            certifications='\n'.join(parsed_data['certifications']) if parsed_data['certifications'] else None,
        )

        # Debug logs BEFORE return
        print("Extracted Text:\n", extracted_text)
        print("Parsed Data:\n", parsed_data)
        print("Score:", resume_score)
        print("Suggestions:", improvement_tips)

        return render(request, 'result.html', {
            'extracted_text': extracted_text,
            'file_url': file_url,
            **parsed_data,
            'resume_score': resume_score,
            'suggestions': improvement_tips
        })

    return render(request, 'homepage.html')


def generate_otp():
    return str(random.randint(100000, 999999)) # generating a random 6-digit OTP

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username = username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register')
        

        if TempUser.objects.filter(email = email).exists():
            messages.error(request, 'Email already registered! Please verify your account.')
            return redirect('register')
        
        otp = generate_otp() # generating an otp

        try:
            # save temporary user data
            TempUser.objects.create(
                username = username,
                email = email,
                password = password,
                otp = otp
            )

            # send otp to the users email
            send_mail(
                subject = 'Your OTP for Smart Resume Parser Registration',
                message = f'Your OTP is {otp}\n\nPlease use this OTP to complete your registration.',
                from_email = settings.EMAIL_HOST_USER,
                recipient_list = [email],
                fail_silently = False
            )

            request.session['email'] = email # storing email in session
            request.session['username'] = username
            request.session['otp'] = otp
            messages.success(request, 'OTP sent to your email! Please check your inbox.')
            return redirect('verify_otp')
        except IntegrityError:
            messages.error(request, 'An error occurred while processing your request. Please try again.')
            return redirect('register')
        
    return render(request, 'register_user.html')
        


        

def verify_otp(request):
    username = request.session.get('username')

    # check if username is not None
    if not username:
        messages.error(request, 'Session expired! Please register again.')
        return redirect('register')
    
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        temp_user = TempUser.objects.filter(username = username).first() # fetching the temporary user data

        # checking if the temp user exists and the entered otp matches the stored otp
        if temp_user and entered_otp == temp_user.otp:
            # creating the user in the User model
            user = User.objects.create_user(
                username = temp_user.username, 
                email = temp_user.email,
                password = temp_user.password
            )

            temp_user.delete() # deleting the temp user data
            messages.success(request, 'Registration Successful! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid OTP! Please try again.')
            
    return render(request, 'verify_otp.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successful!')
            return redirect('homepage')
        else:
            messages.error(request, 'Invalid credentials! Please try again.')
            return redirect('login')
    
    return render(request, 'login_user.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')


def help_page(request):
    return render(request, 'help.html')

    
def resume_builder(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST) # creating a form instance with the POST data
        

        if form.is_valid():
            data = form.cleaned_data
            request.session['resume_data'] = data # storing the cleaned data in session
            skills_list = [skill.strip() for skill in data['skills'].split(',')] # splitting skills by comma and stripping whitespace
            return render(request, 'resume_preview.html', {
                'data': data, # passing the cleaned data to the template
                'skills_list': skills_list, # passing the skills list to the template
            })
    else:
        form = ResumeForm() 
    
    return render(request, 'resume_builder.html', {
        'form': form,
    })

        
        
def download_resume_pdf(request):
    data = request.session.get('resume_data')
    if not data:
        return HttpResponse('No resume data found.', )

    skills_list = [s.strip() for s in data.get('skills', '').split(',')] # splitting skills by comma and stripping whitespaces

    # this context dictionary will be used to render the template
    context = {
        'data': data,
        'skills_list': skills_list,
    }

    return generate_pdf('resume_preview.html', context)


# sample job data

JOB_DATABASE = [
    {
        'title': 'Software Engineer',
        'skills': ['Python', 'Java', 'Django']
    },
    {
        'title': 'Data Scientist',
        'skills': ['Python', 'Machine Learning', 'Statistics']
    },
    {
        'title': 'Product Manager',
        'skills': ['Agile', 'Scrum', 'Product Development']
    },
    {
        'title': 'Web Developer',
        'skills': ['HTML', 'CSS', 'JavaScript']
    },
    {
        'title': 'DevOps Engineer',
        'skills': ['Docker', 'Kubernetes', 'AWS']
    },
    {
        'title': 'Mobile App Developer',
        'skills': ['React Native', 'Flutter', 'Swift']
    },
    {
        'title': 'Database Administrator',
        'skills': ['SQL', 'NoSQL', 'Database Management']
    },
    {
        'title': 'Cybersecurity Analyst',
        'skills': ['Network Security', 'Penetration Testing', 'Risk Assessment']
    },
    {
        'title': 'UI/UX Designer',
        'skills': ['Figma', 'Adobe XD', 'User Research']
    },
    {
        'title': 'Cloud Engineer',
        'skills': ['Azure', 'Google Cloud', 'Cloud Architecture']
    }
]

def job_matcher(request):
    matched_jobs = [] # for storing the matched jobs
    form = JobMatcherForm()

    # this block handles the POST request when a user submits their skills
    if request.method == 'POST':
        form = JobMatcherForm(request.POST) # creating a form instance with the POST data

        if form.is_valid():
            user_skills = [skill.lower().strip() for skill in form.cleaned_data['skills'].split(',')] # splitting skills by comma and stripping white spaces

            # iterating through the job database to find matching jobs
            for job in JOB_DATABASE:
                job_skills = [s.lower() for s in job['skills']] # converting to lowercase for case-insensitve comparison

                match_score = len(set(user_skills) & set(job_skills)) # calculating the match score based on common skills

                # if match score is greater than 0, add the job to the matched jobs list
                if match_score > 0:
                    matched_jobs.append({
                        'title': job['title'],
                        'match_score': match_score,
                        'required_skills': job['skills']     
                    })
            # sorting the matched jobs by match score in descending order
            matched_jobs = sorted(matched_jobs, key=lambda x: x['match_score'], reverse=True)
    
    return render(request, 'job_matcher.html', {
        'form': form,
        'matched_jobs': matched_jobs
    })