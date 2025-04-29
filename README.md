# gharas-saudi-api

## 🛠 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Mahmood-Anaam/gharas-saudi-api.git
cd gharas-saudi-api
```

### 2. Configure Environment Variables

Create a `.env` file based on `.env.example`:

```plaintext
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

### 3. Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate    # For Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run

```bash
uvicorn main:app --reload

# Access the FastAPI Application
# http://127.0.0.1:8000/
```