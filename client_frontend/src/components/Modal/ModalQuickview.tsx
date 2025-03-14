'use client'

import React, { useState, useEffect } from 'react';
import Image from 'next/image';
import { ProductType } from '@/type/ProductType';
import * as Icon from "@phosphor-icons/react/dist/ssr";
import { useModalQuickviewContext } from '@/context/ModalQuickviewContext';
import { useCart } from '@/context/CartContext';
import { useModalCartContext } from '@/context/ModalCartContext';
import { useWishlist } from '@/context/WishlistContext';
import { useModalWishlistContext } from '@/context/ModalWishlistContext';
import { useCompare } from '@/context/CompareContext';
import { useModalCompareContext } from '@/context/ModalCompareContext';
import Rate from '../Other/Rate';
import ModalSizeguide from './ModalSizeguide';

const ModalQuickview = () => {
    const [photoIndex, setPhotoIndex] = useState(0);
    const [openPopupImg, setOpenPopupImg] = useState(false);
    const [openSizeGuide, setOpenSizeGuide] = useState<boolean>(false);
    const { selectedProduct, closeQuickview } = useModalQuickviewContext();
    const [activeColor, setActiveColor] = useState<string>('');
    const [activeSize, setActiveSize] = useState<string>('');
    const [currentPrice, setCurrentPrice] = useState<number>(selectedProduct?.lowestPrice || 0);
    const [currentOriginalPrice, setCurrentOriginalPrice] = useState<number>(selectedProduct?.highestPrice || 0);
    const [currentStock, setCurrentStock] = useState<number>(selectedProduct?.totalQuantity || 0);
    const [currentSKU, setCurrentSKU] = useState<string>(selectedProduct?.skus[0] || '');
    const [currentGender, setCurrentGender] = useState<string>(selectedProduct?.genders[0]?.gender || '');
    const [availableSizes, setAvailableSizes] = useState<string[]>([]);
    const [quantity, setQuantity] = useState<number>(1);
    const { addToCart, updateCart, cartState } = useCart();
    const { openModalCart } = useModalCartContext();
    const { addToWishlist, removeFromWishlist, wishlistState } = useWishlist();
    const { openModalWishlist } = useModalWishlistContext();
    const { addToCompare, removeFromCompare, compareState } = useCompare();
    const { openModalCompare } = useModalCompareContext();

    // Update available sizes and reset quantity when color changes
    useEffect(() => {
        if (selectedProduct && activeColor) {
            const selectedPrice = selectedProduct.prices.find((price) => price.color === activeColor);
            if (selectedPrice) {
                setCurrentPrice(selectedPrice.price);
                setCurrentOriginalPrice(selectedPrice.originalPrice);
                setCurrentStock(selectedPrice.stock);
                setCurrentSKU(selectedPrice.sku);
                const selectedGender = selectedProduct.genders.find((gender) => gender.sku === selectedPrice.sku);
                if (selectedGender) {
                    setCurrentGender(selectedGender.gender);
                }

                // Filter sizes for the selected color
                const sizesForColor = selectedProduct.prices
                    .filter((price) => price.color === activeColor)
                    .map((price) => price.size);
                setAvailableSizes(Array.from(new Set(sizesForColor))); // Remove duplicates
            }
            setQuantity(1); // Reset quantity to 1 when color changes
        }
    }, [activeColor, selectedProduct]);

    // Update stock and reset quantity when size changes
    useEffect(() => {
        if (selectedProduct && activeColor && activeSize) {
            const selectedPrice = selectedProduct.prices.find(
                (price) => price.color === activeColor && price.size === activeSize
            );
            if (selectedPrice) {
                setCurrentStock(selectedPrice.stock);
                setQuantity(1); // Reset quantity to 1 when size changes
            }
        }
    }, [activeSize, activeColor, selectedProduct]);

    const handleActiveColor = (color: string) => {
        setActiveColor(color);
        setActiveSize(''); // Reset size when color changes
    };

    const handleActiveSize = (size: string) => {
        setActiveSize(size);
    };

    const handleIncreaseQuantity = () => {
        if (quantity < currentStock) {
            setQuantity(quantity + 1);
        }
    };

    const handleDecreaseQuantity = () => {
        if (quantity > 1) {
            setQuantity(quantity - 1);
        }
    };

    const handleAddToCart = () => {
        if (!activeColor) {
            alert('Please select a color before adding to cart.');
            return;
        }
        if (!activeSize) {
            alert('Please select a size before adding to cart.');
            return;
        }

        if (selectedProduct) {
            const selectedPrice = selectedProduct.prices.find(
                (price) => price.color === activeColor && price.size === activeSize
            );
            if (selectedPrice) {
                const productToAdd = {
                    ...selectedProduct,
                    skuId: selectedPrice.id, // Pass the SKU ID
                    selectedColor: activeColor,
                    selectedSize: activeSize,
                    price: selectedPrice.price,
                    originalPrice: selectedPrice.originalPrice,
                    quantityPurchase: quantity,
                };

                if (!cartState.cartArray.find(item => item.skuId === selectedPrice.id)) {
                    addToCart(productToAdd);
                } else {
                    updateCart(selectedPrice.id, quantity, activeSize, activeColor);
                }
                openModalCart();
                closeQuickview();
            }
        }
    };


    return (
        <>
            <div className={`modal-quickview-block`} onClick={closeQuickview}>
                <div
                    className={`modal-quickview-main py-6 ${selectedProduct !== null ? 'open' : ''}`}
                    onClick={(e) => { e.stopPropagation() }}
                >
                    <div className="flex h-full max-md:flex-col-reverse gap-y-6">
                        <div className="left lg:w-[388px] md:w-[300px] flex-shrink-0 px-6">
                            <div className="list-img max-md:flex items-center gap-4">
                                {selectedProduct?.images.map((item, index) => (
                                    <div className="bg-img w-full aspect-[3/4] max-md:w-[150px] max-md:flex-shrink-0 rounded-[20px] overflow-hidden md:mt-6" key={index}>
                                        <Image
                                            src={item}
                                            width={1500}
                                            height={2000}
                                            alt={item}
                                            priority={true}
                                            className='w-full h-full object-cover'
                                        />
                                    </div>
                                ))}
                            </div>
                        </div>
                        <div className="right w-full px-4">
                            <div className="heading pb-6 px-4 flex items-center justify-between relative">
                                <div className="heading5">Quick View</div>
                                <div
                                    className="close-btn absolute right-0 top-0 w-6 h-6 rounded-full bg-surface flex items-center justify-center duration-300 cursor-pointer hover:bg-black hover:text-white"
                                    onClick={closeQuickview}
                                >
                                    <Icon.X size={14} />
                                </div>
                            </div>
                            <div className="product-infor px-4">
                                <div className="flex justify-between">
                                    <div>
                                        <div className="heading4 mt-1">{selectedProduct?.name}</div>
                                    </div>
                                </div>
                                <div className="flex items-center gap-3 flex-wrap mt-5 pb-6 border-b border-line">
                                    <div className="product-price heading5">${currentPrice}.00</div>
                                    <div className='w-px h-4 bg-line'></div>
                                    <div className="product-origin-price font-normal text-secondary2"><del>${currentOriginalPrice}.00</del></div>
                                    {selectedProduct?.sale && (
                                        <div className="product-sale caption2 font-semibold bg-green px-3 py-0.5 inline-block rounded-full">
                                            -{Math.floor(100 - ((currentPrice / currentOriginalPrice) * 100))}%
                                        </div>
                                    )}
                                    <br />
                                    <div className='desc text-secondary mt-3'>{selectedProduct?.description}</div>
                                </div>
                                <div className="list-action mt-6">
                                    <div className="choose-color">
                                        <div className="text-title">Colors: <span className='text-title color'>{activeColor}</span></div>
                                        <div className="list-color flex items-center gap-2 flex-wrap mt-3">
                                            {selectedProduct?.prices.map((item, index) => (
                                                <div
                                                    className={`color-item w-12 h-12 rounded-xl duration-300 relative ${activeColor === item.color ? 'active' : ''} overflow-hidden`}
                                                    key={index}
                                                    onClick={() => {
                                                        handleActiveColor(item.color);
                                                    }}
                                                >
                                                    <div
                                                        style={{ backgroundColor: item.colorCode, width: 100, height: 100 }}
                                                        className="rounded-xl"
                                                    ></div>

                                                    <div className="tag-action bg-black text-white caption2 capitalize px-1.5 py-0.5 rounded-sm">
                                                        {item.color}
                                                    </div>

                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                    <div className="choose-size mt-5">
                                        <div className="heading flex items-center justify-between">
                                            <div className="text-title">Size: <span className='text-title size'>{activeSize}</span></div>
                                        </div>
                                        <div className="list-size flex items-center gap-2 flex-wrap mt-3">
                                            {availableSizes.map((item, index) => (
                                                <div
                                                    className={`size-item ${item === 'freesize' ? 'px-3 py-2' : 'w-12 h-12'} flex items-center justify-center text-button rounded-full bg-white border border-line ${activeSize === item ? 'active' : ''}`}
                                                    key={index}
                                                    onClick={() => handleActiveSize(item)}
                                                >
                                                    {item}
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                    <div className="heading flex items-center justify-between mt-5">
                                        <div className="text-title">Product is For: <span className='text-title size'>{currentGender}</span></div>
                                    </div>
                                    <div className="heading flex items-center justify-between mt-5">
                                        <div className="text-title">Stock: <span className='text-title size'>{currentStock}</span></div>
                                    </div>
                                    <div className="text-title mt-5">Quantity:</div>
                                    <div className="choose-quantity flex items-center max-xl:flex-wrap lg:justify-between gap-5 mt-3">
                                        <div className="quantity-block md:p-3 max-md:py-1.5 max-md:px-3 flex items-center justify-between rounded-lg border border-line sm:w-[180px] w-[120px] flex-shrink-0">
                                            <Icon.Minus
                                                onClick={handleDecreaseQuantity}
                                                className={`${quantity <= 1 ? 'opacity-50' : ''} cursor-pointer body1`}
                                            />
                                            <div className="body1 font-semibold">{quantity}</div>
                                            <Icon.Plus
                                                onClick={handleIncreaseQuantity}
                                                className={`${quantity >= currentStock ? 'opacity-50' : ''} cursor-pointer body1`}
                                            />
                                        </div>
                                        <div
                                            onClick={handleAddToCart}
                                            className={`button-main w-full text-center bg-white text-black border border-black ${!activeColor || !activeSize ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
                                        >
                                            {!activeColor || !activeSize ? 'Select Color & Size' : 'Add To Cart'}
                                        </div>
                                    </div>
                                    <div className="more-infor mt-6">
                                        <div className="flex items-center gap-1 mt-3">
                                            <div className="text-title">SKU:</div>
                                            <div className="text-secondary">{currentSKU}</div>
                                        </div>
                                        <div className="flex items-center gap-1 mt-3">
                                            <div className="text-title">Categories:</div>
                                            <div className="text-secondary">{selectedProduct?.categories.join(', ')}</div>
                                        </div>
                                        <div className="flex items-center gap-1 mt-3">
                                            <div className="text-title">Tag:</div>
                                            <div className="text-secondary">{selectedProduct?.types.join(', ')}</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </>
    );
};

export default ModalQuickview;