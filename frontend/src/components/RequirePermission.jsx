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

            try {
                const response = await fetch("http://127.0.0.1:8000/server_api/system/has-permissions/", {
                    method: "POST",
                    headers: {
                        "Authorization": `Bearer ${Cookies.get("accessToken")}`,
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ user_name: username, permission_page_name: pageName }),
                });

                const data = await response.json();
                userPermissionsCache = data.hasPermissions;
                if (!userPermissionsCache) navigate("/403");
                setHasPermission(userPermissionsCache);
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
