import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import axios from 'axios';
import './index.css';

// Set base URL for API requests
axios.defaults.baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);