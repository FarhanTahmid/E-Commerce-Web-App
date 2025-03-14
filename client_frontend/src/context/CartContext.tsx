'use client'

import React, { createContext, useContext, useState, useReducer, useEffect } from 'react';
import { ProductType } from '@/type/ProductType';

interface CartItem extends ProductType {
    skuId: string; // Unique identifier for each SKU
    quantityPurchase: number; // Quantity of the item in the cart
    selectedSize: string; // Selected size
    selectedColor: string; // Selected color
}

interface CartState {
    cartArray: CartItem[]; // Array of items in the cart
}

type CartAction =
    | { type: 'ADD_TO_CART'; payload: CartItem } // Add a new item to the cart
    | { type: 'REMOVE_FROM_CART'; payload: string } // Remove an item by SKU ID
    | {
        type: 'UPDATE_CART'; payload: {
            skuId: string; // SKU ID of the item to update
            quantityPurchase: number; // New quantity
            selectedSize: string; // New size
            selectedColor: string; // New color
        }
    }
    | { type: 'LOAD_CART'; payload: CartItem[] }; // Load the cart from storage

interface CartContextProps {
    cartState: CartState; // Current state of the cart
    addToCart: (item: CartItem) => void; // Function to add an item to the cart
    removeFromCart: (skuId: string) => void; // Function to remove an item by SKU ID
    updateCart: (skuId: string, quantityPurchase: number, selectedSize: string, selectedColor: string) => void; // Function to update an item in the cart
}

const CartContext = createContext<CartContextProps | undefined>(undefined);

const cartReducer = (state: CartState, action: CartAction): CartState => {
    switch (action.type) {
        case 'ADD_TO_CART':
            // Check if the item already exists in the cart
            const existingItem = state.cartArray.find((item) => item.skuId === action.payload.skuId);
            if (existingItem) {
                // If it exists, update the quantity
                return {
                    ...state,
                    cartArray: state.cartArray.map((item) =>
                        item.skuId === action.payload.skuId
                            ? { ...item, quantityPurchase: item.quantityPurchase + action.payload.quantityPurchase }
                            : item
                    ),
                };
            } else {
                // If it doesn't exist, add it to the cart
                return {
                    ...state,
                    cartArray: [...state.cartArray, action.payload],
                };
            }
        case 'REMOVE_FROM_CART':
            // Remove the item by SKU ID
            return {
                ...state,
                cartArray: state.cartArray.filter((item) => item.skuId !== action.payload),
            };
        case 'UPDATE_CART':
            // Update the item by SKU ID
            return {
                ...state,
                cartArray: state.cartArray.map((item) =>
                    item.skuId === action.payload.skuId
                        ? {
                            ...item,
                            quantityPurchase: action.payload.quantityPurchase,
                            selectedSize: action.payload.selectedSize,
                            selectedColor: action.payload.selectedColor,
                        }
                        : item
                ),
            };
        case 'LOAD_CART':
            // Load the cart from storage
            return {
                ...state,
                cartArray: action.payload,
            };
        default:
            return state;
    }
};

export const CartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [cartState, dispatch] = useReducer(cartReducer, { cartArray: [] });

    // Add an item to the cart
    const addToCart = (item: CartItem) => {
        dispatch({ type: 'ADD_TO_CART', payload: item });
    };

    // Remove an item from the cart by SKU ID
    const removeFromCart = (skuId: string) => {
        dispatch({ type: 'REMOVE_FROM_CART', payload: skuId });
    };

    // Update an item in the cart by SKU ID
    const updateCart = (skuId: string, quantityPurchase: number, selectedSize: string, selectedColor: string) => {
        dispatch({
            type: 'UPDATE_CART',
            payload: { skuId, quantityPurchase, selectedSize, selectedColor },
        });
    };

    return (
        <CartContext.Provider value={{ cartState, addToCart, removeFromCart, updateCart }}>
            {children}
        </CartContext.Provider>
    );
};

export const useCart = () => {
    const context = useContext(CartContext);
    if (!context) {
        throw new Error('useCart must be used within a CartProvider');
    }
    return context;
};