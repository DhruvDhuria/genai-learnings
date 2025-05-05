from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY") 

pdf_path = Path(__file__).parent / "nodejs_pdf.pdf"
loader = PyPDFLoader(file_path=pdf_path)

docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200
)

splitted_docs = text_splitter.split_documents(documents=docs)

embedder = OpenAIEmbeddings(
    model = "text-embedding-3-large",
    api_key= openai_api_key
)

# vector_store = QdrantVectorStore.from_documents(
#     documents=[],
#     url="http://localhost:6333",
#     collection_name="learning_langchain",
#     embedding=embedder
# )

# vector_store.add_documents(documents=splitted_docs)

print("Injection done", )

retriver = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_langchain",
    embedding=embedder
)
user_query = "What is FS Module?" 
relevant_chunks = retriver.similarity_search(
    query=user_query
)

# json_chunks = json.dumps(relevant_chunks)

context_chunks = []


for doc in relevant_chunks:
    page_no = doc.metadata.get("page", "N/A")  # Safe access
    content = doc.page_content
    context_chunks.append({"page_no": page_no, "content": content})



SYSTEM_PROMPT = f""" 
You are a knowledgeable and helpful AI assistant. Use only the information provided in the context below to answer the user's query. The context includes page numbers and their corresponding content from a PDF document.

If the answer is not present in the context, respond with "The answer is not available in the provided context."


Be concise, factual, and helpful in your responses.

CONTEXT: {context_chunks}
"""

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": user_query },
    ]
)

print(completion.choices[0].message.content)