from celery import shared_task
from apps.debate.crew import DebateCrew
import json
import time

def extract_json(raw_text):
    """Extract and parse JSON from various formats"""
    raw_text = raw_text.strip()
    
    if "```json" in raw_text:
        raw_text = raw_text.split("```json")[1].split("```")[0]
    elif "```" in raw_text:
        parts = raw_text.split("```")
        if len(parts) >= 3:
            raw_text = parts[1]
    
    start = raw_text.find('{')
    end = raw_text.rfind('}') + 1
    if start != -1 and end > start:
        raw_text = raw_text[start:end]
    
    return json.loads(raw_text)

@shared_task(bind=True, max_retries=3)
def run_debate_async(self, article_text, context="", num_rounds=2):
    try:
        full_article = article_text
        
        MAX_DEBATE_ARTICLE = 1200
        article_for_debate = (
            article_text[:MAX_DEBATE_ARTICLE] + "...[truncated]"
            if len(article_text) > MAX_DEBATE_ARTICLE
            else article_text
        )

        conversation = []
        opposer_last_argument = "No previous opposition"
        defender_current_argument = ""
        
        self.update_state(state='PROGRESS', meta={'stage': 'debate_starting', 'progress': 0})

        for round_num in range(1, num_rounds + 1):
            progress = int((round_num / (num_rounds + 1)) * 80)
            self.update_state(
                state='PROGRESS',
                meta={
                    'stage': f'round_{round_num}',
                    'progress': progress,
                    'current_round': round_num,
                    'total_rounds': num_rounds
                }
            )

            if conversation:
                recent_rounds = conversation[-2:]
                conversation_context = "\n\n".join([
                    f"Round {r['round']}:\n"
                    f"DEFENDER: {r['defender']}\n"
                    f"OPPOSER: {r['opposer']}"
                    for r in recent_rounds
                ])
            else:
                conversation_context = "This is the first round. No previous arguments."

            # DEFENDER
            defender_crew = DebateCrew()
            defender_crew.defender_crew().kickoff(inputs={
                'round_num': round_num,
                'num_rounds': num_rounds,
                'article_text': article_for_debate,
                'conversation_context': conversation_context,
                'opposer_last_argument': opposer_last_argument,
                'context': context or "No additional context"
            })
            
            defender_current_argument = defender_crew.defend_task().output.raw
            time.sleep(0.5)

            # OPPOSER
            opposer_crew = DebateCrew()
            opposer_crew.opposer_crew().kickoff(inputs={
                'round_num': round_num,
                'num_rounds': num_rounds,
                'article_text': article_for_debate,
                'conversation_context': conversation_context,
                'defender_current_argument': defender_current_argument,
                'context': context or "No additional context"
            })
            
            opposer_last_argument = opposer_crew.oppose_task().output.raw

            conversation.append({
                'round': round_num,
                'defender': defender_current_argument,
                'opposer': opposer_last_argument
            })

            time.sleep(1)

        # BUILD FULL DEBATE
        full_debate = "\n\n".join([
            f"=== ROUND {r['round']} ===\n"
            f"DEFENDER ARGUED:\n{r['defender']}\n\n"
            f"OPPOSER COUNTERED:\n{r['opposer']}"
            for r in conversation
        ])

        # JUDGE
        self.update_state(state='PROGRESS', meta={'stage': 'judging', 'progress': 90})
        
        judge_crew = DebateCrew()
        judge_crew.judge_crew().kickoff(inputs={
            'article_text': full_article,
            'full_debate': full_debate,
            'num_rounds': num_rounds,
            'context': context or "No additional context"
        })

        raw_judge_output = judge_crew.judge_task().output.raw

        try:
            verdict = extract_json(raw_judge_output)
            required_fields = ['legitimacy_score', 'verdict', 'reasoning_chain']
            if not all(field in verdict for field in required_fields):
                raise ValueError("Missing required fields")
        except Exception as e:
            print(f"Judge parsing error: {e}")
            print(f"Raw output: {raw_judge_output[:500]}")
            
            verdict = {
                "legitimacy_score": 0.5,
                "verdict": "uncertain",
                "confidence": "low",
                "reasoning_chain": [{
                    "step": 1,
                    "factor": "parsing_error",
                    "evidence": "Judge output was malformed",
                    "impact": "0",
                    "justification": str(e)
                }],
                "key_findings": ["Unable to parse judge output"],
                "error": str(e)
            }

        return {
            'conversation': conversation,
            'verdict': verdict,
            'metadata': {
                'rounds': num_rounds,
                'article_length': len(full_article),
                'debate_length': len(full_debate),
                'xai_enabled': True,
                'total_api_calls': (num_rounds * 2) + 1
            }
        }

    except Exception as e:
        print(f"Debate error: {str(e)}")
        raise self.retry(exc=e, countdown=60)