# Social Network API

## Overview
This Social Network API allows users to register, log in, search for other users, manage friend requests, and view their friends list. The API is built using Django Rest Framework and is containerized using Docker.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Developer-DewPool/social_network.git
    cd social_network
    ```

2. **Build and start the Docker containers:**
    ```bash
    docker-compose up --build
    ```

3. **Run database migrations:**
    ```bash
    docker-compose exec web python manage.py migrate
    ```

4. **Create a superuser (optional, for admin access):**
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

5. **The API will be available at:**
    ```
    http://localhost:8000
    ```

## Features

- User registration and login
- User search by name or email
- User edit profile
- Friend request management (send, accept, reject, delete)
- List of friends and pending friend requests
- Password reset functionality

## Endpoints

### User Authentication

- **Register a new user**
  - **URL:** `POST /api/signup/`
  - **Request Body:**
    ```json
    {
      "username": "user", 
      "email": "user@example.com", 
      "name": "username",
      "gender": "male | female", 
      "password": "yourpassword"
    }
    ```

- **Login a user**
  - **URL:** `POST /api/login/`
  - **Request Body:**
    ```json
    {
      "email": "user@example.com",
      "password": "yourpassword"
    }
    ```

### User Profile

- **Edit Profile**
  - **URL:** `PUT /api/edit-profile/`
  - **Headers:**
    ```json
    {
      "Authorization": "Social_Bearer <token>"
    }
    ```
  - **Request Body:**
    ```json
    {
      "name": "New Name"
    }
    ```

### User Search

- **Search by Name or Email**
  - **URL:** `GET /api/search/?q=email | keyword`
  - **Headers:**
    ```json
    {
      "Authorization": "Social_Bearer <token>"
    }
    ```

### Friend Requests

- **Send a Friend Request**
  - **URL:** `POST /api/friend-request/`
  - **Headers:**
    ```json
    {
      "Authorization": "Social_Bearer <token>",
      "Content-Type": "application/json"
    }
    ```
  - **Request Body:**
    ```json
    {
      "to_user": user_id
    }
    ```

- **List Pending Friend Requests**
  - **URL:** `GET /api/pending-requests/`
  - **Headers:**
    ```json
    {
      "Authorization": "Social_Bearer <token>"
    }
    ```

- **Accept or Reject a Friend Request**
  - **URL:** `PUT /api/friend-request/<id>/`
  - **Headers:**
    ```json
    {
      "Authorization": "Social_Bearer <token>",
      "Content-Type": "application/json"
    }
    ```
  - **Request Body:**
    ```json
    {
      "status": "accepted"
    }
    ```

- **Delete Pending or Accepted Friend Request**
  - **URL:** `DELETE /api/friend-request/<id>/`
  - **Headers:**
    ```json
    {
      "Authorization": "Social_Bearer <token>"
    }
    ```

### Friends

- **List of Friends**
  - **URL:** `GET /api/friends/`
  - **Headers:**
    ```json
    {
      "Authorization": "Social_Bearer <token>"
    }
    ```

### Password Management

- **Reset with Temporary Password**
  - **URL:** `POST /api/reset-password/`
  - **Headers:**
    ```json
    {
      "Authorization": "Social_Bearer <token>",
      "Content-Type": "application/json"
    }
    ```
  - **Request Body:**
    ```json
    {
      "email": "user@example.com"
    }
    ```

- **Update with New Password**
  - **URL:** `PUT /api/reset-password/`
  - **Headers:**
    ```json
    {
      "Authorization": "Social_Bearer <token>",
      "Content-Type": "application/json"
    }
    ```
  - **Request Body:**
    ```json
    {
      "email": "user@example.com",
      "password": "yourpassword"
    }
    ```

## Rate Limiting
Users can send no more than 3 friend requests within a minute to prevent spam.

## Models

### User
- **Fields:**
  - `id`: Integer, primary key
  - `email`: String, unique, required
  - `password`: String, required
  - `name`: String, optional
  - `gender`: String, optional
  - `is_active`: Boolean
  - `is_staff`: Boolean

### FriendRequest
- **Fields:**
  - `id`: Integer, primary key
  - `from_user`: ForeignKey to User
  - `to_user`: ForeignKey to User
  - `status`: String, choices are 'pending', 'accepted', 'rejected'
  - `timestamp`: DateTime

## Postman Collection

A Postman collection for testing all the endpoints is included. Import the `Social Network API.postman_collection.json` file into Postman to get started.

---

This `README.md` provides a comprehensive guide to your API, covering all essential endpoints, setup instructions, and Docker configuration.

