from apps.debate.crew import DebateCrew
import json

def run_debate(article_text, context="", num_rounds=2):
    """Run multi-round conversational debate"""
    
    conversation = []
    
    for round_num in range(1, num_rounds + 1):
        # Build up the dialogue history so far
        conversation_history = "\n".join([
            f"Round {r['round']}:\nDefender: {r['defender']}\nOpposer: {r['opposer']}"
            for r in conversation
        ]) if conversation else "First round"
        
        # Initialize and run the current round
        crew = DebateCrew()
        result = crew.crew().kickoff(inputs={
            'round_num': round_num,
            'num_rounds': num_rounds,
            'article_text': article_text,
            'context': context or "No context",
            'conversation_history': conversation_history,
            'defender_response': "",
            'full_transcript': ""  # ✅ added placeholder to satisfy CrewAI template
        })
        
        # Store both agents’ responses for this round
        conversation.append({
            'round': round_num,
            'defender': crew.defend_task().output.raw,
            'opposer': crew.oppose_task().output.raw
        })
    
    # Build the full transcript after all rounds
    full_transcript = "\n".join([
        f"Round {r['round']}:\n{r['defender']}\n{r['opposer']}"
        for r in conversation
    ])
    
    # Run the judge crew on the final transcript
    judge_crew = DebateCrew()
    judge_crew.crew().kickoff(inputs={
    'article_text': article_text,
    'full_transcript': full_transcript,
    'conversation_history': full_transcript,  # 👈 add this
    'num_rounds': num_rounds,
    'round_num': num_rounds,
    'context': context or "No context"
})


    # Try parsing the verdict safely
    try:
        verdict = json.loads(judge_crew.judge_task().output.raw)
    except Exception:
        verdict = {"legitimacy_score": 0.5, "verdict": "uncertain"}
    
    # Return the full conversation and verdict
    return {'conversation': conversation, 'verdict': verdict}
