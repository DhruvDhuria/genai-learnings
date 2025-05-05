from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
import json
import pprint

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

embedder = OpenAIEmbeddings(
    model = "text-embedding-3-large",
    api_key= openai_api_key
)

retriver = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_langchain",
    embedding=embedder
)
user_query = input('> ')

QUERY_ENHANCING_PROMPT = f"""
You are a ai assistant who is very knowledgable about everything related to Nodejs. You know everything about it. Your job is to understand the user query carefully and check what the user is trying to ask and based on that query you create three more queries which are more specific and related to the user query so that the answer can be found easily and the answer is more accurate.

Rules:
- Always create three more queries which are more specific and related to the user query.

Output format: 
["query1", "query2", "query3"]
"""

completion = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        { "role": "system", "content": QUERY_ENHANCING_PROMPT },
        { "role": "user", "content": user_query },
    ]
)

query_list = json.loads(completion.choices[0].message.content)

chunk_list = []

for query in query_list: 
    relevant_chunks = retriver.similarity_search(
        query=query
    )
    chunk_list.append(relevant_chunks)

context_chunks = []

for index, doc_set in enumerate(chunk_list):
    # print("INDEX:", index, doc_set )
    for index, doc_chunk in enumerate(doc_set):
        # print("INDEX: ", index, doc_chunk)
        page_no = doc_chunk.metadata.get("page", "N/A")  # Safe access
        content = doc_chunk.page_content
        context_chunks.append({"page_no": page_no, "content": content})


# Filter out duplicates
seen = set()
unique_documents = []
for doc in context_chunks:
    frozen_doc = frozenset(doc.items())  # Make the dictionary hashable
    if frozen_doc not in seen:
        seen.add(frozen_doc)
        unique_documents.append(doc)


SYSTEM_PROMPT = f""" 
You are a knowledgeable and helpful AI assistant. Use only the information provided in the context below to answer the user's query. The context includes page numbers and their corresponding content from a PDF document. At the end of the answer, provide the page number from which the answer is taken.

If the answer is not present in the context, respond with "The answer is not available in the provided context."


Be concise, factual, and helpful in your responses.

CONTEXT: {unique_documents}
"""


completion = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": user_query },
    ]
)

print(completion.choices[0].message.content)