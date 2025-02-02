import Cookies from 'js-cookie';
import { Navigate } from 'react-router-dom';

const parseJwt = (token) => {
    try {
        const base64Url = token.split('.')[1]; // Get payload
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/'); // Fix URL-safe characters
        const jsonPayload = decodeURIComponent(atob(base64).split('').map((c) =>
            '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
        ).join(''));

        return JSON.parse(jsonPayload);
    } catch (error) {
        return null; // Invalid token
    }
};

const RequireAuth = ({ children }) => {
    const accessToken = Cookies.get('accessToken');

    if (!accessToken) {
        return <Navigate to="/authentication/login/minimal" replace />;
    }

    const decodedToken = parseJwt(accessToken);

    if (!decodedToken || decodedToken.exp * 1000 < Date.now()) {
        // Token expired, redirect to login
        return <Navigate to="/authentication/login/minimal" replace />;
    }

    return children;
};

export default RequireAuth;
