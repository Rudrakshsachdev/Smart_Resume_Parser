import spacy # for natural language processing
import re # for handling regular expressions
import calendar
from spacy.matcher import PhraseMatcher # for matching patterns in text

nlp = spacy.load('en_core_web_sm') # loading the English language model for handling text processing

SKILLS = [
    "Python", "Java", "C++", "JavaScript", "SQL", "HTML", "CSS",
    "Machine Learning", "Data Analysis", "Deep Learning", "TensorFlow",
    "Django", "Flask", "React", "Node.js", "Scikit-learn", "Pandas",
    "NumPy", "Keras", "PyTorch", "Matplotlib", "Seaborn", "C", "R",
    "Git", "Docker", "Kubernetes", "AWS", "Azure", "Google Cloud",
    "Agile", "Scrum", "DevOps", "CI/CD", "RESTful APIs", "DSA",
    "Algorithms", "Problem Solving", "Communication", "Teamwork", "Leadership",
    "Time Management", "Critical Thinking", "Adaptability", "Creativity",
    "Database Management", "Software Development", "Web Development", "Mobile Development",
    "Cloud Computing", "Cybersecurity", "Networking", "Virtualization", "Big Data",
    "Artificial Intelligence", "Natural Language Processing", "Computer Vision", "Robotics",
    "Blockchain", "IoT", "Edge Computing", "Quantum Computing", "Augmented Reality",
    "Virtual Reality", "Game Development", "UI/UX Design", "C#", "PHP",
    "Swift", "Go", "Rust", "Scala", "Perl", "TypeScript",
    "GraphQL", "NoSQL", "PostgreSQL", "MongoDB", "Redis", "Elasticsearch"
]


def clean_section_lines(lines):
    cleaned = [] # an empty list to store cleaned lines
    current = "" # a variable to store the current line being processed

    # iterating through each line in the input lines
    for line in lines:
        line = line.strip() # removing leading whitespaces
        
        if not line:
            continue # skipping empty lines

        
        # checking if the line starts with a bullet point or dash or asterisk
        if not line.startswith("•") and not line.startswith("-") and not line.startswith("*"):

            if current: # if current is not empty, append it to the cleaned list
                cleaned.append(current.strip()) # appending the current line to the cleaned list if it is not empty
            
            # resetting the current line to the new line
            current = line
        else:
            # continuation of the previous item
            current += '\n' + line

    if current:
        cleaned.append(current.strip()) # appending the last current line to the cleaned list if it is not empty
    
    return list({entry for entry in cleaned if entry}) # returning a list of unique cleaned lines


def extract_name(text):
    lines = text.strip().splitlines() # splitting the text into lines and stripping leading/trailing whitespaces

    # First, checking the first 5 non-empty lines for a likely name
    for line in lines:
        line = line.strip() # stripping leading/trailing whitespaces
        if not line:
            continue # skipping empty lines

        # checking if the line looks like a name
        if (
            2 <= len(line.split()) <= 4 and                # Looks like a name (2–4 words)
            line[0].isupper() and                          # Starts with a capital letter
            all(w[0].isupper() for w in line.split() if w) # Each word starts uppercase
        ):
            return line  # likely a full name

    # fallback to spaCy NER
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == 'PERSON' and 2 <= len(ent.text.split()) <= 4:
            return ent.text.strip()

    return "Not Found"



def extract_email(text):
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" # regex pattern for matching email addresses
    match = re.findall(pattern, text) # searching for the pattern in the text
    
    return match[0] if match else None # returning the first matched email address if found, otherwise returning none


def extract_phone(text):
    pattern = r"(\+91[\-\s]?)?[6-9]\d{9}" # regex pattern for matching Indian Phone numbers
    match = re.search(pattern, text) # searching for the pattern in the text
    if match:
        return match.group(0) # returning the matched phone number
    else:
        return None



