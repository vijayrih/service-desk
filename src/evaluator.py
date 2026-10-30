from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from src.config import MODEL_NAME
from src.agent import build_service_desk_agent
from src.rag import query_company_policy

class EvaluationResult(BaseModel):
    is_compliant: bool = Field(description="True if the response perfectly adheres to company policies, False otherwise.")
    critique: str = Field(description="If False, explain exactly what policy was violated. If True, output 'Approved'.")

# Evaluator Chain
def build_evaluator():
    llm = ChatGroq(model=MODEL_NAME, temperature=0.0)
    
    structured_llm = llm.with_structured_output(EvaluationResult)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are the QA Compliance Manager for the Enterprise Service Desk.
        Your job is to review the AI Agent's drafted response to the user.
        
        You must ensure the draft strictly follows this company policy:
        {policy_context}
        
        CRITICAL RULES:
        - If the agent promised a refund without mentioning photo evidence (if required), FAIL IT.
        - If the agent is speaking to a VIP and forgot to include the VIP emergency phone number, FAIL IT.
        - If the agent hallucinates a policy not in the text, FAIL IT.
        """),
        ("user", "User's Original Request: {user_input}\n\nAgent's Draft Response: {draft_response}\n\nEvaluate this draft.")
    ])
    
    return prompt | structured_llm

# The Reflection Loop Orchestrator
async def execute_with_reflection(user_input: str, user_email: str, session_id: str, max_retries: int = 2):
    """
    Runs the agent, evaluates the draft, and forces a retry if it fails compliance.
    """
    print(f"\n[SYSTEM] Starting Resolution for {user_email}...")
    
    agent = build_service_desk_agent(user_email)
    config = {"configurable": {"session_id": session_id}}
    
    evaluator = build_evaluator()
    
    print("\n[EXECUTOR] Analyzing request and executing tools...")
    response = await agent.ainvoke({"input": user_input}, config=config)
    draft = response["output"]
    
    for attempt in range(max_retries):
        print(f"\n[EVALUATOR] Reviewing Draft (Attempt {attempt + 1})...")
        
        policy_context = query_company_policy.invoke({"topic": user_input})
        
        eval_result = await evaluator.ainvoke({
            "policy_context": policy_context,
            "user_input": user_input,
            "draft_response": draft
        })
        
        if eval_result.is_compliant:
            print("[EVALUATOR] Draft Approved. Policy compliant.")
            return draft
        else:
            print(f"[EVALUATOR] Draft Rejected. Critique: {eval_result.critique}")
            print("[EXECUTOR] Revising draft based on QA critique...")
            
            correction_prompt = (
                f"Your previous response was rejected by QA for this reason: {eval_result.critique}. "
                "Please fix your response and use any tools necessary to complete missing actions. "
                "Output the final, corrected response for the user."
            )
            response = await agent.ainvoke({"input": correction_prompt}, config=config)
            draft = response["output"]
            
    print("\n[SYSTEM] Warning: Max retries reached. Outputting safest available draft.")
    return draft