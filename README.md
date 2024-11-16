# README - User and Admin API Documentation

This README provides an overview and documentation for the **User and Admin API** that manages user registration, login, assignment uploads, and task management using a MongoDB database. The API is deployed on **Render** and can be accessed remotely via the endpoint:

### **Deployed Backend URL:**
[https://assignment-submission-bym9.onrender.com](https://assignment-submission-bym9.onrender.com)

For local development, the API can also be accessed at:

### **Local Backend URL (for testing on your machine):**
[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## **Technologies Used**
- **Flask** - Web framework for building REST APIs.
- **MongoDB** - NoSQL database to store user and assignment data.
- **Flask-JWT-Extended** - For secure JWT-based authentication.
- **Werkzeug** - For password hashing and validation.
- **MongoEngine** - ODM (Object-Document Mapper) for interacting with MongoDB.
- **Flask-RESTx** - For building and managing the RESTful API structure.

---

## **How to Use the API**

The API is available for access at the following base URL:

- **Base URL for all API endpoints**: `https://assignment-submission-bym9.onrender.com` (for the deployed version)

Or, if you're working locally on your machine, the base URL is:

- **Local URL for all API endpoints**: `http://127.0.0.1:5000` (for local testing)

To access the API, make sure to include a valid **JWT access token** in the request headers. The token can be obtained by logging in as a **user** or **admin** via the `/user/login` or `/admin/login` endpoints.

---

## **Managing Access Tokens**

The **JWT access token** is required for **authenticated requests**. Here is how you can manage and use the access token in the headers:

### **1. Get an Access Token**

- **For Users**: Call the `/user/login` endpoint with your username and password to get an access token.
- **For Admins**: Call the `/admin/login` endpoint with your username and password to get an access token.

### **2. Include Access Token in the Request Headers**

Once you obtain the access token, include it in the `Authorization` header as a `Bearer` token in your requests to access protected routes.

#### Example:
```http
GET /admin/assignments HTTP/1.1
Host: assignment-submission-bym9.onrender.com
Authorization: Bearer YOUR_JWT_TOKEN
```

- Replace `YOUR_JWT_TOKEN` with the actual token returned from the login API.
- The `Authorization` header is required for all routes that are protected by authentication.

---

## **User API Endpoints**

### 1. **User Registration** (`POST /user/register`)

This endpoint registers a new user. The user needs to provide a `username`, `email`, and `password`.

#### Request URL (Deployed):
`https://assignment-submission-bym9.onrender.com/user/register`

#### Request URL (Local):
`http://127.0.0.1:5000/user/register`

#### Request Body:
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

#### Response:
- **200 OK**: User successfully registered.
- **400 Bad Request**: If the username or email is missing, or if they already exist in the database.

---

### 2. **User Login** (`POST /user/login`)

This endpoint allows users to log in by providing their `username` and `password`. A JWT token will be returned upon successful login.

#### Request URL (Deployed):
`https://assignment-submission-bym9.onrender.com/user/login`

#### Request URL (Local):
`http://127.0.0.1:5000/user/login`

#### Request Body:
```json
{
  "username": "string",
  "password": "string"
}
```

#### Response:
- **200 OK**: Login successful and access token generated.
- **400 Bad Request**: If username or password is incorrect.
- **500 Internal Server Error**: If there’s an issue with the server.

---

### 3. **Upload Assignment** (`POST /user/upload`)

This endpoint allows authenticated users to upload assignments. The user must provide the `task` and `admin` to whom the assignment is related.

#### Request URL (Deployed):
`https://assignment-submission-bym9.onrender.com/user/upload`

#### Request URL (Local):
`http://127.0.0.1:5000/user/upload`

#### Request Body:
```json
{
  "task": "string",
  "admin": "admin_username"
}
```

#### Response:
- **200 OK**: Assignment uploaded successfully.
- **400 Bad Request**: If `task` or `admin` fields are missing.

---

### 4. **Fetch All Admins** (`GET /user/all-admin`)

This endpoint retrieves a list of all registered admins. Only an authenticated user with valid credentials can access this endpoint.

#### Request URL (Deployed):
`https://assignment-submission-bym9.onrender.com/user/all-admin`

#### Request URL (Local):
`http://127.0.0.1:5000/user/all-admin`

#### Response:
- **200 OK**: Returns a list of all admins.
- **403 Forbidden**: If the current user is not authorized.

---

## **Admin API Endpoints**

### 1. **Admin Registration** (`POST /admin/register`)

This endpoint allows an admin to register by providing their `username`, `email`, and `password`.

#### Request URL (Deployed):
`https://assignment-submission-bym9.onrender.com/admin/register`

#### Request URL (Local):
`http://127.0.0.1:5000/admin/register`

#### Request Body:
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

#### Response:
- **200 OK**: Admin successfully registered.
- **400 Bad Request**: If the username or email is missing, or if they already exist in the database.

---

### 2. **Admin Login** (`POST /admin/login`)

This endpoint allows admins to log in by providing their `username` and `password`. A JWT token will be returned upon successful login.

#### Request URL (Deployed):
`https://assignment-submission-bym9.onrender.com/admin/login`

#### Request URL (Local):
`http://127.0.0.1:5000/admin/login`

#### Request Body:
```json
{
  "username": "string",
  "password": "string"
}
```

#### Response:
- **200 OK**: Login successful and access token generated.
- **400 Bad Request**: If username or password is incorrect.
- **500 Internal Server Error**: If there’s an issue with the server.

---

### 3. **View Assignments** (`GET /admin/assignments`)

This endpoint allows authenticated admins to view all assignments that are assigned to them. Admins can view the user’s name, task, and the assignment status.

#### Request URL (Deployed):
`https://assignment-submission-bym9.onrender.com/admin/assignments`

#### Request URL (Local):
`http://127.0.0.1:5000/admin/assignments`

#### Response:
- **200 OK**: List of assignments for the admin.
- **403 Forbidden**: If the current user is not an admin.
- **404 Not Found**: If no assignments are found for the admin.

---

### 4. **Accept Assignment** (`POST /admin/assignments/<assign_id>/accept`)

This endpoint allows an admin to accept a pending assignment by its `assign_id`.

#### Request URL (Deployed):
`https://assignment-submission-bym9.onrender.com/admin/assignments/<assign_id>/accept`

#### Request URL (Local):
`http://127.0.0.1:5000/admin/assignments/<assign_id>/accept`

#### Response:
- **200 OK**: Assignment accepted successfully.
- **400 Bad Request**: If the assignment has already been processed (accepted or rejected).
- **403 Forbidden**: If the admin is not authorized to accept the assignment.
- **404 Not Found**: If the assignment does not exist.

---

### 5. **Reject Assignment** (`POST /admin/assignments/<assign_id>/reject`)

This endpoint allows an admin to reject a pending assignment by its `assign_id`.

#### Request URL (Deployed):
`https://assignment-submission-bym9.onrender.com/admin/assignments/<assign_id>/reject`

#### Request URL (Local):
`http://127.0.0.1:5000/admin/assignments/<assign_id>/reject`

#### Response:
- **200 OK**: Assignment rejected successfully.
- **400 Bad Request**: If the assignment has already been processed (accepted or rejected).
- **403 Forbidden**: If the admin is not authorized to reject the assignment.
- **404 Not Found**: If the assignment does not exist.

---

## **Managing Access Tokens**

To manage **JWT access tokens** properly:

1. **Login** via

 `/user/login` or `/admin/login` to obtain a token.
2. **Store** the token securely (e.g., in localStorage or HTTPOnly cookies) for subsequent requests.
3. **Include** the token in the `Authorization` header as `Bearer <your_token>` for all protected routes.
4. **Logout** by simply discarding the token, as JWT tokens are stateless.

---


## **Models Overview**

### `AssignUser`
Represents a user or admin in the system. It contains fields such as `username`, `email`, `password`, `user_type` (either "user" or "admin"), and `access_token` for JWT authentication.

### `Assignment`
Represents an assignment that is uploaded by a user. It contains fields such as `task`, `admin` (who the task is assigned to), `submitted_at`, and `status` (which can be "pending", "accepted", or "rejected").

---

## **Database Models**

- **AssignUser Model**:
    - `user_id` (string): Unique identifier for each user.
    - `username` (string): The username of the user or admin.
    - `email` (string): The email of the user.
    - `password` (string): The password (hashed).
    - `user_type` (string): The type of user (either `user` or `admin`).
    - `access_token` (string): JWT token used for authentication.
    - `created_at` (datetime): Timestamp of when the user was created.

- **Assignment Model**:
    - `assign_id` (string): Unique identifier for each assignment.
    - `user` (ReferenceField): The user who uploaded the assignment.
    - `task` (string): The task description.
    - `admin` (string): The admin to whom the assignment is assigned.
    - `submitted_at` (datetime): Timestamp of when the assignment was uploaded.
    - `status` (string): The current status of the assignment (pending, accepted, rejected).

---

## **Authentication**
- All endpoints under `/admin/*` and `/user/upload` require a valid JWT token in the `Authorization` header.
- Use the `/user/login` or `/admin/login` endpoint to obtain a token.

---

## **Conclusion**

This API provides endpoints for both **users** and **admins** to interact with assignments. Users can upload assignments and view available admins, while admins can manage the assignments, accept or reject them. Access to these endpoints is controlled via **JWT authentication** to ensure security.

For any questions or issues, feel free to reach out to the team.