def extract_skill(text):
    lines = text.splitlines()
    skills_section = []
    capture = False

    # Step 1: Extract just the Skills section
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.search(r'\bSkills\b', line, re.IGNORECASE):
            capture = True
            continue
        elif capture and re.search(r'\b(Education|Experience|Projects|Certifications|Achievements|Internship)\b', line, re.IGNORECASE):
            break
        elif capture:
            skills_section.append(line)

    # Step 2: Match skills ONLY from skills_section with proper word boundaries
    found_skills = set()
    skill_text = ' '.join(skills_section)

    # Sort skills by length (descending) to match longer skills first
    # This prevents "Java" from being matched when "JavaScript" is present
    sorted_skills = sorted(SKILLS, key=len, reverse=True)

    for skill in sorted_skills:
        # Use word boundaries to avoid partial matches
        # Handle special cases for skills with special characters
        if skill.lower() in ['c++', 'c#', 'f#']:
            # For skills with special characters, use exact match
            pattern = r'\b' + re.escape(skill) + r'\b'
        elif skill.lower() in ['c']:
            # Special case for "C" to avoid matching "C++" or "C#"
            pattern = r'\b' + re.escape(skill) + r'\b(?!\+|#)'
        else:
            # For regular skills, use word boundaries
            pattern = r'\b' + re.escape(skill) + r'\b'
        
        if re.search(pattern, skill_text, re.IGNORECASE):
            found_skills.add(skill)

    print("📌 Skills Section Extracted:\n", skills_section)
    print("✅ Matched Skills:\n", found_skills)

    return sorted(found_skills) if found_skills else ["Not found"]


    

def extract_education(text):
    # education_keywords = [
    #     'B.Tech', 'Bachelor', 'Master', 'M.Tech', 'B.E', 'B.Sc', 'M.Sc',
    #     'Diploma', 'University', 'College', 'Computer Science', 'Engineering',
    #     'Information Technology', 'IT', 'Electronics', 'Electrical', 'Mechanical',
    #     'Civil', 'Chemical', 'Biotechnology', 'Data Science', 'Artificial Intelligence',
    #     'Machine Learning', 'MBA', 'Management', 'Business Administration',
    #     'Bachelor of Technology', 'Bachelor of Engineering', 'Bachelor of Science',
    #     'Master of Technology', 'Master of Science', 'Master of Business Administration',
    #     'Graduation', 'Post Graduation', 'Undergraduate', 'Graduate', 'Postgraduate',
    #     'Academic', 'Academic Qualifications', 'Academic Background', 'Academic History',
    #     'Academic Achievements', 'Academic Records', 'Academic Credentials',
    #     'Academic Performance', 'Academic Excellence', 'Academic Awards', 'Academic Honors',
    #     'Academic Distinctions', 'Academic Degrees', 'Academic Certifications',
    #     'Academic Courses', 'Academic Programs', 'Academic Institutions',
    #     'Bachelor of Arts', 'Bachelor of Commerce', 'Bachelor of Business Administration',
    #     'Master of Arts', 'Master of Commerce', 'Master of Business Studies',
    #     'Master of Computer Applications', 'MCA', 'Bachelor of Computer Applications',
    #     'BCA', 'Bachelor of Information Technology', 'BIT', 'Master of Information Technology',
    #     'MIT', 'Bachelor of Design', 'B.Des', 'Master of Design', 'M.Des',
    #     'Bachelor of Fine Arts', 'BFA', 'Master of Fine Arts', 'MFA', 'PhD',
    #     'Doctor of Philosophy', 'Doctorate', 'Doctoral Degree', 'Thesis', 'Dissertation',
    #     'Research', 'Research Work', 'Thesis Work', 'Dissertation Work', 'Thesis Defense',
    #     'Dissertation Defense', 'Thesis Submission', 'Dissertation Submission',
    #     'Thesis Proposal', 'Dissertation Proposal', 'Thesis Research', 'Dissertation Research',
    #     'Thesis Writing', 'Dissertation Writing', 'Thesis Publication', 'Dissertation Publication'
    # ]

    lines = text.splitlines() # splitting the text into lines

    education_section = [] # an empty list to store education-related lines

    capture = False # flag to capture lines after the education keyword

    # iterating through each line in the text

    for line in lines:
        # checking if the line contains any education-related keywords
        if re.search(r'\bEducation\b', line, re.IGNORECASE):
            capture = True # flag to capture lines after the education keyword
            continue # skipping the line with the education keyword
        elif capture and re.search(r'\b(Experience|Projects|Certifications|Skills)\b', line, re.IGNORECASE):
            break # breaking the loop if we reach a new section after capturing education lines
        elif capture: # this condition is true if we are in the education section
            if line.strip(): # checking if the line is not empty
                education_section.append(line.strip()) 

    return education_section if education_section else None # returning the education section if found, otherwise returning None  



