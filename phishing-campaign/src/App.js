import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage.js';
import AddMessagePage from './pages/AddMessagePage.js';
import MessageDesignPage from './pages/MessageDesignPage.js';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/add-message" element={<AddMessagePage />} />
        <Route path="/message-design" element={<MessageDesignPage />} />
      </Routes>
    </Router>
  );
}

export default App;
