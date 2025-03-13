"use client";
import { useState, useEffect } from "react";
import axios from "axios";

// Define the proper ProductType to match what HotProduct expects
interface ProductType {
    id: string;
    category: string;
    type: string;
    name: string;
    gender: string;
    new: boolean;
    sale: boolean;
    rate: number;
    price: number;
    originPrice: number; // Must be a number, not null
    brand: string;
    sold: number;
    quantity: number;
    quantityPurchase: number;
    sizes: string[];
    variation: {
        color: string;
        colorCode: string;
        colorImage: string;
        image: string;
    }[];
    thumbImage: string[];
    images: string[];
    description: string;
    action: string;
    slug: string;
    sku: string;
}

const useProducts = () => {
    const [products, setProducts] = useState<any[]>([]);
    const [transformedProducts, setTransformedProducts] = useState<ProductType[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const API_BASE_URL = `http://127.0.0.1:8000/`;

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                console.log("Fetching products...");
                const response = await axios.get(`${API_BASE_URL}client_api/fetch/fetch_all_product/`);
                console.log("Full API Response:", response.data);

                // Ensure the response is structured as expected
                if (!Array.isArray(response.data)) {
                    console.error("Unexpected response structure:", response.data);
                    setError("Invalid API response structure");
                    return;
                }

                setProducts(response.data);

                const transformed = response.data
                    .map((item: any, index: number) => {
                        try {
                            console.log(`Processing item ${index}:`, item);

                            if (!item.product) {
                                console.warn(`Skipping item ${index} due to missing product field:`, item);
                                return null; // Skipping invalid items
                            }

                            const product = item.product;
                            const discountAmount = Array.isArray(item.product_discount) && item.product_discount.length > 0
                                ? parseFloat(item.product_discount[0]?.discount_amount || "0")
                                : 0;

                            const price = parseFloat(item.product_price) || 0;
                            const originPrice = discountAmount > 0 ? price + (price * (discountAmount / 100)) : price;
                            const defaultImage = "/images/product/1000x1000.png";

                            return {
                                id: item.id?.toString() || "0",
                                category: product?.product_category?.[0]?.category_name?.toLowerCase() || "cosmetic",
                                type: product.product_sub_category?.[0]?.sub_category_name?.toLowerCase() || "face",
                                name: product.product_name || "Unnamed Product",
                                gender: "women",
                                new: new Date(item.created_at || Date.now()) > new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
                                sale: discountAmount > 0,
                                rate: 5,
                                price: price,
                                originPrice: originPrice,
                                brand: product.product_brand?.brand_name || "",
                                sold: 0,
                                quantity: item.product_stock || 0,
                                quantityPurchase: 1,
                                sizes: item.product_size ? [item.product_size] : ["Default"],
                                variation: [{
                                    color: item.product_color ? item.product_color.replace('#', '') : "default",
                                    colorCode: item.product_color || "#000000",
                                    colorImage: item.product_images?.[0] || defaultImage,
                                    image: item.product_images?.[0] || defaultImage
                                }],
                                thumbImage: item.product_images?.length > 0 ? item.product_images : [defaultImage],
                                images: item.product_images?.length > 0 ? item.product_images : [defaultImage, defaultImage],
                                description: product.product_description?.replace(/<\/?[^>]+(>|$)/g, "") ||
                                    product.product_summary ||
                                    "No description available",
                                action: "add to cart",
                                slug: product?.product_category?.[0]?.category_name?.toLowerCase() || "cosmetic",
                                sku: item.product_sku
                            };
                        } catch (itemError) {
                            console.error("Error processing item:", item, itemError);
                            return null; // Prevent transformation failure
                        }
                    })
                    .filter((product): product is ProductType => product !== null); // ✅ Removes null values

                console.log("Transformed Products:", transformed);
                setTransformedProducts(transformed)
            } catch (err) {
                console.error("Error fetching products:", err);
                setError((err as Error).message);
            } finally {
                setLoading(false);
            }
        };

        fetchProducts();
    }, []);



    return { products: transformedProducts, rawProducts: products, loading, error };
};

export default useProducts;