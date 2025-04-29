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
OPEN_WEATHER_API_KEY=YOUR_OPEN_WEATHER_API_KEY
```

### 3. Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate    # For Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Access the FastAPI Application
# http://localhost:8000
```