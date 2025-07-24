from django.template.loader import get_template # for getting the templates
from xhtml2pdf import pisa # for converting html to pdf
from io import BytesIO # for handling byte streams
from django.http import HttpResponse 

def generate_pdf(template_src, context_dict):
    """
    Generates a PDF from a template and context dictionary.
    
    Args:
        template_src (str): The path to the template file.
        context_dict (dict): The context dictionary to render the template with.
    
    Returns:
        HttpResponse: A response object containing the gnerated PDF.
    """

    template = get_template(template_src) # load the template
    html = template.render(context_dict) # render the template with the context
    result = BytesIO() # creating a byte stream to hold the PDF data
    pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result) # converting the html to pdf

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf') # return the PDF as a response
    else:
        return None
    
    