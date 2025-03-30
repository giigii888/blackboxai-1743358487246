import React, { useContext } from 'react';
import { Link, Outlet } from 'react-router-dom';
import AuthContext from '../context/AuthContext';

const Dashboard = () => {
  const { user, logout } = useContext(AuthContext);

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-md">
        <div className="p-4 border-b border-gray-200">
          <h1 className="text-xl font-semibold text-gray-800">Chatbot Admin</h1>
          <p className="text-sm text-gray-500">Welcome, {user?.username}</p>
        </div>
        <nav className="p-4">
          <ul className="space-y-2">
            <li>
              <Link
                to="/bots"
                className="flex items-center p-2 text-gray-700 rounded-lg hover:bg-gray-100"
              >
                <span className="ml-3">Bots</span>
              </Link>
            </li>
            <li>
              <Link
                to="/scripts"
                className="flex items-center p-2 text-gray-700 rounded-lg hover:bg-gray-100"
              >
                <span className="ml-3">Training Scripts</span>
              </Link>
            </li>
            <li>
              <Link
                to="/integrations"
                className="flex items-center p-2 text-gray-700 rounded-lg hover:bg-gray-100"
              >
                <span className="ml-3">Integrations</span>
              </Link>
            </li>
            <li>
              <Link
                to="/logs"
                className="flex items-center p-2 text-gray-700 rounded-lg hover:bg-gray-100"
              >
                <span className="ml-3">Conversation Logs</span>
              </Link>
            </li>
            <li>
              <button
                onClick={logout}
                className="w-full flex items-center p-2 text-gray-700 rounded-lg hover:bg-gray-100"
              >
                <span className="ml-3">Logout</span>
              </button>
            </li>
          </ul>
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        <div className="p-6">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;