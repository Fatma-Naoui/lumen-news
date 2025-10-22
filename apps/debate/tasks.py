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
    """
    OPTIMIZED: Single crew instance, single execution.
    No redundant agent instantiation.
    """
    try:
        full_article = article_text
        
        MAX_DEBATE_ARTICLE = 1200
        article_for_debate = (
            article_text[:MAX_DEBATE_ARTICLE] + "...[truncated]"
            if len(article_text) > MAX_DEBATE_ARTICLE
            else article_text
        )

        self.update_state(state='PROGRESS', meta={'stage': 'debate_starting', 'progress': 0})

        # ✅ OPTIMIZATION: Create crew ONCE
        debate_crew = DebateCrew()
        
        # ✅ OPTIMIZATION: Run the ENTIRE debate in ONE crew execution
        # The crew handles all rounds + judgment internally
        result = debate_crew.crew().kickoff(inputs={
            'article_text': article_for_debate,
            'full_article': full_article,
            'num_rounds': num_rounds,
            'context': context or "No additional context"
        })

        self.update_state(state='PROGRESS', meta={'stage': 'parsing_results', 'progress': 95})

        # ✅ Extract conversation from task outputs
        conversation = []
        
        # Round 1
        conversation.append({
            'round': 1,
            'defender': debate_crew.defend_round1_task().output.raw,
            'opposer': debate_crew.oppose_round1_task().output.raw
        })
        
        # Round 2
        conversation.append({
            'round': 2,
            'defender': debate_crew.defend_round2_task().output.raw,
            'opposer': debate_crew.oppose_round2_task().output.raw
        })

        # Build full debate transcript
        full_debate = "\n\n".join([
            f"=== ROUND {r['round']} ===\n"
            f"DEFENDER ARGUED:\n{r['defender']}\n\n"
            f"OPPOSER COUNTERED:\n{r['opposer']}"
            for r in conversation
        ])

        # ✅ Get judge verdict
        raw_judge_output = debate_crew.judge_task().output.raw

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
                'total_api_calls': 5,  # ✅ FIXED: Always 5 calls (2+2+1)
                'optimization': 'single_crew_execution'
            }
        }

    except Exception as e:
        print(f"Debate error: {str(e)}")
        raise self.retry(exc=e, countdown=60)