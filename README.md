# 🚀 Smart Resume Parser

A powerful Django-based web application that intelligently parses, analyzes, and scores resumes while providing AI-powered insights and recommendations.

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### 🔍 **Resume Parsing**

- **Multi-format Support**: Parse PDF and DOCX resume files
- **Intelligent Extraction**: Extract key information including:
  - Personal details (Name, Email, Phone)
  - Skills and technical competencies
  - Education background
  - Work experience
  - Projects
  - Certifications

### 📊 **Resume Scoring & Analysis**

- **Smart Scoring Algorithm**: Comprehensive scoring based on:
  - Skills diversity (up to 25 points)
  - Project portfolio (up to 20 points)
  - Certifications (up to 15 points)
  - Education background (up to 15 points)
  - Work experience (up to 15 points)
  - Contact information completeness (up to 10 points)
- **Personalized Suggestions**: AI-powered recommendations for resume improvement

### 🤖 **AI-Powered Features**

- **Gemini Chatbot Integration**: Get instant answers about resume optimization
- **Job Matching**: Match resumes against job descriptions
- **Resume Builder**: AI-assisted resume creation tool

### 👤 **User Management**

- **Secure Authentication**: User registration and login system
- **OTP Verification**: Email-based account verification
- **Session Management**: Secure user sessions

### 📄 **Additional Tools**

- **PDF Generation**: Export parsed data and recommendations as PDF
- **Resume Builder**: Create professional resumes with guided assistance
- **Job Matcher**: Compare resumes against job requirements

## 🛠️ Technology Stack

### **Backend**

- **Django 5.2.4**: Web framework
- **Python 3.x**: Programming language
- **SQLite**: Database (development)
- **Regex & NLP**: Text parsing and pattern matching

### **AI & Machine Learning**

- **Google Gemini AI**: Chatbot and content generation
- **spaCy**: Natural language processing
- **Custom ML Models**: Resume scoring algorithms

### **File Processing**

- **pdfminer**: PDF text extraction
- **python-docx**: DOCX file processing
- **django.core.files**: File upload handling

### **Frontend**

- **HTML5 & CSS3**: User interface
- **JavaScript**: Interactive features
- **Bootstrap**: Responsive design

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/Rudrakshsachdev/Smart_Resume_Parser.git
cd Smart_Resume_Parser
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv myenv
myenv\Scripts\activate

# macOS/Linux
python3 -m venv myenv
source myenv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install django
pip install pdfminer.six
pip install python-docx
pip install spacy
pip install google-generativeai
pip install reportlab  # for PDF generation
```

### Step 4: Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

### Step 5: Environment Configuration

Create a `.env` file in the `Resume_Parser` directory:

```env
SECRET_KEY=your_django_secret_key_here
GEMINI_API_KEY=your_google_gemini_api_key
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEBUG=True
```

### Step 6: Database Setup

```bash
cd Resume_Parser
python manage.py makemigrations
python manage.py migrate
```

### Step 7: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Step 8: Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser to access the application.

## 📱 Usage

### 1. **Upload Resume**

- Navigate to the homepage
- Upload a PDF or DOCX resume file
- View extracted information and analysis

### 2. **Resume Analysis**

- Get comprehensive scoring based on multiple criteria
- Receive personalized improvement suggestions
- View detailed breakdown of extracted sections

### 3. **AI Chatbot**

- Ask questions about resume optimization
- Get instant feedback and recommendations
- Powered by Google Gemini AI

### 4. **Job Matching**

- Upload both resume and job description
- Get compatibility analysis
- Receive tailored suggestions for improvement

### 5. **Resume Builder**

- Create professional resumes with guided assistance
- Export as PDF format
- AI-powered content suggestions

## 📁 Project Structure

```
Smart_Resume_Parser/
├── myenv/                          # Virtual environment
├── Resume_Parser/                  # Main Django project
│   ├── manage.py                   # Django management script
│   ├── db.sqlite3                  # Database file
│   ├── media/                      # Uploaded files
│   ├── Resume_Parser/              # Project settings
│   │   ├── settings.py             # Django settings
│   │   ├── urls.py                 # URL configuration
│   │   └── wsgi.py                 # WSGI configuration
│   └── parser_app/                 # Main application
│       ├── models.py               # Database models
│       ├── views.py                # View functions
│       ├── urls.py                 # App URL patterns
│       ├── forms.py                # Django forms
│       ├── resume_parser.py        # Core parsing logic
│       ├── utils.py                # Utility functions
│       ├── templates/              # HTML templates
│       ├── static/                 # CSS, JS, images
│       └── migrations/             # Database migrations
└── README.md                       # Project documentation
```

## 🔗 API Endpoints

| Endpoint                | Method   | Description                 |
| ----------------------- | -------- | --------------------------- |
| `/`                     | GET      | Homepage with resume upload |
| `/register/`            | POST     | User registration           |
| `/verify-otp/`          | POST     | OTP verification            |
| `/login/`               | POST     | User login                  |
| `/logout/`              | GET      | User logout                 |
| `/chatbot/`             | POST     | AI chatbot interaction      |
| `/job-matcher/`         | POST     | Job matching analysis       |
| `/resume-builder/`      | GET/POST | Resume building tool        |
| `/download-resume-pdf/` | GET      | Download generated resume   |
| `/help/`                | GET      | Help and documentation      |

## 🎯 Core Features Breakdown

### Resume Parsing Engine

The `resume_parser.py` module contains sophisticated algorithms for:

- **Name Extraction**: Using regex patterns and spaCy NER
- **Contact Information**: Email and phone number detection
- **Skills Matching**: Word boundary matching with 60+ predefined skills
- **Section Identification**: Education, Experience, Projects, Certifications
- **Data Cleaning**: Removing noise and formatting inconsistencies

### Scoring Algorithm

The scoring system evaluates resumes based on:

```python
# Scoring Criteria:
- Skills (5-25 points): Based on quantity and relevance
- Projects (0-20 points): Presence and quantity of projects
- Certifications (0-15 points): Professional certifications
- Education (0-15 points): Educational background
- Experience (0-15 points): Work experience
- Contact Info (0-10 points): Completeness of contact details
```

### AI Integration

- **Google Gemini API**: Powers the chatbot and content generation
- **Natural Language Processing**: Advanced text analysis and understanding
- **Contextual Responses**: Intelligent, context-aware recommendations

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add comments for complex logic
- Update documentation for new features
- Test thoroughly before submitting

## 📧 Contact

**Developer**: Rudraksh Sachdev
**Email**: [Your Email]
**GitHub**: [@Rudrakshsachdev](https://github.com/Rudrakshsachdev)

## 🙏 Acknowledgments

- Django community for the excellent framework
- Google for Gemini AI API
- spaCy team for NLP capabilities
- All contributors and testers

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

⭐ **Star this repository if you find it helpful!**

Made with ❤️ by [Rudraksh Sachdev](https://github.com/Rudrakshsachdev)
