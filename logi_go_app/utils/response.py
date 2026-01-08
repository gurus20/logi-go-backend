from django.http import JsonResponse

def api_response(success, message, data=None, status=200):
    return JsonResponse(
        {
            "success": success,
            "message": message,
            "data": data,
        },
        safe=False,
        status=status,
    )