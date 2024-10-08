import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage.js';
import AddMessagePage from './pages/AddMessagePage.js';
import MessageDesignPage from './pages/MessageDesignPage.js';
import AddEmployeePage from './pages/AddEmployeePage';
import WhoFellPage from './pages/WhoFellPage.js';

/**
 * Main application component that sets up routing for the application.
 * It uses React Router to define the different routes and their corresponding components.
 */
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/add-message" element={<AddMessagePage />} />
        <Route path="/message-design" element={<MessageDesignPage />} />
        <Route path="/add-employee" element={<AddEmployeePage />} />
        <Route path="/who-fell" element={<WhoFellPage />} />
      </Routes>
    </Router>
  );
}

export default App;
