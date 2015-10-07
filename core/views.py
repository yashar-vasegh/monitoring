from django.shortcuts import HttpResponse
import json
import query_ini


def get_system(request):
    result = query_ini.main()
    #result = {'record':[result]}
    response = HttpResponse(json.dumps(result))
    response["Access-Control-Allow-Origin"] = "*"
    return response
