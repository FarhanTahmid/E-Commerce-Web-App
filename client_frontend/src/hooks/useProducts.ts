"use client";
import { useState, useEffect } from "react";
import axios from "axios";

const useProducts = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const API_BASE_URL = `http://127.0.0.1:8000/`;

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const response = await axios.get(`${API_BASE_URL}client_api/fetch/fetch_all_product/`);
                console.log("response.data", response)
                setProducts(response.data);
            } catch (err) {
                setError((err as Error).message);
            } finally {
                setLoading(false);
            }
        };

        fetchProducts();
    }, []);
    console.log("products", { products })
    return { products, loading, error };
};

export default useProducts;
