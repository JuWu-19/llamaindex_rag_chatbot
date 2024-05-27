## LlamaIndex-based and LLM-powered Q&A Management System
 
### Introduction
This project is a Q&A management system leveraging the LlamaIndex and large language models (LLMs) to provide an intelligent, retrieval-augmented generation (RAG) based chatbot. The system integrates multiple components, including backend services and a frontend user management system, to deliver a robust and scalable solution for querying a knowledge base.

### Backend Components

### RAG Q&A Engine
**Functionalities:**
1. **Embed**: Convert text data into vector representations using embedding models.
2. **Index**: Optimize search by indexing these embeddings.
3. **Query Embedding**: Convert user queries into embeddings.
4. **Retrieve**: Fetch relevant document embeddings based on query embeddings.
5. **Generate**: Generate responses using the retrieved documents and the query.

**Description:**
The Q&A engine processes user queries by embedding the query and documents, retrieving the most relevant documents, and generating responses using an LLM. Two indexing methods are considered: integrated and separate indexing, with the latter chosen for its scalability and efficiency.

### Database Integration
**Functionalities:**
1. **User Management**: Handles user registrations, logins, and permissions.
2. **Document Management**: Manages document uploads, access control, and storage.
3. **Feedback Management**: Collects and processes user feedback.
4. **Q&A Records Management**: Stores and manages records of user interactions.

**Description:**
The backend uses PostgreSQL for relational database management, with SQLAlchemy as the ORM and Flask RESTful for creating APIs. Four main tables—Users, Documents, Document_Access, and Feedback—manage user access, document handling, and interaction history.

### Frontend Components

### User Interface
The frontend is built using Vue.js and provides a user-friendly interface for interacting with the Q&A system. Key components include:

1. **LoginPage.vue**: Handles user login functionality.
2. **RegisterPage.vue**: Manages user registration.
3. **HomeView.vue**: The main landing page for users.
4. **UserDashboard.vue**: The dashboard where users can manage their documents (upload & scrape), query, give feedback, and view query results.
5. **AdminLogin.vue**: Admin-specific login interface.
6. **AdminDashboard.vue**: The dashboard for admin users to manage documents access, users, and feedback.
7. **AboutView.vue**: Provides information about the application.
8. **WelcomePage.vue**: Initial welcome page for users.

**Functionalities:**
- **User Authentication**: Secure login and registration for users and admins.
- **Document Upload and Management**: Users can upload documents, get .txt documents by scraping the web, and view/manage them in the dashboard.
- **Admin Controls**: Admins can manage user documents, feedback, and query records.

### Usage

### Global Configuration
1. **Operating System**: Microsoft Windows 11 Pro.
2. **Virtual Environment**: Built using Anaconda for package, library, and dependency management.

**Installation Commands:**
```bash
# Clone the repository
git clone https://github.com/JuWu-19/llamaindex_rag_chatbot.git
cd llamaindex_rag_chatbot

# Setup Backend
cd qa_backend
pip install -r requirements.txt

# Setup Frontend
cd user-management-frontend
npm install
npm run serve
```
### Component-Specific Configuration

### Backend Configuration:
Install necessary packages using:
```bash
pip install llama-index chromadb -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install -U sentence-transformers -i https://pypi.tuna.tsinghua.edu.cn/simple
```
Configure PostgreSQL for database management.

### Frontend Configuration:
Ensure Node.js and Vue CLI are installed.
Use 'vue.config.js' and 'jsconfig.json' for project-specific configurations.

#### Frontend Installation Steps:
Install Node.js and npm.
Install Vue CLI:
```bash
npm install -g @vue/cli
```
Verify Vue CLI installation:
```bash
vue --version
```
Configure project using 'jsconfig.json':
```bash
{
  "compilerOptions": {
    "target": "es5",
    "module": "esnext",
    "baseUrl": "./",
    "moduleResolution": "node",
    "paths": {
      "@/*": ["src/*"]
    },
    "lib": ["esnext", "dom", "dom.iterable", "scripthost"]
  }
}
