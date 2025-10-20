from apps.debate.crew import DebateCrew
import json

def run_debate(article_text, context="", num_rounds=2):
    """Run multi-round debate with XAI verdict"""
    
    # ✅ OPTIMIZATION: Truncate article to save tokens if too long
    max_article_length = 2000  # Adjust based on your needs
    if len(article_text) > max_article_length:
        article_text = article_text[:max_article_length] + "... [truncated]"
    
    conversation = []
    defender_response = ""
    
    for round_num in range(1, num_rounds + 1):
        # Build conversation history (keep last 1000 chars to save tokens)
        conversation_history = "\n".join([
            f"Round {r['round']}:\nDefender: {r['defender']}\nOpposer: {r['opposer']}"
            for r in conversation
        ]) if conversation else "First round - no previous debate"
        
        # ✅ Truncate history to save tokens
        if len(conversation_history) > 1000:
            conversation_history = "..." + conversation_history[-1000:]
        
        # Run defender task
        crew = DebateCrew()
        crew.crew().kickoff(inputs={
            'round_num': round_num,
            'num_rounds': num_rounds,
            'article_text': article_text,
            'context': context or "No additional context",
            'conversation_history': conversation_history,
            'defender_response': defender_response,
            'full_transcript': ""
        })
        
        defender_response = crew.defend_task().output.raw
        
        # Run opposer task with defender's response
        opposer_crew = DebateCrew()
        opposer_crew.crew().kickoff(inputs={
            'round_num': round_num,
            'num_rounds': num_rounds,
            'article_text': article_text,
            'context': context or "No additional context",
            'conversation_history': conversation_history,
            'defender_response': defender_response,
            'full_transcript': ""
        })
        
        opposer_response = opposer_crew.oppose_task().output.raw
        
        conversation.append({
            'round': round_num,
            'defender': defender_response,
            'opposer': opposer_response
        })
    
    # Build full transcript for judge
    full_transcript = "\n\n".join([
        f"=== ROUND {r['round']} ===\n\nDEFENDER:\n{r['defender']}\n\nOPPOSER:\n{r['opposer']}"
        for r in conversation
    ])
    
    # Run judge with full transcript
    judge_crew = DebateCrew()
    judge_crew.crew().kickoff(inputs={
        'article_text': article_text,
        'full_transcript': full_transcript,
        'conversation_history': full_transcript,
        'num_rounds': num_rounds,
        'round_num': num_rounds,
        'context': context or "No additional context",
        'defender_response': ""
    })
    
    # Parse XAI verdict
    try:
        raw_output = judge_crew.judge_task().output.raw
        # Remove markdown code blocks if present
        if "```json" in raw_output:
            raw_output = raw_output.split("```json")[1].split("```")[0]
        elif "```" in raw_output:
            raw_output = raw_output.split("```")[1].split("```")[0]
        
        verdict = json.loads(raw_output.strip())
    except Exception as e:
        print(f"Judge parsing error: {e}")
        verdict = {
            "legitimacy_score": 0.5,
            "verdict": "uncertain",
            "verdict_explanation": "Could not parse judge output",
            "error": str(e)
        }
    
    return {
        'conversation': conversation,
        'verdict': verdict,
        'metadata': {
            'rounds': num_rounds,
            'article_length': len(article_text),
            'debate_length': len(full_transcript)
        }
    }

