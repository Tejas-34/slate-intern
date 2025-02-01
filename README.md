# Django Application with PostgreSQL Setup

## **Prerequisites**

Ensure you have the following installed:

- Python (>= 3.8)
- PostgreSQL & pgAdmin
- pip (Python package manager)
- virtualenv (recommended for isolated environments)
- git (optional)

---

## **1. Clone the Repository**

```bash
git clone https://github.com/Tejas-34/slate-intern.git
cd slate
```

---

## **2. Create and Activate Virtual Environment**

### **Linux/macOS**

```bash
python3 -m venv venv  
source venv/bin/activate  
```

### **Windows**

```bash
python -m venv venv  
venv\Scripts\activate  
```

---

## **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

---

## **4. Configure PostgreSQL in pgAdmin**

1. Open **pgAdmin** and login.
2. Create a new database:
   - Right-click **Databases** → **Create** → **Database**
   - Name it (e.g., `mydatabase`).
   - Set the **Owner** to your PostgreSQL username.
3. Get your **PostgreSQL connection details** (host, port, database name, username, password).

---

## **5. Update ********************************************************************************`settings.py`******************************************************************************** for PostgreSQL**

Modify your `settings.py` database settings:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',  # Replace with your DB name
        'USER': 'your_username',  # Replace with your PostgreSQL username
        'PASSWORD': 'your_password',  # Replace with your PostgreSQL password
        'HOST': 'localhost',  # Change if using a remote DB
        'PORT': '5432',  # Default PostgreSQL port
    }
}
```

---

## **6. Apply Migrations **

```bash
python manage.py migrate  
```

---

## **7. Run the Django Server**

```bash
python manage.py runserver  
```

Visit **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser.

---

## **8. Access Django Admin Panel**

Go to **[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)**\
Login with the superuser credentials created earlier.

\--------------------------------------------------------------------------------


---

## API Endpoints

### `register/`
This endpoint allows users to register by providing their name, email, password, and role.

### `auth/login/`
Users can log in by providing their credentials (email and password) to receive a token.

### `student/achievements/`
With a valid token and proper authentication:

- **Parents** can view the achievements of their related student(s).
- **Students** can view their own achievement data.
- **Schools** can add achievements and view the achievements of all their students.

---

### **Enjoy your Django + PostgreSQL app! 🚀**
