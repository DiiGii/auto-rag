# AutoRAG: Autonomous Retrieval-Augmented Generation 
## Overview
This Streamlit app presents Autonomous RAG (Retrieval-Augmented Generation) implemented with the GPT-4o-mini model and Phidata's PgVector2 backend. Features include document upload, web search, and more.

Check it out at: https://dii-gii-auto-rag.streamlit.app/

## Features
* Caching for resource efficiency
* Document (PDF) upload and knowledge base querying
* Web search (DuckDuckGo)
* OpenAI API key validation
* Intuitive, user-friendly UI

## Deep Dive: What is RAG? 
**Retrieval Augmented Generation (RAG)** lets AI chatbots use external knowledge to give better answers. Instead of just relying on their training data, they first search a knowledge base (like a library or the internet) for relevant information and then use that information to craft their response. This makes their answers more accurate, up-to-date, and relevant to the conversation.

**Autonomous RAG** takes this a step further. Instead of waiting for instructions on what to look for, the AI figures it out itself. It decides what information it needs, comes up with search queries, and actively hunts for the right context. This lets it handle more complex questions and adapt to changing information.

## How to use? 
If you would like to test this app locally: 
1. Clone the Github.
2. Once in the repository's root directory, run `pip install -r requirements.txt` in your terminal to install dependencies
3. In the same directory, run `streamlit run main.py` to deploy the app locally.

Otherwise, check out the app on Streamlit: 
1. https://dii-gii-auto-rag.streamlit.app/

## Conclusion
A beautiful, easy-to-use tool for AutoRAG. I would highly recommend trying to implement this project yourself, as it gives you insight into various aspects of AI application development: database setup, LLM APIs, and building out the UX and UI. Please 
