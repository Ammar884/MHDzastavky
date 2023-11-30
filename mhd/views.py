from django.shortcuts import render

def index(request):
	name = request.GET.get("name")
	return render(request, "index.html", {"name": name})
