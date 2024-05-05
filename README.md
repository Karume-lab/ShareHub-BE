# SHAREHUB BACKEND

## SET UP GUIDE

**1. Clone the Repo:**

```bash
git clone https://github.com/Karume-lab/ShareHub-BE
```

**2. Create a Virtual Environment:**

```bash
python -m venv venv
```

**3. Activate Virtual Environment:**

**- Linux:**

```bash
source ./venv/bin/activate
```

**- Windows:**

```bash
venv\Scripts\activate
```

**4. Install Python Packages:**

```bash
pip install -r requirements.txt
```

**5. Create `.env` from `.env.example`:**

- Need help creating the file? Watch this video for guidance: [How to Create an App Password](https://www.youtube.com/watch?v=hXiPshHn9Pw&pp=yg93IHRvIGNyZWF0ZSBhcHAgcGFzc3dvcmQgZ29vZ2xl)
- Fill in the Gmail account and app password in the first two fields.
- Set the third field to `True`.

**6. Make Migrations:**

```bash
python manage.py makemigrations && python manage.py migrate
```

**7. Run the Server:**

```bash
python manage.py runserver
```

**8. API Documentation:**

Navigate to either of these URLs:

- [Swagger Documentation](http://127.0.0.1:8000/swagger/)
- [Redoc Documentation](http://127.0.0.1:8000/redoc/)
