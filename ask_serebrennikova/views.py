from django.http import HttpResponse

def helloworld(request):
    response = "<html>Django`s \"Hello,World\"<br><br>GET:<br>"
    for key in request.GET.keys():
	response += key + " = "
        for param in request.GET[key]:
            response += param
        response += "<br>"
    response += "<br>POST:"
    for key in request.POST.keys():
	response += key + " = "
        for param in request.POST[key]:
            response += param
        response += "<br>"
    response += "</html>"
    return HttpResponse(response)
