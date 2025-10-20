from django.http import JsonResponse
from apps.debate.tasks import run_debate_async
from celery.result import AsyncResult

def test_debate(request):
    article = """Breaking News: Scientists Discover Water on Mars.
    NASA announced today that their rover found liquid water beneath
    the surface of Mars."""

    task = run_debate_async.delay(article, num_rounds=2)

    return JsonResponse({
        'status': 'queued',
        'task_id': str(task.id),
        'check_status_url': f'/debate/status/{task.id}/'
    })

def check_debate_status(request, task_id):
    task = AsyncResult(str(task_id))

    if task.state == 'PENDING':
        return JsonResponse({'status': 'pending'})
    elif task.state == 'PROGRESS':
        return JsonResponse({
            'status': 'in_progress',
            **task.info
        })
    elif task.state == 'SUCCESS':
        return JsonResponse({
            'status': 'completed',
            'result': task.result
        })
    elif task.state == 'FAILURE':
        return JsonResponse({
            'status': 'failed',
            'error': str(task.info)
        })
    else:
        return JsonResponse({'status': task.state.lower()})
