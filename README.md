# LangChain Project Assistant

A full-stack AI-powered project management assistant that lets you track and manage your projects, tasks, and team assignments through a conversational chat interface.

---

## 🚀 Features

- **Conversational Project Management:**  
  Ask questions like:
  - “What tasks are pending?”
  - “What is Project Alpha ending date?”
  - “Who is assigned the most tasks?”
- **AI-Powered Answers:**  
  Uses LangChain and Google Generative AI for natural language understanding and retrieval.
- **Modern UI:**  
  Built with Next.js, TypeScript, and TailwindCSS for a responsive chat experience.
- **Robust Backend:**  
  FastAPI, SQLAlchemy, and FAISS for scalable, efficient data and AI operations.
- **Cloud Database:**  
  Uses NeonDB (PostgreSQL) for persistent, cloud-hosted storage.

---

## 🗂️ Project Structure Overview

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

---

## 🧠 Tech Stack

- **Frontend:** Next.js, TypeScript, TailwindCSS
- **Backend:** FastAPI, LangChain, SQLAlchemy, FAISS
- **Database:** PostgreSQL (NeonDB cloud)
- **AI:** Google Generative AI Embeddings, LangChain, FAISS (vector search)

---

## 🛠️ Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/harsha-1807/LangChain-Project-Assistant.git
cd LangChain-Project-Assistant
```

### 2. Backend Setup

```sh
cd Backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

- Create a `.env` file in `Backend/` with your NeonDB connection string:
  ```
  DATABASE_URL=postgresql+psycopg2://<user>:<password>@<host>/<dbname>
  GOOGLE_API_KEY = your_googleApi_key
  ```

- Start the FastAPI server:
  ```sh
  uvicorn app.main:app --reload
  ```

### 3. Frontend Setup

```sh
cd langchain-chat
npm install
npm run dev
```

- Open [http://localhost:3000](http://localhost:3000) to use the chat UI.

---

## 💬 Example Questions

- **Pending Tasks:**  
  _“What tasks are pending?”_
- **Project Status:**  
  _“What is Project Alpha ending date?”_
- **Top Assignee:**  
  _“Who is assigned the most tasks?”_

---

## 🤖 How It Works

-   **User** interacts with the chat UI (Next.js).
-   **Frontend** sends questions to the FastAPI backend.
-   **Backend** leverages **LangChain** to:
    * **Embed** your database's project, task, and user data into a **FAISS vector store** using **Google's `gemini-embedding-001`**.
    * Perform **similarity search** to retrieve relevant context for the user's query.
    * Utilize **Google's `gemini-2.5-flash` LLM** to generate answers based on the retrieved context.
-   **Database** stores all project, task, and user information.

---

## 📦 Key Dependencies

- **Frontend:**  
  - next, react, tailwindcss
- **Backend:**  
  - check requirements.txt file

---

## 🙏 Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain)
- [FastAPI](https://fastapi.tiangolo.com/)
- [NeonDB](https://neon.tech/)
- [Next.js](https://nextjs.org/)
- [FAISS](https://github.com/facebookresearch/faiss)

---

**Build your own AI project assistant and supercharge your productivity!**
