from django.shortcuts import render

from django.shortcuts import render, redirect  
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from sampleapp.forms import EmployeeForm  
from sampleapp.models import Employee  
 
# Create your views here.  
def addnew(request):  
    if request.method == "POST":  
        form = EmployeeForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/')  
            except:  
                pass
    else:  
        form = EmployeeForm()  
    return render(request,'index.html',{'form':form})  
 
def index(request):  
    employees = Employee.objects.all()  
    return render(request,"show.html",{'employees':employees})  
 
def edit(request, id):  
    employee = Employee.objects.get(id=id)  
    return render(request,'edit.html', {'employee':employee})  
 
def update(request, id):  
    employee = Employee.objects.get(id=id)  
    form = EmployeeForm(request.POST, instance = employee)  
    if form.is_valid():  
        form.save()  
        return redirect("/")  
    return render(request, 'edit.html', {'employee': employee})  
     
def destroy(request, id):  
    employee = Employee.objects.get(id=id)  
    employee.delete()  
    return redirect("/")  

def generate_pdf(request):
    # Fetch all records from the database
    items = Employee.objects.all()
    
    # Get the template
    template_path = 'pdf_template.html'
    
    # Create context dictionary with your data
    context = {
        'items': items,
    }
    
    # Load the template
    template = get_template(template_path)
    html = template.render(context)
    
    # Create a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    
    # Create PDF
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    
    # If error then return some error
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    
    return response