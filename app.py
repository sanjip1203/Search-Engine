import streamlit as st
from langchain_groq import ChatGroq 
from langchain_community.utilities import ArxivAPIWrapper ,WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun,DuckDuckGoSearchRun
from langchain_classic.agents import initialize_agent,AgentType
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
import os 
from dotenv import load_dotenv 
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

### Arxiv and Wikipedia Tools 
arxiv_wrapper =ArxivAPIWrapper(top_k_results=1,doc_content_chars_max=200)
arxiv=ArxivQueryRun(api_wrapper=arxiv_wrapper)

api_wrapper=WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=200)
wiki=WikipediaQueryRun(api_wrapper=api_wrapper)

search = DuckDuckGoSearchRun(name="Search")
st.title("Langchain - Chat with Search")
'''
In this example , we ' suing 'StreamlitCallbackHandler to display the thoughts and action in an intercative streamlit app .

'''
## Sidebar for settings 
st.sidebar.title("settings")
api_key = st.sidebar.text_input("Enter your Groq API Key:",type="password")


if not api_key:
    st.warning("Please enter your Groq API key in the sidebar.")
    st.stop()


if "messages" not in st.session_state:
    st.session_state['messages']=[
        {"role":"assisstant",
         "content":"Hi, I am a chatbot who can search the web . How can I Help you ? "}
    ]
for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

if prompt:=st.chat_input(placeholder="what is machine learning?"):
    st.session_state.messages.append({"role":"user",
                                      "content":prompt
                                      })
    st.chat_message("user").write(prompt)
    llm=ChatGroq(groq_api_key=api_key,model_name="llama-3.1-8b-instant",streaming=True)
    tools=[search,arxiv,wiki]
    search_agent=initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,handling_parsing_errors=True)
     
    with st.chat_message("assistant"):
        st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=True)
        response=search_agent.run(st.session_state.messages,callbacks=[st_cb])
        st.session_state.messages.append({'role':'assistant',"content":response})
        st.write(response)
