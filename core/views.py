from django.shortcuts import HttpResponse
import query_ini

def get_system(request):
    result = query_ini.main()
    return HttpResponse(str(result))
