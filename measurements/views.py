from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from .models import Measurement
import json
import datetime


@csrf_exempt
def measurements_view(request):
    """
    GET  /measurements?user_id=xxx[&start=ISO8601&end=ISO8601]  -> list items
    POST /measurements  JSON body:
        {
          "user_id": "demo-user",
          "sbp": 120,
          "dbp": 75,
          "hr": 70,
          "timestamp": "2025-08-29T23:15:00Z"
        }
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode())
            m = Measurement(
                user_id=data['user_id'],
                sbp=int(data['sbp']),
                dbp=int(data['dbp']),
                hr=int(data['hr']) if data.get('hr') is not None else None,
                timestamp=datetime.datetime.fromisoformat(
                    data['timestamp'].replace('Z', '+00:00')
                )
            )
            m.save()
            return JsonResponse({'ok': True, 'id': m.id}, status=201)
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)

    elif request.method == 'GET':
        user_id = request.GET.get('user_id')
        if not user_id:
            return JsonResponse({'ok': False, 'error': 'user_id required'}, status=400)

        qs = Measurement.objects.filter(user_id=user_id).order_by('-timestamp')

        start = request.GET.get('start')
        end = request.GET.get('end')
        if start:
            qs = qs.filter(timestamp__gte=parse_datetime(start))
        if end:
            qs = qs.filter(timestamp__lte=parse_datetime(end))

        items = [{
            'sbp': x.sbp, 'dbp': x.dbp, 'hr': x.hr,
            'timestamp': x.timestamp.isoformat().replace('+00:00','Z')
        } for x in qs[:500]]

        return JsonResponse({'ok': True, 'items': items}, status=200)

    return JsonResponse({'error': 'method not allowed'}, status=405)
