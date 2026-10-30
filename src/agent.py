from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.runnables.history import RunnableWithMessageHistory

from src.config import MODEL_NAME
from src.tools import (
    fetch_account_details,
    check_system_status,
    create_support_ticket,
    send_email_confirmation,
    check_and_book_calendar
)
from src.rag import query_company_policy
from src.memory import get_chat_history, fetch_user_tier

def build_service_desk_agent(user_email: str):
    """
    Factory function that builds a personalized agent pipeline for a specific user.
    """

    user_tier = fetch_user_tier(user_email)
    
    llm = ChatGroq(model=MODEL_NAME, temperature=0.0)
    
    tools = [
        query_company_policy,
        fetch_account_details,
        check_system_status,
        create_support_ticket,
        send_email_confirmation,
        check_and_book_calendar
    ]
    
    system_instructions = f"""
    You are the Autonomous Enterprise Service Desk Agent (Tier-0).
    You are currently helping an authenticated user with the email: {user_email}
    Their account tier is: {user_tier}.
    
    STRICT RULES FOR OPERATION:
    1. RAG FIRST: ALWAYS use the `query_company_policy` tool before giving advice on hardware, software, refunds, or escalations. Never guess company policy.
    2. OUTAGE CHECKS: If a user complains about software downtime (e.g., 'login failure', 'crashing'), use `check_system_status` before creating a ticket. 
    3. SELF-CORRECTION: If a tool returns an error (e.g., failed to book a calendar), analyze the error message, adjust your arguments, and try again.
    4. VIP ESCALATION: Only VIP users can have calendar meetings booked with human managers. Do not book meetings for Standard users unless policy explicitly overrides.
    5. TICKET LOGGING: If you create a support ticket, always email the user their Ticket ID.
    
    Think step-by-step. Plan your actions, execute them, and verify the observations.
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_instructions),
        ("placeholder", "{chat_history}"),       
        ("user", "{input}"),
        ("placeholder", "{agent_scratchpad}")    
    ])
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, 
        handle_parsing_errors=True,
        max_iterations=10
    )
    
    memory_agent = RunnableWithMessageHistory(
        runnable=agent_executor,
        get_session_history=get_chat_history,
        input_messages_key="input",
        history_messages_key="chat_history"
    )
    
    return memory_agent


def execute_agent(user_input: str, user_email: str, session_id: str):
    print(f"\n[SYSTEM] Executing request for {user_email}...")
    
    agent = build_service_desk_agent(user_email)
    config = {"configurable": {"session_id": session_id}}
        
    response = agent.invoke({"input": user_input}, config=config)
    return response["output"]