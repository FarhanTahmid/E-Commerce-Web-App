"use client"
import { useState, useEffect } from "react";
import axios from "axios";

// Define Product type based on your Django model
interface Product {
    id: number;
    name: string;
    description: string;
    price: number;
    image: string;
    category: string;
    [key: string]: any; // Allow additional properties
}

const useProducts = () => {
    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const API_BASE_URL = `http://127.0.0.1:8000/`;

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const response = await axios.get<Product[]>(`${API_BASE_URL}client_api/fetch/fetch_all_product/`);
                setProducts(response.data);
            } catch (err) {
                setError((err as Error).message);
            } finally {
                setLoading(false);
            }
        };

        fetchProducts();
    }, []);

    return { products, loading, error };
};

export default useProducts;
