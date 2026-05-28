🛒 Cartify

Cartify is a lightweight e-commerce backend API built with FastAPI, designed to handle core shopping functionalities such as user authentication, product management, cart operations, and order processing.

This project is built for learning, portfolio development, and future scalability into a full e-commerce platform.

🚀 Features
🔐 User authentication (JWT-based)
👤 Role-based access (User / Admin)
📦 Product management (CRUD)
🛒 Shopping cart system
🧾 Order creation and tracking (basic)
⚡ Fast and scalable REST API using FastAPI
🧱 Tech Stack
Backend: FastAPI
Database: SQLite (development) / PostgreSQL (production-ready)
ORM: SQLAlchemy
Authentication: JWT (JSON Web Tokens)
Validation: Pydantic
Server: Uvicorn
📁 Project Structure
cartify/
│── app/
│   ├── main.py
│   ├── core/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│
│── database.py
│── requirements.txt
│── .env
│── README.md
⚙️ Installation & Setup
1. Clone the repository
git clone https://github.com/yourusername/cartify.git
cd cartify
2. Create virtual environment
python -m venv venv
3. Activate virtual environment

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate
4. Install dependencies
pip install -r requirements.txt
5. Run the server
uvicorn app.main:app --reload
🔐 Environment Variables

Create a .env file:

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./cartify.db
📌 API Endpoints (Basic Overview)
Auth
POST /auth/register → Create user
POST /auth/login → Login user
Products
GET /products → List all products
GET /products/{id} → Get product details
POST /products → Create product (admin)
PUT /products/{id} → Update product (admin)
DELETE /products/{id} → Delete product (admin)
Cart
POST /cart/add
GET /cart
DELETE /cart/remove
Orders
POST /order/checkout
GET /orders
🎯 Project Goals
Build a production-style backend API
Practice real-world database relationships
Learn authentication and authorization
Strengthen FastAPI and backend architecture skills
🚧 Future Improvements
Payment integration (Paystack / Stripe)
Product image uploads (S3 / Cloudinary)
Email notifications
Admin dashboard
Docker deployment
PostgreSQL migration
👨‍💻 Author

Built by Gideon Oyegbami

📜 License

This project is open-source and available for learning and personal development.

If you want next, I can help you:

generate your requirements.txt
build the FastAPI starter code
or design your database models for Cartify

Just tell me 👍
