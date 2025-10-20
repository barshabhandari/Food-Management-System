# Annapurna

Annapurna is a FastAPI-based e-commerce application built with Python, SQLAlchemy, and SQLite. It provides a RESTful API for managing products, users, categories, carts, payments, and images.

## Features

- User authentication and authorization
- Product management with categories
- Shopping cart functionality
- Payment processing
- Image upload and management
- SQLite database for easy setup and deployment

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd annapurna
   ```

2. Create a virtual environment:
   ```
   python -m venv venv_new
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv_new\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv_new/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirement.txt
   ```

## Database Setup

The application uses SQLite as the default database. The database file `annapurna.db` will be created automatically when you run the application.

To initialize the database tables:
```
python -c "from app.database import engine; from app.modules.product import models; from app.modules.user import models as user_models; from app.modules.cart import models as cart_models; from app.modules.image import models as image_models; from app.modules.category import models as category_models; models.Base.metadata.create_all(bind=engine); user_models.Base.metadata.create_all(bind=engine); cart_models.Base.metadata.create_all(bind=engine); image_models.Base.metadata.create_all(bind=engine); category_models.Base.metadata.create_all(bind=engine)"
```

## Running the Application

1. Start the FastAPI server:
   ```
   uvicorn app.main:app --reload
   ```

2. Open your browser and navigate to `http://127.0.0.1:8000`

3. For API documentation, visit `http://127.0.0.1:8000/docs` (Swagger UI) or `http://127.0.0.1:8000/redoc` (ReDoc)

## API Endpoints

The application provides the following main endpoints:

- `/users` - User management
- `/auth` - Authentication
- `/products` - Product management
- `/categories` - Category management
- `/cart` - Shopping cart
- `/images` - Image upload and management
- `/payments` - Payment processing

## Project Structure

```
annapurna/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── modules/
│   │   ├── auth/
│   │   ├── user/
│   │   ├── product/
│   │   ├── category/
│   │   ├── cart/
│   │   ├── image/
│   │   ├── payment/
│   │   └── oauth2/
│   └── utils/
├── alembic/
├── static/
├── venv_new/
├── .gitignore
├── README.md
├── requirement.txt
└── annapurna.db
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests (if available)
5. Submit a pull request

## License

This project is licensed under the MIT License.
