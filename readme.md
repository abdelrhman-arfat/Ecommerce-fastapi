## Read :

- I will not complete because i won't learn new i add the important
- things like auth ,jwt ,Oauth will be the same in nodejs create session
- and convert the user to the login url and after sucess to client url
- stripe after add to chart and buy first checking the products and make session with products info and convert the user to this session
- admin pannel will be by grouping the tables to collect money

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
