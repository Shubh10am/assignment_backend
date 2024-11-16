# README - User and Admin API Documentation

This README provides an overview and documentation for the **User and Admin API** that manages user registration, login, assignment uploads, and task management using a MongoDB database. The API is designed using **Flask**, **Flask-RESTx**, and **Flask-JWT-Extended** for handling authentication and data validation.

---

## **Technologies Used**
- **Flask** - Web framework for building REST APIs.
- **MongoDB** - NoSQL database to store user and assignment data.
- **Flask-JWT-Extended** - For secure JWT-based authentication.
- **Werkzeug** - For password hashing and validation.
- **MongoEngine** - ODM (Object-Document Mapper) for interacting with MongoDB.
- **Flask-RESTx** - For building and managing the RESTful API structure.

---

## **User API Endpoints**

### 1. **User Registration** (`POST /user/register`)
This endpoint registers a new user. The user needs to provide a `username`, `email`, and `password`.

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

Example Response:
```json
{
  "status": "success",
  "code": 200,
  "message": "User Successfully Registered",
  "data": {
    "user_id": "user123",
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

---

### 2. **User Login** (`POST /user/login`)
This endpoint allows users to log in by providing their `username` and `password`. A JWT token will be returned upon successful login.

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

Example Response:
```json
{
  "status": "success",
  "code": 200,
  "message": "Login Successfully",
  "data": {
    "user_id": "user123",
    "username": "john_doe",
    "access_token": "your_jwt_token"
  }
}
```

---

### 3. **Upload Assignment** (`POST /user/upload`)
This endpoint allows authenticated users to upload assignments. The user must provide the `task` and `admin` to whom the assignment is related.

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

Example Response:
```json
{
  "status": "success",
  "code": 200,
  "message": "Assignment uploaded successfully!",
  "data": {
    "task": "Complete the report"
  }
}
```

---

### 4. **Fetch All Admins** (`GET /user/all-admin`)
This endpoint retrieves a list of all registered admins. Only an authenticated user with valid credentials can access this endpoint.

#### Response:
- **200 OK**: Returns a list of all admins.
- **403 Forbidden**: If the current user is not authorized.

Example Response:
```json
{
  "status": "success",
  "code": 200,
  "message": "All Admin List",
  "data": [
    {"username": "admin1"},
    {"username": "admin2"}
  ]
}
```

---

## **Admin API Endpoints**

### 1. **Admin Registration** (`POST /admin/register`)
This endpoint allows an admin to register by providing their `username`, `email`, and `password`.

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

Example Response:
```json
{
  "status": "success",
  "code": 200,
  "message": "User Successfully Registered",
  "data": {
    "user_id": "admin123",
    "username": "admin_user",
    "email": "admin@example.com"
  }
}
```

---

### 2. **Admin Login** (`POST /admin/login`)
This endpoint allows admins to log in by providing their `username` and `password`. A JWT token will be returned upon successful login.

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

Example Response:
```json
{
  "status": "success",
  "code": 200,
  "message": "Login Successfully Admin Panel",
  "data": {
    "user_id": "admin123",
    "username": "admin_user",
    "access_token": "your_jwt_token"
  }
}
```

---

### 3. **View Assignments** (`GET /admin/assignments`)
This endpoint allows authenticated admins to view all assignments that are assigned to them. Admins can view the user’s name, task, and the assignment status.

#### Response:
- **200 OK**: List of assignments for the admin.
- **403 Forbidden**: If the current user is not an admin.
- **404 Not Found**: If no assignments are found for the admin.

Example Response:
```json
{
  "status": "success",
  "code": 200,
  "message": "Assignments fetched successfully",
  "data": [
    {
      "user_name": "user123",
      "task": "Complete report",
      "assign_id": "assign001",
      "submitted_at": "2024-11-16 10:30:00",
      "status": "pending"
    }
  ]
}
```

---

### 4. **Accept Assignment** (`POST /admin/assignments/<assign_id>/accept`)
This endpoint allows an admin to accept a pending assignment by its `assign_id`. 

#### Response:
- **200 OK**: Assignment accepted successfully.
- **400 Bad Request**: If the assignment has already been processed (accepted or rejected).
- **403 Forbidden**: If the admin is not authorized to accept the assignment.
- **404 Not Found**: If the assignment does not exist.

Example Response:
```json
{
  "status": "success",
  "code": 200,
  "message": "Assignment assign001 accepted successfully"
}
```

---

### 5. **Reject Assignment** (`POST /admin/assignments/<assign_id>/reject`)
This endpoint allows an admin to reject a pending assignment by its `assign_id`.

#### Response:
- **200 OK**: Assignment rejected successfully.
- **400 Bad Request**: If the assignment has already been processed (accepted or rejected).
- **403 Forbidden**: If the admin is not authorized to reject the assignment.
- **404 Not Found**: If the assignment does not exist.

Example Response:
```json
{
  "status": "success",
  "code": 200,
  "message": "Assignment assign001 rejected successfully"
}
```

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
This API provides full functionality for users and admins

 to manage tasks and assignments. It uses JWT for secure authentication, MongoDB for data storage, and Flask for handling the web framework and APIs.
