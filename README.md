# Certificate Generator 🏆

This project is a full-stack application that generates PDF-based certificates and letters like:

* Appreciation Letter
* Internship Certificate
* Recommendation Letter
* Joining Letter

All documents are created dynamically using user input and styled HTML, converted into PDFs using `wkhtmltopdf`.

---

## 🛠️ Tech Stack

* **Frontend**: React.js
* **Backend**: Flask (Python)
* **PDF Generation**: pdfkit + wkhtmltopdf
* **Deployment**: Render (Free tier, Docker-based backend)

---

## 📁 Folder Structure

```
/
├── backend/        # Flask backend + templates + Docker
├── frontend/       # React app
├── render.yaml     # Render deploy instructions
├── .gitignore
└── README.md
```

---

## 🚀 Local Development

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/purplerain-generator.git
cd purplerain-generator
```

### 2. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Use 'venv\Scripts\activate' on Windows
pip install -r requirements.txt
python app.py
```

### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend
npm install
npm start
```

---

## 🌐 Deployment on Render

1. Push this repo to GitHub.
2. Go to [https://render.com](https://render.com) and sign in.
3. Deploy:

   * **Backend**: as Web Service (Docker)
   * **Frontend**: as Static Site (connect build directory)
4. Set environment variable in frontend:

   ```env
   REACT_APP_API_URL=https://your-backend-name.onrender.com
   ```

---