def extract_experience(text):
    # experience_keywords = [
    #     "experience", "work experience", "professional experience", "employment history",
    #     "job history", "career history", "previous employment", "past employment",
    #     "work history", "job experience", "professional background", "career background",
    #     "roles and responsibilities", "job roles", "job responsibilities", "work roles",
    #     "work responsibilities", "job duties", "work duties", "job tasks", "work tasks",
    #     "achievements", "accomplishments", "projects", "projects undertaken",
    #     "projects completed", "project management", "project lead", "project coordinator",
    #     "team lead", "team member", "collaboration", "collaborative work",
    #     "cross-functional team", "interdepartmental collaboration", "cross-functional collaboration",
    #     "teamwork", "team player", "leadership", "mentorship", "coaching",
    #     "supervision", "management", "project management", "program management",
    #     "product management", "business analysis", "data analysis", "market research",
    #     "customer service", "client management", "stakeholder management", "vendor management",
    #     "sales", "marketing", "business development", "account management",
    #     "customer relationship management", "CRM", "salesforce", "lead generation",
    #     "leadership", "team management", "people management", "resource management",
    #     "budget management", "financial management", "cost management", "risk management",
    #     "quality management", "process improvement", "continuous improvement", "lean", "six sigma",
    #     "agile", "scrum", "kanban", "waterfall", "project lifecycle", "project planning", "project execution",
    #     "project monitoring", "project control", "project closure", "project reporting",
    #     "project documentation", "project deliverables", "project milestones", "project timelines",
    #     "project scope", "project requirements", "project objectives", "project goals",
    #     "project success", "project outcomes", "project results", "project impact",
    #     "project benefits", "project value", "project ROI", "project KPIs",
    #     "project metrics", "project performance", "project evaluation", "project review",
    #     "project feedback", "project lessons learned", "project best practices", "project challenges"
    # ]

    lines = text.splitlines() # splitting the text into lines

    experience_section = [] # an empty list to store experience-related lines

    capture = False # flag to capture lines after the experience keyword

    # iterating through each line in the text
    for line in lines:
        # checking if the line containes any experience-related keywords

        if re.search(r'\bExperience\b', line, re.IGNORECASE):
            capture = True # flag to capture lines after the experience keyword
            continue
        elif capture and re.search(r'\b(Projects|Certifications|Skills|Education)\b', line, re.IGNORECASE):
            break # breaking the loop if we reach a new section after capturing experience lines
        elif capture:
            if line.strip(): 
                experience_section.append(line.strip())
    
    return clean_section_lines(experience_section) if experience_section else None # returning the experience section if found, otherwise returning None




def extract_projects(text):
    # project_keywords = [
    #     "project", "projects", "project management", "project lead", "project coordinator",
    #     "project execution", "project planning", "project monitoring", "project control",
    #     "project closure", "project deliverables", "project milestones", "project timelines",
    #     "project scope", "project requirements", "project objectives", "project goals",
    #     "project success", "project outcomes", "project results", "project impact",
    #     "project benefits", "project value", "project ROI", "project KPIs",
    #     "project metrics", "project performance", "project evaluation", "project review",
    #     "project feedback", "project lessons learned", "project best practices"
    # ]

    lines = text.split('\n') # splitting the text into lines
    project_section = [] # an empty list to store project related lines
    capture = False # flag to capture lines after the project keyword
    
    # iterating through each line in the text
    for line in lines:
        # checking if the line contains any project-related keywords
        if re.search(r'\bProjects\b', line, re.IGNORECASE):
            capture = True 
            continue # flag to capture lines after the project keyword
        elif capture and re.search(r'\b(Certifications|Skills|Experience|Education)\b', line, re.IGNORECASE):
            break # breaking the loop if we reach a new section after capturing project lines
        elif capture:
            if line.strip():
                project_section.append(line.strip()) # appending the line to the project section if it is not empty
        
    return list(set(clean_section_lines(project_section))) if project_section else None # returning the project section if found, otherwise returning None
    


