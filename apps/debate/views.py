from django.http import JsonResponse
from apps.debate.main import run_debate

def test_debate(request):
    article = """Breaking News: Scientists Discover Water on Mars. 
    NASA announced today that their rover found liquid water."""
    
    result = run_debate(article, num_rounds=2)
    
    return JsonResponse(result)