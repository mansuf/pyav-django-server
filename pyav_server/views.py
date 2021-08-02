import json
from django.http import HttpResponse, HttpRequest, JsonResponse, StreamingHttpResponse
from pyav import iter_av_packets

def produce_av_packets(r: HttpRequest):
    try:
        data = json.loads(r.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'not a json request'}, status=400)
    url = data.get('url')
    if not url:
        return JsonResponse({'error': 'No url supplied'}, status=400)
    format = data.get('format')
    if not format:
        return JsonResponse({'error': 'No format supplied'}, status=400)
    codec = data.get('codec')
    if not codec:
        return JsonResponse({'error': 'No codec supplied'}, status=400)
    rate = data.get('rate') or 44100
    if not isinstance(rate, int):
        return JsonResponse({'error': 'rate is not integer value'}, status=400)
    seek = data.get('seek')
    if seek:
        if not isinstance(seek, int):
            return JsonResponse({'error': 'seek is not integer value'}, status=400)
    try:        
        return StreamingHttpResponse(iter_av_packets(
            url,
            format,
            codec,
            rate,
            seek
        ))
    except Exception as e:
        return JsonResponse(
            {'error': '{0.__class__.__name__}: {1}'.format(e, str(e))}
        , status=500)