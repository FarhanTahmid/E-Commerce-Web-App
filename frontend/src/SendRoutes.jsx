import { useEffect } from "react";
import allRoutes from "./extractRoutes"; // Import extracted routes

const SendRoutes = () => {
    useEffect(() => {
        const sendRoutesToBackend = async () => {
            try {
                await fetch("http://127.0.0.1:8000/api/save-routes/", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ routes: allRoutes }),
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
