# Sweet Shop - My Awesome Project

## Project Overview
This project is a simple full-stack web application for a sweet shop. It allows users to view available sweets, purchase them, and provides special administrative access for managing the sweets.

## Features

- **User Authentication**: Users can register and log in to the application.
- **Admin Access**: An admin user has special permissions to restock, delete, and add new sweets.
- **Product Management**:
    - Users can see a list of all sweets.
    - Users can purchase sweets, which decreases the quantity.
    - Admins can add new sweets, restock existing sweets, and delete sweets.

## Technologies Used

### Frontend (React)
- **React**: For building the user interface.
- **Vite**: For a fast development environment.
- **State Management**: Using React's `useState` and `useEffect` hooks.

### Backend (Python)
- **FastAPI**: For creating the backend API.
- **SQLAlchemy**: For database management (ORM).
- **SQLite**: The database is stored in a `sweets.db` file.
- **Passlib**: For password hashing.
- **python-jose**: For handling JWT tokens.

## How to Run the Project

1.  **Clone the Repository**
    ```bash
    git clone <https://github.com/ThulasiGopinath/KATA-Sweet-Shop-Management-System.git>
    ```

2.  **Setup Backend**
    - Navigate into the backend directory:
      ```bash
      cd KATA/backend
      ```
    - Activate the virtual environment:
      - For Mac/Linux: `source venv/bin/activate`
      - For Windows (Git Bash): `source venv/Scripts/activate`
    - Start the backend server:
      ```bash
      uvicorn main:app --reload
      ```

3.  **Setup Frontend**
    - Open a new terminal and navigate to the frontend directory:
      ```bash
      cd KATA/frontend
      ```
    - Install dependencies:
      ```bash
      npm install
      ```
    - Start the frontend development server:
      ```bash
      npm run dev
      ```

4.  **Usage**
    - Open your browser and go to `http://localhost:5173`.
    - Register a user with the username 'admin' to test the admin features.
    - Register other users to test the regular user features.