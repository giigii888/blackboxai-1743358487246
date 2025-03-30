import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  // Set auth token for axios
  const setAuthToken = (token) => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      delete axios.defaults.headers.common['Authorization'];
    }
  };

  // Check if user is authenticated
  const checkAuth = async () => {
    try {
      if (token) {
        setAuthToken(token);
        const res = await axios.get('/api/auth/me');
        setUser(res.data);
      }
    } catch (err) {
      logout();
    } finally {
      setIsLoading(false);
    }
  };

  // Login user
  const login = async (username, password) => {
    try {
      const res = await axios.post('/api/auth/login', { username, password });
      const { access_token } = res.data;
      localStorage.setItem('token', access_token);
      setToken(access_token);
      setAuthToken(access_token);
      await checkAuth();
      navigate('/');
    } catch (err) {
      throw err;
    }
  };

  // Logout user
  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    navigate('/login');
  };

  // Check auth on initial load
  useEffect(() => {
    checkAuth();
  }, [token]);

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isLoading,
        login,
        logout,
        setUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;