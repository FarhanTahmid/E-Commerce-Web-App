import { useEffect } from "react";
import allRoutes from "./extractRoutes"; // Import extracted routes
console.log(allRoutes);

const SendRoutes = () => {
    useEffect(() => {
        const sendRoutesToBackend = async () => {
            try {
                await fetch("http://127.0.0.1:8000/server_api/system/register-permissions/", {
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
