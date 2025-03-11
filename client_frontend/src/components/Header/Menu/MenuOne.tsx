'use client'

import React, { useState, useEffect } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import * as Icon from "@phosphor-icons/react/dist/ssr";
import { usePathname } from 'next/navigation';
import Product from '@/components/Product/Product';
import productData from '@/data/Product.json'
import useLoginPopup from '@/store/useLoginPopup';
import useMenuMobile from '@/store/useMenuMobile';
import { useModalCartContext } from '@/context/ModalCartContext';
import { useModalWishlistContext } from '@/context/ModalWishlistContext';
import { useModalSearchContext } from '@/context/ModalSearchContext';
import { useCart } from '@/context/CartContext';
import { useRouter } from 'next/navigation';

interface Props {
    props: string;
}
// API URL configuration
const BackendUrlMainAPI = "http://127.0.0.1:8000/"
const API_BASE_URL = `${BackendUrlMainAPI}client_api`

const MenuOne: React.FC<Props> = ({ props }) => {
    const router = useRouter()
    const pathname = usePathname()
    let [selectedType, setSelectedType] = useState<string | null>()
    const { openLoginPopup, handleLoginPopup } = useLoginPopup()
    const { openMenuMobile, handleMenuMobile } = useMenuMobile()
    const [openSubNavMobile, setOpenSubNavMobile] = useState<number | null>(null)
    const { openModalCart } = useModalCartContext()
    const { cartState } = useCart()
    const { openModalWishlist } = useModalWishlistContext()
    const { openModalSearch } = useModalSearchContext()

    const [categories, setCategories] = useState([])
    const [subCategories, setSubCategories] = useState([])
    const [loading, setLoading] = useState(true)
    const [activeCategory, setActiveCategory] = useState(null)

    // Fetch all categories on component mount
    useEffect(() => {
        const fetchCategories = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/fetch/fetch_categories/`)
                if (response.ok) {
                    const data = await response.json()
                    setCategories(data)

                    // Fetch all subcategories on initial load
                    fetchSubCategories()
                } else {
                    console.error('Failed to fetch categories')
                }
            } catch (error) {
                console.error('Error fetching categories:', error)
            } finally {
                setLoading(false)
            }
        }

        const fetchSubCategories = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/fetch/fetch_sub_categories/`)
                if (response.ok) {
                    const data = await response.json()
                    setSubCategories(data)
                } else {
                    console.error('Failed to fetch subcategories')
                }
            } catch (error) {
                console.error('Error fetching subcategories:', error)
            }
        }

        fetchCategories()
    }, [])


    // Filter subcategories by category ID
    const getSubcategoriesByCategory = (categoryId) => {
        return subCategories.filter(subcat => subcat.id === categoryId)
    }

    // Handle category hover
    const handleCategoryHover = (categoryId) => {
        setActiveCategory(categoryId)
    }

    // Navigate to subcategory page
    const handleSubCategoryClick = (subCategoryName) => {
        router.push(`/shop?sub_category=${subCategoryName}`)
    }

    const handleOpenSubNavMobile = (index: number) => {
        setOpenSubNavMobile(openSubNavMobile === index ? null : index)
    }

    const [fixedHeader, setFixedHeader] = useState(false)
    const [lastScrollPosition, setLastScrollPosition] = useState(0);

    useEffect(() => {
        const handleScroll = () => {
            const scrollPosition = window.scrollY;
            setFixedHeader(scrollPosition > 0 && scrollPosition < lastScrollPosition);
            setLastScrollPosition(scrollPosition);
        };

        // Gắn sự kiện cuộn khi component được mount
        window.addEventListener('scroll', handleScroll);

        // Hủy sự kiện khi component bị unmount
        return () => {
            window.removeEventListener('scroll', handleScroll);
        };
    }, [lastScrollPosition]);

    const handleGenderClick = (gender: string) => {
        router.push(`/shop?gender=${gender}`);
    };

    const handleCategoryClick = (category: string) => {
        router.push(`/shop?category=${category}`);
    };

    const handleTypeClick = (type: string) => {
        setSelectedType(type)
        router.push(`/shop?type=${type}`);
    };

    return (
        <>
            <div className={`header-menu style-one ${fixedHeader ? 'fixed' : 'absolute'} top-0 left-0 right-0 w-full md:h-[74px] h-[56px] ${props}`}>
                <div className="container mx-auto h-full">
                    <div className="header-main flex justify-between h-full">
                        <div className="menu-mobile-icon lg:hidden flex items-center" onClick={handleMenuMobile}>
                            <i className="icon-category text-2xl"></i>
                        </div>
                        <div className="left flex items-center gap-16">
                            <Link href={'/'} className='flex items-center max-lg:absolute max-lg:left-1/2 max-lg:-translate-x-1/2'>
                                <div className="heading4">Knap Cosmetics</div>
                            </Link>
                            <div className="menu-main h-full max-lg:hidden">
                                <ul className='flex items-center gap-8 h-full'>

                                    {categories.map((category) => (
                                        <li className='h-full relative'>
                                            <Link href="#!" className={`text-button-uppercase duration-300 h-full flex items-center justify-center ${pathname.includes('/pages') ? 'active' : ''}`}>
                                                {category.category_name}
                                            </Link>
                                            <div className="sub-menu py-3 px-5 -left-10 absolute bg-white rounded-b-xl">
                                                <ul className='w-full'>
                                                    {getSubcategoriesByCategory(category.id).map((subCategory) => (
                                                        <li key={subCategory.id}>
                                                            <Link
                                                                href="#"
                                                                onClick={(e) => {
                                                                    e.preventDefault()
                                                                    handleSubCategoryClick(subCategory.sub_category_name)
                                                                }}
                                                                className={`link text-secondary duration-300 ${pathname === '/pages/about' ? 'active' : ''}`}
                                                            >
                                                                {subCategory.sub_category_name}
                                                            </Link>
                                                        </li>
                                                    ))}
                                                    <li>
                                                        <Link href="/pages/about" className={`link text-secondary duration-300 ${pathname === '/pages/about' ? 'active' : ''}`}>
                                                            About Us
                                                        </Link>
                                                    </li>
                                                    <li>
                                                        <Link href="/pages/contact" className={`link text-secondary duration-300 ${pathname === '/pages/contact' ? 'active' : ''}`}>
                                                            Contact Us
                                                        </Link>
                                                    </li>
                                                    <li>
                                                        <Link href="/pages/store-list" className={`link text-secondary duration-300 ${pathname === '/pages/store-list' ? 'active' : ''}`}>
                                                            Store List
                                                        </Link>
                                                    </li>
                                                    <li>
                                                        <Link href="/pages/page-not-found" className={`link text-secondary duration-300 ${pathname === '/pages/page-not-found' ? 'active' : ''}`}>
                                                            404
                                                        </Link>
                                                    </li>
                                                    <li>
                                                        <Link href="/pages/faqs" className={`link text-secondary duration-300 ${pathname === '/pages/faqs' ? 'active' : ''}`}>
                                                            FAQs
                                                        </Link>
                                                    </li>
                                                    <li>
                                                        <Link href="/pages/coming-soon" className={`link text-secondary duration-300 ${pathname === '/pages/coming-soon' ? 'active' : ''}`}>
                                                            Coming Soon
                                                        </Link>
                                                    </li>
                                                    <li>
                                                        <Link href="/pages/customer-feedbacks" className={`link text-secondary duration-300 ${pathname === '/pages/customer-feedbacks' ? 'active' : ''}`}>
                                                            Customer Feedbacks
                                                        </Link>
                                                    </li>
                                                </ul>
                                            </div>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                        <div className="right flex gap-12">
                            <div className="max-md:hidden search-icon flex items-center cursor-pointer relative">
                                <Icon.MagnifyingGlass size={24} color='black' onClick={openModalSearch} />
                                <div className="line absolute bg-line w-px h-6 -right-6"></div>
                            </div>
                            <div className="list-action flex items-center gap-4">
                                <div className="user-icon flex items-center justify-center cursor-pointer">
                                    <Icon.User size={24} color='black' onClick={handleLoginPopup} />
                                    <div
                                        className={`login-popup absolute top-[74px] w-[320px] p-7 rounded-xl bg-white box-shadow-sm 
                                            ${openLoginPopup ? 'open' : ''}`}
                                    >
                                        <Link href={'/login'} className="button-main w-full text-center">Login</Link>
                                        <div className="text-secondary text-center mt-3 pb-4">Don’t have an account?
                                            <Link href={'/register'} className='text-black pl-1 hover:underline'>Register</Link>
                                        </div>
                                        <Link href={'/my-account'} className="button-main bg-white text-black border border-black w-full text-center">Dashboard</Link>
                                        <div className="bottom mt-4 pt-4 border-t border-line"></div>
                                        <Link href={'#!'} className='body1 hover:underline'>Support</Link>
                                    </div>
                                </div>
                                <div className="max-md:hidden wishlist-icon flex items-center cursor-pointer" onClick={openModalWishlist}>
                                    <Icon.Heart size={24} color='black' />
                                </div>
                                <div className="cart-icon flex items-center relative cursor-pointer" onClick={openModalCart}>
                                    <Icon.Handbag size={24} color='black' />
                                    <span className="quantity cart-quantity absolute -right-1.5 -top-1.5 text-xs text-white bg-black w-4 h-4 flex items-center justify-center rounded-full">{cartState.cartArray.length}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div id="menu-mobile" className={`${openMenuMobile ? 'open' : ''}`}>
                <div className="menu-container bg-white h-full">
                    <div className="container h-full">
                        <div className="menu-main h-full overflow-hidden">
                            <div className="heading py-2 relative flex items-center justify-center">
                                <div
                                    className="close-menu-mobile-btn absolute left-0 top-1/2 -translate-y-1/2 w-6 h-6 rounded-full bg-surface flex items-center justify-center"
                                    onClick={handleMenuMobile}
                                >
                                    <Icon.X size={14} />
                                </div>
                                <Link href={'/'} className='logo text-3xl font-semibold text-center'>Anvogue</Link>
                            </div>
                            {/* <div className="form-search relative mt-2">
                                <Icon.MagnifyingGlass size={20} className='absolute left-3 top-1/2 -translate-y-1/2 cursor-pointer' />
                                <input type="text" placeholder='What are you looking for?' className=' h-12 rounded-lg border border-line text-sm w-full pl-10 pr-4' />
                            </div> */}
                            <div className="list-nav mt-6">
                                <ul>

                                    {categories.map((category) => (
                                        <li
                                            key={category.id}
                                            className={openSubNavMobile === category.id ? 'open' : ''}
                                            onClick={() => handleOpenSubNavMobile(category.id)}
                                        >
                                            <a href={'#!'} className={`text-xl font-semibold flex items-center justify-between mt-5`}>{category.category_name}
                                                <span className='text-right'>
                                                    <Icon.CaretRight size={20} />
                                                </span>
                                            </a>
                                            <div className="sub-nav-mobile">
                                                <div
                                                    className="back-btn flex items-center gap-3"
                                                    onClick={() => handleOpenSubNavMobile(1)}
                                                >
                                                    <Icon.CaretLeft />
                                                    Back
                                                </div>
                                                <div className="list-nav-item w-full grid grid-cols-2 pt-2 pb-6">
                                                    <ul>
                                                        {getSubcategoriesByCategory(category.id).map((subCategory) => (
                                                            <li key={subCategory.id}>

                                                                <Link href="/" className={`nav-item-mobile link text-secondary duration-300 `}>
                                                                    {subCategory.sub_category_name}
                                                                </Link>

                                                            </li>

                                                        ))}
                                                        {/* <li>
                                                            <Link href="/" className={`nav-item-mobile link text-secondary duration-300 ${pathname === '/' ? 'active' : ''}`}>
                                                                Home Fashion 1
                                                            </Link>
                                                        </li> */}
                                                    </ul>
                                                </div>
                                            </div>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div >
        </>
    )
}

export default MenuOne