// Define nested interface types for better organization
interface Brand {
    id: number;
    brand_name: string;
    brand_logo: string;
    brand_description: string;
    brand_country: string;
    brand_established_year: number;
    is_own_brand: boolean;
}

interface Gender {
    sku: string;
    gender: string;
}

interface Price {
    sku: string;
    price: number;
    originalPrice: number;
    stock: number;
    size: string;
    color: string;
    colorCode: string;
    flavours?: {
        id: number;
        name: string;
    }[];
}

interface Variation {
    color: string;
    colorCode: string;
    colorImage: string;
    image: string;
    flavour?: string;
    flavourId?: number;
    sku?: string;
}

interface Discount {
    amount: number;
    name: string;
    startDate: string;
    endDate: string;
    isActive: boolean;
}

export interface ProductType {
    id: number;
    categories: string[];
    types: string[];
    name: string;
    genders: Gender[];
    new: boolean;
    sale: boolean;
    rate: number;
    prices: Price[];
    lowestPrice: number;
    highestPrice: number;
    brand: string;
    sold: number;
    totalQuantity: number;
    quantityPurchase: number;
    sizes: string[];
    variation: Variation[];
    thumbImage: string[];
    images: string[];
    description: string;
    action: string;
    slugs: string[];
    skus: string[];
    discount?: Discount;
}