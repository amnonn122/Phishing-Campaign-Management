# Phishing Campaign Management System

This project is a full-stack solution for managing phishing campaigns. It includes both a backend (written in Python) and a frontend (using React). The backend manages email sending, MongoDB database connections, and tracks results, while the frontend provides a user-friendly interface for managing the campaign.

## Project Structure

### Backend (Python)
The backend manages the core logic of sending phishing emails and tracking results. Key files:
- **`configIp.py`** – Configures the server IP for sending requests.
- **`dbConnect.py`** – Manages the MongoDB database connection for storing campaign data.
- **`sendEmail.py`** – Handles the process of sending phishing and warnings emails.
- **`server.py`** – Flask-based server that runs the backend API.

### Frontend (React)
The frontend is a React-based web interface for interacting with the backend. Key files:
- **`src/App.js`** – Main application logic.
- **`src/pages/`** – Different pages for interacting with the app:
  - **HomePage.js** – The main landing page where the campaign's admin can select recipients for the phishing campaign, manage employees, messages, and send phising & warning emails.  
  - **AddEmployeePage.js** – Page for adding employee details.
  - **MessageDesignPage.js** – Page for designing phishing messages.
  - **WhoFellPage.js** – Displays a list of users who fell victim to the phishing campaign.
  - **ipGetter.js** – Retrieves the current server IP.
  - **AddMessagePage.js** – Page for creating phishing messages. When adding a message, you can dynamically insert the recipient's name and phishing URL. For example:
    `Hi {name}, we are offering an upgrade for your account. Click <a href='{phishing_url}{email}'>HERE</a> for more information.`

## Setup Instructions

### 1. Backend Setup

To run the backend, you'll need Python installed along with the necessary dependencies.

#### Install Dependencies
```bash
pip install flask flask_cors requests smtplib pymongo 
```

#### Run the Backend Server
```bash
python server.py
```

Before running the server, make sure you configure the following:
- **Email Details**: You need to add the sender email details in the `fromEmailDetails.txt` file located in the root directory. Make sure to include the following:
  ```txt
  from_email: your_email@example.com
  password: your_password
  smtp_server: smtp.example.com
  smtp_port: 587
  ```

- **IP Configuration**: If necessary, update the IP settings in `configIp.py`.

- **MongoDB Configuration**: The project uses MongoDB as its default database. Ensure that you have a MongoDB instance running on your local machine. The MongoDB connection settings are located in `dbConnect.py`. The connection uses the following format:
```from pymongo import MongoClient

    client = MongoClient('mongodb://localhost:27017')
    db = client['companyDB']
 ```
You will need to make sure MongoDB is running on port `27017`, or adjust the connection string to reflect your MongoDB configuration.

### 2. Frontend Setup

The frontend is built using React, so you'll need Node.js installed to run it.

#### Install Dependencies
Navigate to the `front` directory and install the required Node.js packages:
```bash
cd front
npm install
```

#### Run the Frontend
```bash
npm start
```

This will start the frontend on `http://localhost:3000` by default.

### 3. Project Workflow

1. **Add Employees**: Use the frontend to add the target employees to the phishing campaign. The application starts with one fictional employee. already loaded.
  
2. **Add Messages**: Design phishing messages through the interface. The database is preloaded with 5 phishing messages ready to be sent.

3. **Send Emails**: Trigger the email sending through the backend.

4. **Track Results**: View the employees who clicked the phishing link on the "Who Fell" page. This page displays a list of employee names alongside a column showing how many times each employee clicked on phishing links. There is also an option to send a warning email to each employee individually. When a warning email is sent, their click count is reset.

   Currently, the code is set to redirect employees to YouTube upon clicking the phishing link. This behavior can be modified in the server code within the `server.py` file, specifically in the `handle_phishing_click()` function at the following line:
   ```python
   # Redirect to YouTube
   return redirect("https://www.youtube.com")
   ```


## Notes
- The system is currently a demo version that only works if all devices are connected to the same network.
- Ensure that the backend and frontend are running simultaneously for full functionality.

Enjoy!

## Authors
- Amnon Abaev
- Bar Shuv
