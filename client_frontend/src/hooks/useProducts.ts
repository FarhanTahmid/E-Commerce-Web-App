"use client";
import { useState, useEffect } from "react";
import axios from "axios";

// Original ProductType for raw API data
interface ProductType {
    id: number;
    product_name: string;
    product_description: string;
    product_summary: string;
    product_usage_direction: string | null;
    product_ingredients: string | null;

    // Brand information
    product_brand: {
        id: number;
        brand_name: string;
        brand_logo: string;
        brand_description: string;
        brand_country: string;
        brand_established_year: number;
        is_own_brand: boolean;
        created_at: string;
        updated_at: string;
        updated_by: any[];
    };

    // Categories - array of category objects
    product_category: {
        id: number;
        category_name: string;
        description: string;
        created_at: string;
        updated_at: string;
        updated_by: any[];
    }[];

    // Sub-categories - array of subcategory objects
    product_sub_category: {
        id: number;
        sub_category_name: string;
        description: string;
        category_id: number[];
        created_at: string;
        updated_at: string;
        updated_by: any[];
    }[];

    // Product SKUs - variations with different prices, colors, sizes, etc.
    product_skus: {
        id: number;
        product_sku: string;
        product_color: string;
        product_size: string;
        product_price: string;
        product_stock: number;
        product_gender: string;
        product_id: number;
        product_flavours: number[];
        created_at: string;
        updated_at: string;
        updated_by: any[];
    }[];

    // Product images
    product_images: string[];

    // Product flavours - object with keys as IDs mapping to arrays of flavour objects
    product_flavours: {
        [key: string]: {
            id: number;
            product_flavour_name: string;
            created_at: string;
            updated_at: string;
            updated_by: any[];
        }[];
    };

    // Product discount information
    product_discount: {
        id: number;
        discount_name: string;
        discount_amount: string;
        start_date: string;
        end_date: string;
        is_active: boolean;
        product_id: number[];
        product_id_pk: number;
        brand_id: number | null;
        brand_id_pk: number;
        category_id: number | null;
        category_id_pk: number;
        sub_category_id: number | null;
        sub_category_id_pk: number;
        created_at: string;
        updated_at: string;
        updated_by: any[];
    };

    created_at: string;
    updated_at: string;
    updated_by: any[];
}

// New interface for transformed products
interface TransformedProductType {
    id: number;
    categories: string[];
    types: string[];
    name: string;
    genders: { sku: string; gender: string }[];
    new: boolean;
    sale: boolean;
    rate: number;
    prices: {
        id: number;  // Added the SKU ID here
        sku: string;
        price: number;
        originalPrice: number;
        stock: number;
        size: string;
        color: string;
        colorCode: string;
        flavours?: { id: number; name: string }[];
    }[];
    lowestPrice: number;
    highestPrice: number;
    brand: string;
    sold: number;
    totalQuantity: number;
    quantityPurchase: number;
    sizes: string[];
    variation: {
        id: number;  // Added the SKU ID here
        color: string;
        colorCode: string;
        colorImage: string;
        image: string;
        sku: string;
        flavour?: string;
        flavourId?: number;
    }[];
    thumbImage: string[];
    images: string[];
    description: string;
    action: string;
    slugs: string[];
    skus: string[];
    discount?: {
        amount: number;
        name: string;
        startDate: string;
        endDate: string;
        isActive: boolean;
    };
}

