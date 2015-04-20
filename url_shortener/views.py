from django.shortcuts import render
from models import Url
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden
import urllib

# Create your views here.

@csrf_exempt
def main(request):
    host = request.META['HTTP_HOST']

    if request.method == "GET":
        output = ("<form action='/' method='POST'>\n"
                + "Introduce your url:"
                + "<input type='text' name='url'/></br>\n"
                + "<input type='submit' value='Submit' "
                + "/></form>\n<br>\n<br>"
                + str(Url.objects.values_list()))

    elif request.method == "POST":
        urlname = urllib.unquote(request.body.split("=")[1])
        if (not urlname.startswith("http://") 
                and not urlname.startswith("https://")):
            urlname = "http://" + urlname

        try:
            urlname = Url.objects.get(url=urlname).url
        except Url.DoesNotExist:
            new_entry = Url(url=urlname)
            new_entry.save()

        urlnum = Url.objects.get(url=urlname).id
        output = ("You introduced: " + str(urlname) + "</br>\n"
                + "The abbreviation is: /" + str(urlnum) + "</br>\n"
                + "<meta http-equiv='Refresh' content='2;"
                + "url=http://" + host + "'>")
    else:
        return HttpResponseForbidden("Method not allowed")

    return HttpResponse(output)

def redirect(request, resource):
    try:
        if request.method == "GET":
            shortened = Url.objects.get(id=resource).url
            output = ("<meta http-equiv='refresh'"
                    + "content='0;" + " url="
                    + shortened + "' />")
            return HttpResponse(output)
        else:
            return HttpResponseForbidden("Method not allowed")
    except Url.DoesNotExist:
        return HttpResponseNotFound("Not existent shortened url")


    
    