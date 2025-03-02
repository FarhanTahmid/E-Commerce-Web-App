import { useEffect } from "react";
import allRoutes from "./extractRoutes"; // Import extracted routes
import { BackendUrlMainAPI } from "./BackendUrlMainAPI";

const SendRoutes = () => {
    useEffect(() => {
        const sendRoutesToBackend = async () => {
            try {
                await fetch(`${BackendUrlMainAPI}server_api/system/register-permissions/`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ permission_names_list: allRoutes }),
                });
            } catch (error) {
                console.error("Error sending routes:", error);
            }
        };

        sendRoutesToBackend();
    }, []);

    return null;
};

export default SendRoutes;
