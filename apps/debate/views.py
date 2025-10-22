from django.http import JsonResponse
from apps.debate.tasks import run_debate_async
from celery.result import AsyncResult

def test_debate(request):
    article = """Source: The Guardian

Headline: Israel will disarm Hamas and demilitarise Gaza, says Netanyahu
Summary: Israeli Prime Minister Benjamin Netanyahu announced plans to disarm Hamas and demilitarize the Gaza Strip during a speech to the Knesset. This aligns with a broader ceasefire and peace strategy involving U.S. support. However, the ceasefire has faced challenges, including alleged violations and ongoing humanitarian concerns."""

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
