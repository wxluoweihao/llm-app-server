base_suffix = """
When giving the final answer, also append the final SQL and explain it. 
each sentence should take a new line.
For example,
```sql 
SELECT COUNT(*) from employee WHERE employee.name = xxx, 
```
this query find the number of employee whose name is xxx.\n

You must use reponses from database to answer questions.
if the answers contains multiple items, list them line by line. 
For example, the final answer is [apple, orange, banana], list thema as follow:
-apple
-orange
-banana"""

custom_suffix_sim = """
I should first get the similar examples I know.
If the examples are enough to construct the query, I can build it.
Otherwise, I can then look at the tables in the database to see what I can query.
Then I should query the schema of the most relevant tables.
"""

custom_suffix_filter = """
If a query statement asks for me to filter based on proper nouns, I should first check the spelling using the name_search tool.
Filter nouns are case-sensitive. For example, `Orange` and `orange` are different in spelling. if SQL is filtering on `Orange`,
but name_search gives `orange` as the most similar noun then you should use `orange` in SQL.
Otherwise, I can then look at the tables in the database to see what I can query.
Then I should query the schema of the most relevant tables.
"""
import openai
openai.api_base = "https://api.chatanywhere.com.cn/v1"

#prepare vector store
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain.agents.agent_toolkits import create_retriever_tool

def create_retriever_sim(openai_key):
    embeddings =  OpenAIEmbeddings(openai_api_key = openai_key)
    vectorDB_sim = FAISS.load_local("./data/similar_example_store_index", embeddings)
    retriever_sim = vectorDB_sim.as_retriever()
    tool_sim_des = """
    This tool will help you understand similar examples to adapt them to the user question.
    Input to this tool should be the user question.
    """

    retriever_sim = create_retriever_tool(
        retriever_sim, 
        name="sql_get_similar_examples", 
        description=tool_sim_des
    )
    return retriever_sim

def create_retriever_filter(opai_key):
    embeddings =  OpenAIEmbeddings(openai_api_key = opai_key)
    vector_db_filter = FAISS.load_local("./data/name_search_store_index", embeddings)
    retriever_filter = vector_db_filter.as_retriever()
    tool_filter_des = "use to learn how a piece of data is actually written, can be from names, surnames addresses etc"
    retriever_tool_filter = create_retriever_tool(
        retriever_filter,
        name="name_search",
        description=tool_filter_des
        )
    return retriever_tool_filter


