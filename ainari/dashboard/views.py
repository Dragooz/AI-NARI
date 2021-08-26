from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, 'dashboard/homepage.html')

def test(request):
    return render(request, 'dashboard/index.html')
