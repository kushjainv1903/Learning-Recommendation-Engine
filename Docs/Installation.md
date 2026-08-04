# 🚀 Installation & Setup

# Prerequisites

Before running the project, ensure the following are installed:

- Python 3.11 or later
- Git
- pip (Python Package Manager)

Verify installation:

```bash
python --version
pip --version
```

---

# Clone the Repository

```bash
git clone https://github.com/kushjainv1903/Learning-Recommendation-Engine.git
```

Move into the project:

```bash
cd Learning-Recommendation-Engine
```

---

# Create a Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate:

```powershell
.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

If Uvicorn is not installed globally:

```bash
python -m uvicorn app.main:app --reload
```

---

# Open the API Documentation

Swagger UI:

```
http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

---

# Run the Test Suite

```bash
python -m pytest
```

Expected output:

```
133 passed
```


---

# Troubleshooting

## Module Not Found

Install dependencies again:

```bash
pip install -r requirements.txt
```

---

## Swagger Not Opening

Verify that the FastAPI server is running.

Then open:

```
http://127.0.0.1:8000/docs
```
