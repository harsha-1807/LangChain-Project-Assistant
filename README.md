# LangChain Project Assistant

**LangChain Project Assistant** is a full-stack, AI-powered project management tool that enables users to track and manage projects, tasks, and team assignments seamlessly through a conversational chat interface.

---

## 🚀 Features

- **Conversational Project Management**  
  Ask natural language questions like:
  - “What tasks are pending?”
  - “Is Project Alpha delayed?”
  - “Who is assigned the most tasks?”
- **AI-Powered Answers**  
  Uses LangChain, Google Generative AI embeddings, and FAISS for semantic search and natural language understanding.
- **Modern and Responsive UI**  
  Built with Next.js, TypeScript, and TailwindCSS for a sleek chat-based interface.
- **Robust Backend**  
  Powered by FastAPI and SQLAlchemy to handle API requests, AI processing, and database operations.
- **Cloud-Hosted Database**  
  Uses NeonDB (PostgreSQL) for persistent, scalable cloud storage.
- **Modular Architecture**  
  Clear separation of frontend, backend, and database layers allows easy customization and maintenance.
- **Ready for Local Development and Cloud Deployment**

---

## 🧰 Tech Stack

| Layer     | Technologies                                  |
|-----------|----------------------------------------------|
| Frontend  | Next.js, TypeScript, React, TailwindCSS     |
| Backend   | FastAPI, LangChain, SQLAlchemy, FAISS       |
| Database  | PostgreSQL (NeonDB cloud-hosted)             |
| AI/Search | Google Generative AI embeddings, LangChain, FAISS |

---

## 📁 Project Structure

```
LangChain-Project-Assistant/
│
├── langchain-chat/         # Frontend (Next.js, TSX, TailwindCSS)
│   ├── app/
│   ├── public/
│   ├── package.json
│   └── ...
│
└── Backend/                # Backend (FastAPI, LangChain, SQLAlchemy)
    ├── app/
    │   ├── main.py
    │   ├── models.py
    │   ├── db.py
    │   ├── routers/
    │   ├── tests/
    │   └── ...
    ├── requirements.txt
    └── ...
```
## 🔗 Deployment Links

- **Frontend:** [https://lang-chain-project-assistant.vercel.app](https://lang-chain-project-assistant.vercel.app)
- **Backend API:** [https://langchain-project-assistant.onrender.com](https://langchain-project-assistant.onrender.com)

---

## 🤖 How It Works

1. **User interacts** with the chat interface in the frontend.  
2. The **frontend sends queries** to the FastAPI backend.  
3. The **backend uses LangChain** and **Google Generative AI** embeddings to embed and semantically search your project data stored in PostgreSQL (NeonDB) using FAISS vector search.  
4. Google’s `gemini-2.5-flash` LLM generates natural language answers based on the retrieved context.  
5. The **assistant responds** conversationally with relevant project and task information.

---
---

## 🚀 Getting Started

### Backend Setup

1. Navigate to backend folder and create a virtual environment:

    ```
    cd Backend
    python -m venv venv
    source venv/bin/activate     # macOS/Linux
    # or
    venv\Scripts\activate        # Windows
    ```

2. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

3. Create a `.env` file inside `Backend/` and add your configuration:

    ```
    DATABASE_URL=postgresql+psycopg2://<user>:<password>@<host>/<dbname>
    GOOGLE_API_KEY=your_google_api_key
    ```

4. Start the backend server (development mode):

    ```
    uvicorn app.main:app --reload
    ```

### Frontend Setup

1. Navigate to frontend folder and install dependencies:

    ```
    cd langchain-chat
    npm install
    ```

2. Create an `.env.local` file in `langchain-chat/`:

    ```
    NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
    ```

3. Run the frontend development server:

    ```
    npm run dev
    ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser to access the chat UI.

---



## 📦 Key Dependencies

- **Frontend:** next, react, tailwindcss  
- **Backend:** fastapi, sqlalchemy, psycopg2-binary, langchain, uvicorn, google-ai-generativelanguage, faiss-cpu, python-dotenv, pytest, and more (see `requirements.txt`)

---

## Resources

- [LangChain](https://github.com/langchain-ai/langchain)  
- [FastAPI](https://fastapi.tiangolo.com/)  
- [NeonDB](https://neon.tech/)  
- [Next.js](https://nextjs.org/)  
- [FAISS](https://github.com/facebookresearch/faiss)

---

**Build your own AI-powered project assistant and supercharge your team productivity!**
