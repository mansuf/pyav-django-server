import json
from django.http import HttpResponse, HttpRequest, JsonResponse
from pyav import iter_av_pcm_packets, iter_av_opus_packets

def pcm(r: HttpRequest):
    try:
        data = json.loads(r.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'not a json request'}, status=400)
    url = data.get('url')
    if not url:
        return JsonResponse({'error': 'No url supplied'}, status=400)
    try:        
        return HttpResponse(iter_av_pcm_packets(url))
    except Exception as e:
        return JsonResponse(
            {'error': '{0.__class__.__name__}: {1}'.format(e, str(e))}
        , status=500)

def opus(r: HttpRequest):
    try:
        data = json.loads(r.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'not a json request'}, status=400)
    url = data.get('url')
    if not url:
        return JsonResponse({'error': 'No url supplied'}, status=400)
    try:        
        return HttpResponse(iter_av_opus_packets(url))
    except Exception as e:
        return JsonResponse(
            {'error': '{0.__class__.__name__}: {1}'.format(e, str(e))}
        , status=500)