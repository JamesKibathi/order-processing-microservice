# e-commerce-service
Online Shop With Django

# E-Commerce Service API

This is a Python-based E-Commerce service API built with **Django Rest Framework (DRF)**. It enables customers to place orders, authenticate via **Auth0**, and manage product and order data. This API also provides integration with **Africa's Talking SMS API** for order notifications and email notifications for the admin.

## Features:
  - **Customer Authentication**: Auth0 OpenID Connect integration to authenticate users.
  - **Order Management**: Customers can place orders with product quantities.
  - **Order Notifications**:
      - **SMS**: Customers receive SMS notifications for order updates using **Africa's Talking SMS API**.
      - **Email**: Admins are notified via email when a new order is placed.
  - **Hierarchical Categories**: Categories store a product hierarchy, allowing easy organization of products.
  - **Containerized with Docker**: The project is containerized for easy deployment and scaling using **Docker**.
  - **Kubernetes (Minikube)**: Infrastructure as a Service (IaaS) with Kubernetes for scaling and management.
  - **CI/CD with GitHub Actions**: Automated deployment and testing using GitHub Actions.
  - **PostgreSQL**: Uses PostgreSQL as the database for storing product, customer, and order data.

## Tools and Technologies:
  - **Django Rest Framework** (DRF) for building the API
  - **PostgreSQL** for the database
  - **Auth0** for customer authentication (via OpenID Connect)
  - **Africa's Talking SMS API** for SMS notifications
  - **Django Mailer** and **SMTP** for sending email notifications
  - **Docker** for containerization
  - **GitHub Actions** for CI/CD pipeline
  - **Kubernetes (Minikube)** for Infrastructure as a Service (IaaS)

## Authentication Flow:
  1. **Auth0 Authentication**: Customers authenticate using their credentials via Auth0.
  2. **Access Token**: Upon successful authentication, an **access token** is generated and stored for the customer.
  3. **Order Placement**:
      - The customer places an order by specifying products, quantities, and their **phone number**.
      - An order is placed by sending a request to the API with the **access token**.
  4. **Customer Creation**: A **Customer** instance is created or updated with the provided phone number.
  5. **Notifications**:
      - The **customer** receives an SMS notification about the order.
      - **Admins** are notified via email when a new order is placed.

## Requirements:
  - **Clone the repository**:
      ```bash
      git clone https://github.com/yourusername/ecommerce-service-api.git
      cd ecommerce-service-api
      ```
  - **Set up your environment**:
      - Install the dependencies:
        ```bash
        pip install -r requirements.txt
        ```
      - Set up your `.env` file for sensitive configurations:
        - **Africa's Talking**: Set your **shortcode**, **API key**, and **API secret** for SMS notifications.
        - **Auth0**: Set your **client ID**, **client secret**, **domain**, and **identifier**.
      
      Example `.env` file:
      ```env
      AFRICA_TALKING_API_KEY=your_api_key
      AFRICA_TALKING_API_SECRET=your_api_secret
      AFRICA_TALKING_SHORTCODE=your_shortcode

      AUTH0_CLIENT_ID=your_client_id
      AUTH0_CLIENT_SECRET=your_client_secret
      AUTH0_DOMAIN=your_auth0_domain
      AUTH0_IDENTIFIER=your_auth0_identifier
      ```

  - **Docker Setup**:
      - Build the Docker container:
        ```bash
        docker-compose build
        ```
      - Start the container:
        ```bash
        docker-compose up
        ```

  - **Kubernetes Setup** (using Minikube):
      - Start Minikube:
        ```bash
        minikube start
        ```
      - Apply the Kubernetes configurations:
        ```bash
        kubectl apply -f k8s/
        ```

  - **GitHub Actions**:
      - The CI/CD pipeline is configured to deploy and test the application automatically. Ensure you have your secrets configured in GitHub.

## API Endpoints:

### 1. **Order Endpoints**:
  - **POST /api/v1/orders/**: Place an order
    - **Request**:
      ```json
      {
        "items": [
          {
            "product": "product_id",
            "quantity": 2
          },
          {
            "product": "product_id_2",
            "quantity": 1
          }
        ],
        "phone_number": "+1234567890"
      }
      ```
    - **Response**:
      ```json
      {
        "id": "order_id",
        "customer": "customer_id",
        "items": [
          {
            "product": "product_id",
            "quantity": 2
          }
        ],
        "status": "pending"
      }
      ```

### 2. **Authentication Endpoints**:
  - **POST /api/v1/auth/login**: Login using Auth0 credentials and get the access token.

### 3. **Product Endpoints**:
  - **GET /api/v1/products/**: List all products.
  - **POST /api/v1/products/**: Add a new product.

### 4. **Category Endpoints**:
  - **GET /api/v1/categories/**: List all categories.
  - **POST /api/v1/categories/**: Create a new category.

### 5. **Customer Endpoints**:
  - **GET /api/v1/customers/**: List all customers.
  - **POST /api/v1/customers/**: Create or update customer details.

## Sample Swagger UI:
  ![Swagger UI](./swagger_image.png)

## Contribution:
Feel free to fork and contribute to this project. If you have any improvements or bug fixes, please create a pull request.
