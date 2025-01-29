import React from 'react';
import { Navigate } from 'react-router-dom';
import Cookies from 'js-cookie';

const RequireAuth = ({ children }) => {
    const authToken = Cookies.get('authToken');

    if (!authToken) {
        // If no token exists, redirect to login
        return <Navigate to="/authentication/login/minimal" replace />;
    }

    // Render children if token exists
    return children;
};

export default RequireAuth;
