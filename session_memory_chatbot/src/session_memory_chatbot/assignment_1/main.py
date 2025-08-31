from session_memory_chatbot.assignment_1.connection import gemini_model
from agents import Agent, Runner, ModelSettings, SQLiteSession, set_tracing_disabled
import chainlit as cl

set_tracing_disabled(disabled=True)


agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model_settings=ModelSettings(temperature=0.5),
    model=gemini_model,
)


async def show_session_memory(sid: int):
    session_id = f"user_{sid}"
    session = SQLiteSession(session_id=session_id, db_path="conversation.db")
    items = await session.get_items()

    if not items:  
        
        await cl.Message(content="👋 Welcome! I'm your assistant. How can I help you today?").send()
    else:
        
        await cl.Message(content="📜 Welcome back! Here’s your previous conversation:").send()
        for data in items:
            if data["role"] == "user":
                await cl.Message(content=f"**You:** {data['content']}").send()

            elif data["role"] == "assistant":
                content = data["content"]
                if isinstance(content, list):
                    texts = [item.get("text", "") for item in content if isinstance(item, dict)]
                    clean_text = " ".join(texts).strip()
                    await cl.Message(content=f"**Assistant:** {clean_text}").send()
                else:
                    await cl.Message(content=f"**Assistant:** {content}").send()

    return session



@cl.on_chat_start
async def on_start():
    
    session = await show_session_memory(1)
    cl.user_session.set("session", session)



@cl.on_message
async def on_message(message: cl.Message):
    session = cl.user_session.get("session")

    result = await Runner.run(
        starting_agent=agent,
        input=message.content,
        session=session,
    )

    await cl.Message(content=result.final_output).send()