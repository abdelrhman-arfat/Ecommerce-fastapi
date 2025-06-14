# 🛒 E-Commerce Project with FastAPI

## 🚀 Features

- 🔐 **Authentication & Authorization** using OAuth, JWT, and request validation.
- 📦 **Full CRUD Operations** for products, users, and admin features.
- 💳 **Stripe Integration** for secure payment processing.
- 🖼️ **Image Upload & Management** for product images.
- 🛒 **Cart** ,📦 **Orders**, and ✉️ **Email Notifications**.
- 🛠️ **Admin Panel Operations** to manage the platform.

---

## 🧠 Project Structure

```bash
app/
│
├── main.py # Entry point
├── controllers/ # Route logic
├── services/ # Service logic
├── modules/ # Models & schemas
├── middlewares/ # Custom middlewares (auth, etc.)
├── utils/ # Helper functions and services
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```

---

## ⚙️ Running the App

```bash
docker-compose -f docker-compose.yml up  -d --build
```

## Env Var

```env
DATABASE_URL=mysql+pymysql://<username>:<password>@<service_name>/<database_name>
JWT_SECRET_KEY=your_jwt_secret_key
```
