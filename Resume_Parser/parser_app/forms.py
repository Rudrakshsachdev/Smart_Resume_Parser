from django import forms 

class ResumeForm(forms.Form):
    full_name = forms.CharField(max_length = 100, label = 'Full Name')
    email = forms.CharField(max_length = 100, label = 'Email')
    phone = forms.CharField(label = 'Phone Number')
    summary = forms.CharField(widget = forms.Textarea, label = 'Summary')
    skills = forms.CharField(widget = forms.Textarea, label = 'Skills')
    education = forms.CharField(widget = forms.Textarea, label = 'Education')
    experience = forms.CharField(widget = forms.Textarea, label = 'Experience')
    projects = forms.CharField(widget = forms.Textarea, label = 'Projects')
    certifications = forms.CharField(widget = forms.Textarea, label = 'Certifications')

class JobMatcherForm(forms.Form):
    skills = forms.CharField(widget = forms.Textarea, label = 'Enter your skills (comma-separated)')


