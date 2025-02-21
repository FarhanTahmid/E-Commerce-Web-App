import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Cookies from "js-cookie";

let userPermissionsCache = null;

const RequirePermission = ({ children, pageName }) => {
    const [hasPermission, setHasPermission] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchPermissions = async () => {
            const username = Cookies.get("username");
            if (!username) {
                navigate("/403");
                return;
            }

            if (userPermissionsCache !== null) {
                setHasPermission(userPermissionsCache.includes(pageName));
                if (!userPermissionsCache.includes(pageName)) navigate("/403");
                return;
            }

            try {
                const response = await fetch("http://127.0.0.1:8000/api/get-user-permissions/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ username }),
                });

                const data = await response.json();
                userPermissionsCache = data.permissions || [];

                setHasPermission(userPermissionsCache.includes(pageName));
                if (!userPermissionsCache.includes(pageName)) navigate("/403");
            } catch (error) {
                console.error("Error fetching permissions:", error);
                navigate("/403");
            }
        };

        fetchPermissions();
    }, [pageName, navigate]);

    if (hasPermission === null) return <div>Loading...</div>;

    return hasPermission ? children : null;
};

export default RequirePermission;
