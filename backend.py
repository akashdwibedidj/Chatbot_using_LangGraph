from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Annotated
import operator
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0.2)
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):
    messages = state['messages']

    response = llm.invoke(messages)

    return {'messages': [response]}

checkpointer = MemorySaver()

graph = StateGraph(ChatState)

graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)



# chatbot
# initial_state = {
#     'messages': [HumanMessage(content='What is the capital of India')]
# }

# chatbot.invoke(initial_state)['messages'][-1].content
# thread_id = '1'

# while True:
#     user_message = input('Type here: ')

#     print('User : ', user_message)

#     if user_message.strip().lower() in ['exit', 'quit', 'bye']:
#         break

#     config = {'configurable':{'thread_id':thread_id}}

#     response = chatbot.invoke({'messages': [HumanMessage(content=user_message)]}, config=config)

#     print('AI : ', response['messages'][-1].text)
# chatbot.get_state(config=config)