const useProducts = () => {
    const [products, setProducts] = useState<any[]>([]);
    const [transformedProducts, setTransformedProducts] = useState<TransformedProductType[]>([]);
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
                    .map((product: any): TransformedProductType | null => {
                        try {
                            console.log(`Processing product:`, product);

                            // Extract discount information if available
                            const productDiscount = product.product_discount || null;
                            const discountAmount = productDiscount?.discount_amount
                                ? parseFloat(productDiscount.discount_amount)
                                : 0;
                            const isDiscountActive = productDiscount?.is_active || false;

                            // Process product SKUs
                            const skus = product.product_skus || [];
                            if (skus.length === 0) {
                                console.warn(`Product ${product.id} has no SKUs`, product);
                                return null;
                            }

                            // Extract all SKU codes
                            const skuCodes = skus.map((sku: any) => sku.product_sku || "");

                            // Extract all genders from SKUs
                            const genders = skus.map((sku: any) => ({
                                sku: sku.product_sku,
                                gender: typeof sku.product_gender === "string" ? sku.product_gender : "Unisex"
                            }));

                            // Extract all sizes from SKUs
                            const sizes = Array.from(new Set(skus.map((sku: any) =>
                                typeof sku.product_size === "string" ? sku.product_size : "Default"
                            ))) as string[];

                            // Process prices with detailed information for each SKU
                            const prices = skus.map((sku: any) => {
                                const skuPrice = sku.product_price ? parseFloat(sku.product_price) : 0;
                                const originalPrice = isDiscountActive && discountAmount > 0
                                    ? skuPrice + (skuPrice * (discountAmount / 100))
                                    : skuPrice;

                                // Process flavours for this SKU
                                const flavourIds = sku.product_flavours || [];
                                const flavours: { id: number, name: string }[] = [];

                                if (flavourIds.length > 0 && product.product_flavours) {
                                    flavourIds.forEach((flavourId: number) => {
                                        const flavoursForId = product.product_flavours[flavourId] || [];
                                        flavoursForId.forEach((flavour: any) => {
                                            flavours.push({
                                                id: flavour.id,
                                                name: flavour.product_flavour_name
                                            });
                                        });
                                    });
                                }

                                return {
                                    id: sku.id,  // Add SKU ID here
                                    sku: sku.product_sku,
                                    price: skuPrice,
                                    originalPrice: originalPrice,
                                    stock: sku.product_stock || 0,
                                    size: sku.product_size || "Default",
                                    color: sku.product_color || "#000000",
                                    colorCode: sku.product_color || "#000000",
                                    flavours: flavours.length > 0 ? flavours : undefined
                                };
                            });

                            // Calculate lowest and highest prices for display
                            const priceValues: number[] = prices.map((p: { price: number }) => p.price);
                            const lowestPrice = Math.min(...priceValues);
                            const highestPrice = Math.max(...priceValues);

                            // Calculate total stock
                            const totalStock: number = prices.reduce((total: number, p: { stock: number }) => total + p.stock, 0);

                            // Extract all categories as strings
                            const categories = (product.product_category || [])
                                .map((cat: any) => cat.category_name?.toLowerCase() || "");

                            // Extract all subcategories as strings
                            const types = (product.product_sub_category || [])
                                .map((subcat: any) => subcat.sub_category_name?.toLowerCase() || "");

                            // Generate slugs from categories and subcategories
                            const slugs = [...categories, ...types];

                            // Create variations from SKUs and flavors
                            const variations = skus.flatMap((sku: any) => {
                                const flavourIds = sku.product_flavours || [];
                                const allFlavours: any[] = [];

                                // Process flavors related to this SKU
                                if (flavourIds.length > 0 && product.product_flavours) {
                                    flavourIds.forEach((flavourId: number) => {
                                        // Find flavors for this id
                                        const flavoursForId = product.product_flavours[flavourId] || [];
                                        flavoursForId.forEach((flavour: any) => {
                                            allFlavours.push({
                                                id: sku.id,  // Add SKU ID here
                                                colorCode: sku.product_color,
                                                color: sku.product_color?.replace('#', '') || 'default',
                                                flavour: flavour.product_flavour_name,
                                                flavourId: flavour.id,
                                                colorImage: product.product_images?.[0] || "/images/product/1000x1000.png",
                                                image: product.product_images?.[0] || "/images/product/1000x1000.png",
                                                sku: sku.product_sku
                                            });
                                        });
                                    });
                                }

                                // If no flavors, create a variation just from the SKU
                                if (allFlavours.length === 0) {
                                    return [{
                                        id: sku.id,  // Add SKU ID here
                                        color: sku.product_color?.replace('#', '') || 'default',
                                        colorCode: sku.product_color || "#000000",
                                        colorImage: product.product_images?.[0] || "/images/product/1000x1000.png",
                                        image: product.product_images?.[0] || "/images/product/1000x1000.png",
                                        sku: sku.product_sku
                                    }];
                                }

                                return allFlavours;
                            });

                            // Process description - remove HTML tags
                            const plainDescription = product.product_description
                                ? product.product_description.replace(/<\/?[^>]+(>|$)/g, "")
                                : product.product_summary || "No description available";

                            return {
                                id: product.id,
                                categories: categories,
                                types: types,
                                name: product.product_name || "Unnamed Product",
                                genders: genders,
                                new: new Date(product.created_at || Date.now()) >
                                    new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
                                sale: isDiscountActive && discountAmount > 0,
                                rate: 5,
                                prices: prices,
                                lowestPrice: lowestPrice,
                                highestPrice: highestPrice,
                                brand: product.product_brand?.brand_name || "",
                                sold: 0,
                                totalQuantity: totalStock,
                                quantityPurchase: 1,
                                sizes: sizes,
                                variation: variations,
                                thumbImage: product.product_images || ["/images/product/1000x1000.png"],
                                images: product.product_images || ["/images/product/1000x1000.png", "/images/product/1000x1000.png"],
                                description: plainDescription,
                                action: "add to cart",
                                slugs: slugs,
                                skus: skuCodes,
                                discount: productDiscount ? {
                                    amount: discountAmount,
                                    name: productDiscount.discount_name || "",
                                    startDate: productDiscount.start_date || "",
                                    endDate: productDiscount.end_date || "",
                                    isActive: isDiscountActive
                                } : undefined
                            };
                        } catch (itemError) {
                            console.error("Error processing item:", product, itemError);
                            return null; // Prevent transformation failure
                        }
                    })
                    .filter((product): product is TransformedProductType => product !== null); // Remove null values

                console.log("Transformed Products:", transformed);
                setTransformedProducts(transformed);
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