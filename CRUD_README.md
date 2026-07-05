# Product CRUD System

A complete CRUD (Create, Read, Update, Delete) system for managing products built with FastAPI and MongoDB.

## Features

- ✅ **Create** - Add new products
- ✅ **Read** - Retrieve single or multiple products with pagination
- ✅ **Update** - Modify existing products
- ✅ **Delete** - Remove products
- 🔍 **Search** - Search products by title or description
- 💰 **Filter** - Filter products by price range

## API Endpoints

### Base URL

```
/api/v1/products
```

### Endpoints

| Method | Endpoint                                             | Description                          |
| ------ | ---------------------------------------------------- | ------------------------------------ |
| POST   | `/products`                                          | Create a new product                 |
| GET    | `/products`                                          | Get all products (with pagination)   |
| GET    | `/products/{product_id}`                             | Get a single product by ID           |
| PUT    | `/products/{product_id}`                             | Update a product                     |
| DELETE | `/products/{product_id}`                             | Delete a product                     |
| GET    | `/products/search/query?q=...`                       | Search products by title/description |
| GET    | `/products/filter/price?min_price=...&max_price=...` | Filter by price range                |

## Request/Response Examples

### Create Product

```bash
POST /api/v1/products
Content-Type: application/json

{
  "title": "Laptop",
  "description": "High-performance gaming laptop",
  "stock": 5,
  "price": 50000,
  "discount": 10,
  "images": ["image1.jpg", "image2.jpg"]
}
```

**Response (201 Created):**

```json
{
  "_id": "660abc123def456789",
  "title": "Laptop",
  "description": "High-performance gaming laptop",
  "stock": 5,
  "price": 50000,
  "discount": 10,
  "images": ["image1.jpg", "image2.jpg"],
  "created_at": "2024-03-30T12:00:00"
}
```

### Get All Products

```bash
GET /api/v1/products?skip=0&limit=10
```

**Response (200 OK):**

```json
[
  {
    "id": "660abc123def456789",
    "_id": "660abc123def456789",
    "title": "Laptop",
    "price": 50000,
    "stock": 5,
    ...
  }
]
```

### Get Single Product

```bash
GET /api/v1/products/660abc123def456789
```

### Update Product

```bash
PUT /api/v1/products/660abc123def456789
Content-Type: application/json

{
  "title": "Gaming Laptop Pro",
  "price": 55000,
  "stock": 4,
  ...
}
```

### Delete Product

```bash
DELETE /api/v1/products/660abc123def456789
```

**Response (200 OK):**

```json
{
  "message": "Product deleted successfully",
  "product": { ... }
}
```

### Search Products

```bash
GET /api/v1/products/search/query?q=laptop&skip=0&limit=10
```

### Filter by Price

```bash
GET /api/v1/products/filter/price?min_price=10000&max_price=50000&skip=0&limit=10
```

## Project Structure

```
backend/
├── main.py                          # FastAPI app entry point
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── config.py               # Settings configuration
│   │   └── mongoDB.py              # MongoDB connection
│   ├── models/
│   │   ├── __init__.py
│   │   └── db_schemas/
│   │       ├── __init__.py
│   │       ├── product.py          # Product model
│   │       └── conversation.py     # Pydantic utilities
│   ├── controllers/
│   │   ├── BaseController.py       # Base controller
│   │   └── ProductController.py    # Product CRUD logic
│   └── routes/
│       ├── __init__.py
│       ├── base.py                 # Base routes
│       └── products.py             # Product API routes
```

## Environment Variables

Required in `.env`:

```
APP_NAME=Product System
APP_VERSION=1.0.0

MONGODB_USERNAME=your_username
MONGODB_PASSWORD=your_password
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/?retryWrites=true&w=majority

FILE_MAX_SIZE=5242880
FILE_ALLOWED_IMAGES_TYPES=["jpg", "png", "jpeg", "gif", "webp"]

UPLOAD_DIR=uploads
```

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn main:app --reload

# The API will be available at http://localhost:8000
# Interactive API docs: http://localhost:8000/docs
```

## Product Model Validation

- **title**: 3-30 characters (required)
- **description**: Optional text
- **stock**: Integer (required)
- **price**: Integer (required)
- **discount**: Integer (required)
- **images**: List of image URLs (required)
- **created_at**: Automatically set to current UTC time

## Error Handling

All endpoints return appropriate HTTP status codes:

- `201` - Created (successful POST)
- `200` - OK (successful GET, PUT, DELETE)
- `400` - Bad Request (invalid data or operation)
- `404` - Not Found (product doesn't exist)
- `500` - Internal Server Error

Error responses include a detail message:

```json
{
  "detail": "Product not found"
}
```

## Features Included

✅ Full CRUD operations  
✅ MongoDB integration  
✅ Pydantic validation  
✅ Pagination support  
✅ Search functionality  
✅ Price filtering  
✅ Error handling  
✅ Dependency injection  
✅ Auto-generated API documentation
