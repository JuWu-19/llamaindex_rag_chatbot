# app.py

import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Gets the directory of the current script
LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)  # Create logs directory if it doesn't exist
LOG_FILE = os.path.join(LOG_DIR, 'app.log')

#logging.basicConfig(level=logging.DEBUG, filename=LOG_FILE, filemode='w', 
#                   format='%(name)s - %(levelname)s - %(message)s')

from dotenv import load_dotenv
load_dotenv()  # This loads the .env file variables into the environment
print("ADMIN_PASSWORD:", os.getenv("ADMIN_PASSWORD"))
import pdb


def noop(*args, **kwargs):
    pass  # No operation performed

pdb.set_trace = noop  # Override set_trace to do nothing

#logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
pdb.set_trace()

from flask import Flask
from flask_cors import CORS
from flask_cors import cross_origin

from flask_login import LoginManager
from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, UserMixin, login_user, current_user

from auth import auth_bp
from admin import admin_bp

# for file upload and web scraping
import re
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
import requests

from werkzeug.security import check_password_hash

# for rag llm
import openai

# llamaindex + chromadb
# import chromadb
# from llama_index.core import VectorStoreIndex, StorageContext
# from llama_index.vector_stores.chroma.base import ChromaVectorStore
# from llama_index.core import Document
# from llama_index.embeddings.openai import OpenAIEmbedding

app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

# Setup CORS
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=False)
#CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}}, supports_credentials=True)
# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:wj123@localhost/user_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional: reduces overhead

app.config['SESSION_COOKIE_DOMAIN'] = '.localhost'  # Adjust based on your local or deployment settings
app.config['SESSION_COOKIE_NAME'] = 'session'

pdb.set_trace()
# Create an SQLAlchemy object by passing it the application
db = SQLAlchemy(app)

# If using Flask's app logger:
#app.logger.setLevel(logging.DEBUG)

def hello():
    return "Hello World!"

app.config['SECRET_KEY'] = 'wj123'

# Optional: Configure other app settings related to sessions
# app.config['SESSION_PERMANENT'] = True
# app.config['SESSION_COOKIE_DOMAIN'] = '127.0.0.1'
# app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # Example: 24 hours
# app.config['SESSION_COOKIE_NAME'] = 'flask_session'
# app.config['SESSION_COOKIE_HTTPONLY'] = True
# app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Can be 'Strict', 'Lax', or 'None'

# Setup Flask-Login after db because it doesn't depend on db
# from flask_login import LoginManager
# pdb.set_trace()
# login_manager = LoginManager()
# login_manager.init_app(app)
# pdb.set_trace()

from models import User, Document, DocumentAccess, Feedback, ChatHistory# Import models
# pdb.set_trace()
# # User loader callback for Flask-Login
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))
# pdb.set_trace()
# Route to log in a user and start a session

# @app.route('/api/get_embeddings', methods=['POST'])
# def main_em():
#     st="你还好吗"
#     res=get_embeddings(st)
#     embed=res['data'][0]['embedding']
#     return embed.json()

# def get_embeddings(text):
#     api_key = os.getenv('OPENAI_API_KEY')
#     url = "https://api.app4gpt.com/v1/embeddings"
#     payload = {
#         "input": text,
#         "model": "text-embedding-ada-002"
#     }
#     headers = {
#         'Authorization': f'Bearer {api_key}',
#         'Content-Type': 'application/json'
#     }
#     try:
#         response = requests.post(url, json=payload, headers=headers)
#         response.raise_for_status()
#         return jsonify(response.json()), 200
#     except requests.exceptions.RequestException as e:
#         app.logger.error(f"Failed to fetch embeddings: {str(e)}")
#         return jsonify({"error": str(e)}), 500


@app.route('/api/get_embeddings', methods=['POST'])
def main_em():
    try:
        text="你还好吗"
        res = get_embeddings(text)
        return res
        # if res.status_code == 200:
        #     embed = res.json()['data'][0]['embedding']
        #     return jsonify({"embedding": embed}), 200
        # else:
        #     return jsonify({"error": "Failed to fetch embeddings"}), res.status_code
    except Exception as e:
        app.logger.error(f"Error in main_em: {str(e)}")
        return jsonify({"error": str(e)}), 500

