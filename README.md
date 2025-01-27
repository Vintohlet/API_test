# E-commerce API

This API for an online store allows management of products, users, and orders. It uses Flask as the web server and MongoDB as the database.

## Setup and Run Locally

### Requirements

Before running the application locally, make sure you have the following dependencies installed:

- Python 3.8 or higher
- MongoDB (locally or MongoDB Atlas)
- pip

### Steps to Run Locally

1. **Clone the repository**:
   
   Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/your-repository.git
   cd your-repository
Create a virtual environment:

It’s recommended to use a virtual environment to isolate dependencies:

python -m venv venv
Activate the virtual environment:

On Windows:
.\venv\Scripts\activate
On macOS/Linux:
source venv/bin/activate
Install dependencies:

Install all the necessary libraries:


pip install -r requirements.txt
Connect to MongoDB:

Make sure you have access to a MongoDB database. You can either use a local MongoDB instance or MongoDB Atlas for cloud storage.

In the .env file or environment variables, set the connection string:

MONGO_URI=mongodb://127.0.0.1:27017/ecommerce_db
Replace the URL with your own if using MongoDB Atlas.

Run the application:

Start the Flask server:
python app.py
The application will now be available at http://127.0.0.1:5000.

Testing the API
You can use Postman or curl to send requests to the API. Here are the main API endpoints:

POST /products: Add a new product
GET /products: Retrieve a list of all products
GET /products/{product_id}: Get product details by ID
PUT /products/{product_id}: Update product details
DELETE /products/{product_id}: Delete a product by ID
POST /users/register: Register a new user
POST /users/login: Log in a user
POST /orders: Create a new order
GET /orders/{user_id}: Get all orders for a user