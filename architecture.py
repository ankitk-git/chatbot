from src.database.db import collection
from src.llm import llm
from bson import ObjectId
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder




def create_new_chat():
    session_dict={
        "context" : None,
        "session_history" : []
    }

    collection.insert_one(session_dict)

    return "New Chat Created!"




def send_message(id : str, message : str):
    document = collection.find_one({"_id": ObjectId(id)})
    
    message_history = []
    for each_history in document["session_history"]:
        message_history.append(HumanMessage(each_history["human_message"]))
        message_history.append(AIMessage(each_history["ai_message"]))
    
    store = {
        id : InMemoryChatMessageHistory(
            messages=message_history
        )
    }

    prompt = ChatPromptTemplate.from_messages([
        ("system", document["context"], ), MessagesPlaceholder(variable_name="messages"),
    ])

    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        return store[session_id]
    
    chain = prompt | llm

    with_message_history = RunnableWithMessageHistory(chain, get_session_history)

    response = with_message_history.invoke(
        [HumanMessage(content=message)],
        config={
                    "configurable": {
                        "session_id": id
                        }
                    },
        )
    
    filter_ = {"_id": ObjectId(id)}
    update = {"$set": {
        "session_history" : document["session_history"] + [{"human_message" : message, "ai_message" : str(response.content)}]
        }}
    
    collection.update_one(filter_, update)

    return response.content

