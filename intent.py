'''
import re

def detect_intent(text, llm):
    # 1. Simple Keyword Check (Faster & Cheaper)
    text_lower = text.lower()
    if any(x in text_lower for x in ["hi", "hello", "hey", "start"]):
        return "greeting"
    
    # 2. LLM Classification for complex queries
    prompt = f"""
    Classify the user's message into exactly one of these three labels:
    - greeting
    - product
    - high_intent

    User message: "{text}"
    
    Return ONLY the label.
    """
    try:
        response = llm.invoke(prompt).content.strip().lower()
        # Clean up any extra punctuation the LLM might add
        clean_label = re.sub(r'[^a-z_]', '', response)
        
        if clean_label in ["greeting", "product", "high_intent"]:
            return clean_label
        return "greeting" # Fallback
    except:
        return "greeting"
    '''
import re

def detect_intent(text, llm):
    """
    Robust intent detection using Keywords first, then LLM.
    """
    text = text.lower().strip()
    
    # --- 1. KEYWORD RULES (Fast & Reliable for Demo) ---
    
    # Rule A: Greeting
    greeting_words = ["hi", "hello", "hey", "greetings", "good morning", "good evening"]
    if any(word in text for word in greeting_words) and len(text.split()) < 5:
        return "greeting"

    # Rule B: Product / Pricing (The fix for your loop)
    product_words = ["price", "cost", "plan", "basic", "pro", "feature", "how much", "details"]
    if any(word in text for word in product_words):
        return "product"

    # Rule C: High Intent (Lead Capture)
    intent_words = ["sign up", "buy", "purchase", "interested", "join", "register", "start"]
    if any(word in text for word in intent_words):
        return "high_intent"

    # --- 2. LLM FALLBACK (Only if keywords fail) ---
    prompt = f"""
    Classify the user's message into exactly one of these three labels:
    - greeting
    - product
    - high_intent

    User message: "{text}"
    
    Return ONLY the label.
    """
    try:
        response = llm.invoke(prompt).content.strip().lower()
        clean_label = re.sub(r'[^a-z_]', '', response)
        
        if clean_label in ["greeting", "product", "high_intent"]:
            return clean_label
        return "greeting" # Safety fallback
    except:
        return "greeting"