def get_embeddings(text):
    api_key = os.getenv('OPENAI_API_KEY')
    url = "https://api.app4gpt.com/v1/embeddings"
    payload = {
        "input": text,
        "model": "text-embedding-ada-002"
    }
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)
    # if response.status_code == 200:
    response_data = response.json()

    return response_data

    # else:
    #     logging.error(f"API call failed with status code: {response.status_code}")
    #     return None, False


@app.route('/api/login', methods=['POST'])
def login():
    try:
        from models import User
        data = request.get_json()
        
        account_num = data.get('account_number')
        password = data.get('password')
        
        user = User.query.filter_by(account_number=account_num).first()
        if user and check_password_hash(user.user_password, password):
            return jsonify({"message": "Logged in successfully", "user_id": user.user_id, "username": user.user_name, "account_number":account_num}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/get-user-data', methods=['POST'])
def get_user_data():
    try:
        data = request.get_json()
        account_num = data['account_number']
        password = data['password']
        user = User.query.filter_by(account_number=account_num).first()

        if user and check_password_hash(user.user_password, password):
            documents = Document.query.all()
            access_list = []
            for doc in documents:
                access = DocumentAccess.query.filter_by(doc_id=doc.doc_id, user_id=user.user_id).first()
                doc_info = {
                    "doc_id": doc.doc_id,
                    "doc_name": doc.doc_name,
                    "uploader": doc.txt_uploader_name,
                    "has_access": bool(access and access.access_right)
                }
                access_list.append(doc_info)
            
            user_data = {
                "userID": user.user_id,
                "username": user.user_name,
                "documents": access_list
            }
            return jsonify(user_data), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        app.logger.error(f"Error fetching user data: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route('/api/users', methods=['GET'])
#@cross_origin(origins=['http://localhost:8080'])  # Adjust the origins according to where your frontend is hosted
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

# session for user management as bonus feature, not core one
# pdb.set_trace() 
# # Route to get the current user's session data
# @app.route('/api/user/session', methods=['GET'])
# @login_required
# def get_user_session():
#     logging.debug("Session endpoint hit")
#     if current_user.is_authenticated:
#         logging.error("User not authenticated")
#         return jsonify({"error": "User not logged in"}), 401
#     current_user_data = {
#         "username": current_user.user_name,
#         "user_id": current_user.get_id()
#     }
#     return jsonify(current_user_data), 200

# pdb.set_trace()


# @app.route('/api/documents/access', methods=['POST'])
# @login_required
# def modify_document_access():
#     data = request.get_json()
#     doc_id = data.get('doc_id')
#     user_id = data.get('user_id')
#     access_right = data.get('access_right')  # Expecting True or False

#     access = DocumentAccess.query.filter_by(doc_id=doc_id, user_id=user_id).first()
#     if not access:
#         access = DocumentAccess(doc_id=doc_id, user_id=user_id, access_right=access_right)
#         db.session.add(access)
#     else:
#         access.access_right = access_right
#     db.session.commit()
#     return jsonify({"message": "Access updated"}), 200

@app.route('/api/send-query', methods=['POST'])
def send_query():
    data = request.json
    query = data.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    # Get the API key from an environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        app.logger.error('OPENAI_API_KEY is not set.')
        return jsonify({'error': 'Server configuration error'}), 500

    # External API details
    URL = 'https://api.app4gpt.com/v1/chat/completions'

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    body = {
        'model': 'gpt-4',
        'messages': [{'role': 'user', 'content': query}]
    }

    try:
        response = requests.post(URL, json=body, headers=headers)
        response.raise_for_status()
        data = response.json()
        return jsonify(data), 200
    except requests.exceptions.RequestException as e:
        app.logger.error(f'Error sending query to external API: {e}')
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        app.logger.error(f'Unexpected error: {e}')
        return jsonify({'error': 'An unexpected error occurred'}), 500

# generate RAG answer for query with the help of llamaindex and chromadb... but sometimes, the openai api called in llamaindex not stable

@app.route('/api/send-query-rag', methods=['POST'])
def send_query_rag():
    data = request.json
    query = data.get('query')
    user_id = data.get('user_id')
    PROMPT_TEMPLATE, combined_prompt = rag_prompt(user_id, query)
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    try:
        response = requests.post(
            "https://api.app4gpt.com/v1/chat/completions",
            json={'model': 'gpt-4', 'messages': [{'role': 'user', 'content': PROMPT_TEMPLATE}]},
            headers={'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}', 'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        api_response = response.json()
        answer = api_response['choices'][0]['message']['content']
        time_created=api_response['created']
        return jsonify({'answer': answer, 'docu_relevance': combined_prompt,'time_created':time_created, 'total_prompt':PROMPT_TEMPLATE}), 200

    except requests.exceptions.RequestException as e:
        logging.error(f'API Request Error: {e}')
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        logging.error(f'Unexpected Server Error: {e}')
        return jsonify({'error': 'An unexpected error occurred'}), 500

def rag_prompt(user_id, query):
    import openai
    from llama_index.core.retrievers import VectorIndexRetriever
    import chromadb
    from llama_index.core import VectorStoreIndex, StorageContext
    from llama_index.vector_stores.chroma.base import ChromaVectorStore
    #from llama_index.core import Document naming conflicts
    from llama_index.core import Document as LlamaDocument
    from models import Document as MyDocument

    # openai.api_base = "https://api.app4gpt.com/v1"
    # openai.api_base=os.environ.get("OPENAI_API_BASE")
    # openai.api_key = os.environ.get("OPENAI_API_KEY")
    try:
        # Fetch documents the user has access to
        accessible_documents = db.session.query(MyDocument).join(
            DocumentAccess, MyDocument.doc_id == DocumentAccess.doc_id
        ).filter(
            DocumentAccess.user_id == user_id,
            DocumentAccess.access_right == True
        ).all()

        # Prepare data for retrieval
        # documents_data = [{"doc_name": doc.doc_name, "content": doc.txt_content} for doc in accessible_documents]
        # Process documents data for use or response
        documents_data = []
        for doc in accessible_documents:
            doc_info = {
                "doc_name": doc.doc_name,
                "content": doc.txt_content
            }
            documents_data.append(doc_info)
        # Log each document's name and a snippet of content
            logging.info(f"Document processed: {doc.doc_name}, Content Snippet: {doc.txt_content[:50]}")  # shows first 50 characters
     #   documents = [LlamaDocument(text=d['content'], metadata={"file_name": d['doc_name']}) for d in documents_data]
        print(f"number of docu accessed: {len(documents_data)}")
        # Setup ChromaDB client and collection
        # cdb = chromadb.Client()
        # chroma_collection = cdb.get_or_create_collection("test39")
        # vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        # storage_context = StorageContext.from_defaults(vector_store=vector_store)
        # index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
        # from llama_index.embeddings.openai import OpenAIEmbedding
        # from llama_index.core import Settings

        # due to constant retry for embeddings, which does not appear in jupyter notebook env we thus define the embedding config explicitly
        from llama_index.llms.openai import OpenAI
        from llama_index.embeddings.openai import OpenAIEmbedding
        from llama_index.core import Settings

        # Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002")

        # Document objects created but with no embedding data, embeddings will get only if in index.from_documents
        # index = VectorStoreIndex.from_documents(documents, embed_model=Settings.embed_model)
        # # most simple one

        # it seems as long as we use openai api pkg, connection fails (maybe due to some ugly network settings on how flask access internet)
        # so we first build Document, then parser into nodes, then create index
        from llama_index.core.storage.docstore import SimpleDocumentStore
        from llama_index.core.storage.index_store import SimpleIndexStore
        from llama_index.core.vector_stores import SimpleVectorStore
        from llama_index.core import StorageContext
        from llama_index.core import GPTVectorStoreIndex
        from llama_index.core.retrievers import VectorIndexRetriever
        # create storage context using default stores
        storage_context = StorageContext.from_defaults(
            docstore=SimpleDocumentStore(),
            vector_store=SimpleVectorStore(),
            index_store=SimpleIndexStore(),
        )
        import requests

        documents=[]
        for doc in documents_data:
            #print(f"content of test docu: {doc['content']}")
            text=doc['content']
            res = get_embeddings(text)
            logging.info(res)
            # if res.status_code == 200:
            #     if 'data' in res:
            #         embed = res.json()['data'][0]['embedding']
            #     else:
            #         logging.error("API response does not contain 'data' key")
            #         logging.info(res.json)
                #embed = res.json()['data'][0]['embedding']
            # embedding = embed
            embedding = res['data'][0]['embedding']
            print(f"content of embedding: {embedding}")
            # Store the embedding and document text in ChromaDB for retrieval
            # document_id = content[:30]  # Use the first 30 chars as a unique ID
            # collection.add(embeddings=[embedding], ids=[document_id])

            doc = LlamaDocument(text=doc['content'], embedding=embedding)  # Create a Document with embedded data
        # index3.insert(doc)  # Insert the Document into the index
            documents.append(doc)
        print(f"length of embeded docus: {len(documents)}")
        PROMPT_TEMPLATE, combined_prompt=index_get_docu(documents, query)

        return PROMPT_TEMPLATE, combined_prompt
    except Exception as e:
        print(f"Error generating prompt: {e}")
        logging.error(f"Error generating prompt: {e}")
        return None, None  # Handle the error as appropriate

def index_get_docu(documents,query):
    from llama_index.core.node_parser import SimpleNodeParser
    from llama_index.core import GPTVectorStoreIndex
    from llama_index.core.retrievers import VectorIndexRetriever
    parser = SimpleNodeParser()
    nodes = parser.get_nodes_from_documents(documents)
    index = GPTVectorStoreIndex(nodes)
    # most simple and intuitive way
    # index = VectorStoreIndex.from_documents(documents)
    # Retrieve relevant content using the index
    retriever = VectorIndexRetriever(index=index, similarity_top_k=2)
    nodes = retriever.retrieve(query)

    # Format results for response
    retrieval_results = [{"content": node.node.text, "score": node.score, "title": node.node.metadata} for node in nodes]
    combined_prompt = "\n".join([f"{r['title']}\n{r['content']}\nScore: {r['score']}\n{'-'*50}" for r in retrieval_results])

    # Format the prompt for the completion API
    PROMPT_TEMPLATE = f"你可以参考以下文章:\n{combined_prompt}\n问题：{query}\n回答："

    return PROMPT_TEMPLATE, combined_prompt
def fetch_embedding(text):
    from time import sleep
    api_key = os.getenv('OPENAI_API_KEY')
    url = "https://api.app4gpt.com/v1/embeddings"
    payload = {
        "input": text,
        "model": "text-embedding-ada-002"
    }
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    retries=5
    backoff_factor=1.5
    for attempt in range(retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            # Access the first embedding in the list (assuming only one embedding is requested)
            embedding_vector = response_data['data'][0]['embedding']
            logging.info(f"TEST EMBED: {embedding_vector}")
            return embedding_vector
        except requests.exceptions.HTTPError as e:
            logging.info(e)
            if 500 <= e.response.status_code < 600:
                print(f"Retry {attempt+1}/{retries}")
                logging.info(f"Retry {attempt+1}/{retries}")
                sleep(backoff_factor ** attempt)
            else:
                raise
    raise Exception("Failed to fetch embeddings after multiple retries.")

@app.route('/api/save-chat-history', methods=['POST'])
def save_chat_history():
    # Parse request data
    data = request.json
    user_name = data.get('user_name')
    query_question = data.get('query_question')
    accessed_docs = data.get('accessed_docs')
    answer = data.get('answer')
    answer_time=data.get('timestamp')
    # Validate the presence of all required fields
    if not all([user_name, query_question, answer]):
        return jsonify({'error': 'Missing data for saving chat history'}), 400

    try:
        # Create a new ChatHistory record
        new_record = ChatHistory(
            user_name=user_name,
            query_question=query_question,
            accessed_docs=accessed_docs,  # Optional, can be None
            answer=answer,
            answer_time=answer_time
        )
        
        # Save the new record to the database
        db.session.add(new_record)
        db.session.commit()
        
        return jsonify({'message': 'Chat history saved successfully', 'query_id': new_record.query_id}), 200
    except Exception as e:
        # Log the exception and rollback the session
        app.logger.error(f'Error saving chat history: {e}')
        db.session.rollback()
        return jsonify({'error': 'Could not save chat history'}), 500



# @app.route('/api/chathistory/<username>', methods=['GET'])
# def get_chat_history(username):
#     history = ChatHistory.query.filter_by(user_name=username).all()
#     result = [{
#         'query_id': h.query_id,
#         'query_question': h.query_question,
#         'accessed_docs': h.accessed_docs,
#         'answer': h.answer,
#         'answer_time': h.answer_time.isoformat()  # Ensuring time is serialized properly
#     } for h in history]
#     return jsonify(result)

@app.route('/api/upload', methods=['POST'])
def upload_document():
    data = request.get_json()
    content = data.get('content')
    doc_name = data.get('docName')
    user_id = data.get('userId')  # Assuming you pass userId somehow or extract it from session
    doc_kind = data.get('docKind')  # This should be passed from the frontend

    if content and doc_name:
        # Fetch the user's name using the user_id
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "Invalid user ID"}), 400
        
        # Create and save the document
        new_document = Document(
            doc_name=doc_name,
            txt_content=content,
            txt_uploader_id=user_id,
            txt_uploader_name=user.user_name,  # Using the fetched user's name
            txt_kind=doc_kind  # Use the document kind passed from the frontend
        )
        db.session.add(new_document)
        db.session.commit()
        
        # Automatically grant access to the uploader
        new_access = DocumentAccess(
            user_id=user_id,
            doc_id=new_document.doc_id,
            access_right=True
        )
        db.session.add(new_access)
        db.session.commit()

        return jsonify({"message": "Document uploaded successfully", "doc_id": new_document.doc_id}), 201
    else:
        return jsonify({"error": "No content or document name provided"}), 400


@app.route('/api/submit-feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    user_name = data.get('user_name')  # We are using username instead of user_id
    feedback_content = data.get('feedback')
    fb_time=data.get('fb_time')

    if not user_name or not feedback_content:
        return jsonify({'error': 'Missing feedback content or user name'}), 400

    try:
        # Fetch the user by name
        user = User.query.filter_by(user_name=user_name).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        new_feedback = Feedback(feedback_name=user.user_name, feedback_content=feedback_content,feedback_createtime=fb_time)
        db.session.add(new_feedback)
        db.session.commit()
        return jsonify({'message': 'Feedback submitted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error submitting feedback: {e}')
        return jsonify({'error': str(e)}), 500
def clean_text(text):
    cleaned_text = re.sub(r'\[\d+\]', '', text)  # 去除索引标记
    cleaned_text = ' '.join(cleaned_text.split())  # 去除空格和换行符
    return cleaned_text

@app.route('/api/scrape', methods=['POST'])
def scrape_website():
    try:
        url = request.json.get('url')
        response = requests.get(url, timeout=10)  # 10 seconds timeout
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        cleaned_text = clean_text(text)
        return jsonify({"content": cleaned_text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
pdb.set_trace()


if __name__ == '__main__':
    from app import db
    with app.app_context():
        # Dangerous to use in production! Use only in a controlled dev environment
        db.drop_all()  # Drop all tables
        db.create_all()  # Recreate tables based on models
    app.run(debug=True)