def extract_certifications(text):
    # certifcation_keywords = [
    #     "certification", "certified", "certifications", "certified in", "certified as",
    #     "professional certification", "industry certification", "technical certification",
    #     "certification program", "certification course", "certification exam",
    #     "certification training", "certification workshop", "certification seminar",
    #     "certification conference", "certification event", "certification badge",
    #     "certification credential", "certification license", "certification authority",
    #     "certification body", "certification organization", "certification institute",
    #     "accredited certification", "recognized certification", "approved certification",
    #     "valid certification", "current certification"
    # ]

    lines = text.splitlines() 
    certification_section = []
    capture = False

    for line in lines:
        
        if re.search(r'\bCertifications\b', line, re.IGNORECASE):
            capture = True
            continue
        elif capture and re.search(r'\b(Projects|Skills|Experience|Education)\b', line, re.IGNORECASE):
            break
        elif capture:
            if line.strip():
                certification_section.append(line.strip())
    return clean_section_lines(certification_section) if certification_section else None # returning the certification section if found, otherwise returning None


def parse_resume(text):


    # text = clean_section_lines(text.splitlines()) # cleaning the resume text by removing unnecessary lines
    # text = '\n'.join(text) # joining the cleaned lines back into a single string
    name = extract_name(text) # extracting the name from the resume text
    email = extract_email(text) # extracting the email from the resume text
    phone = extract_phone(text) # extracting the phone number from the resume text
    print("NAME:", name)
    print("EMAIL:", email)
    print("PHONE:", phone)
    # main function to parse the resume text and extract relevant infoormation
    return {
        'name': extract_name(text),
        'email': extract_email(text),
        'phone': extract_phone(text),
        'skills': extract_skill(text),
        'education': extract_education(text),
        'experience': extract_experience(text),
        'projects': extract_projects(text),
        'certifications': extract_certifications(text)
    }


def score_resume(parsed_data):
    score = 0 # initializing the score to 0
    suggestions = [] # an empty list to store suggestions for improvement

    skill_count = len(parsed_data.get('skills', [])) # getting the number of skills extracted from the resume

    if skill_count >= 10:
        score += 25 # adding 25 points if the resume has 10 or more skills
    elif skill_count >= 5:
        score += 15
    else:
        score += 5
        suggestions.append("Consider adding more skills to you resume.")
    

    if parsed_data.get('projects'):
        score += 20 # adding 20 points if the resume has projects listed
        
        if len(parsed_data['projects']) < 2:
            suggestions.append("Consider adding more projects to showcase you work.")
    else:
        suggestions.append("Consider adding a projects section to highlight your work.")

    if parsed_data.get('certifications'):
        score += 15 # adding 15 points if the resume has ceritifications listed
    else:
        suggestions.append("Consider adding certifications to enhance your qualifications.")
        
    if parsed_data.get('education'):
        score += 15 # adding 15 points if the resume has education listed
    else:
        suggestions.append("Consider adding an education section to your resume.")
    
    if parsed_data.get('experience'):
        score += 15
    else:
        suggestions.append("Consider adding an experience section to your resume.")
    
    if parsed_data.get('name') and parsed_data.get('email') and parsed_data.get('phone'):
        score += 10
    else:
        suggestions.append("Ensure your contact information is complete with name, email, and phone number.")
    
    return min(score, 100), suggestions # returning the final score and suggestions for improvement, ensuring the score does not exceed 100