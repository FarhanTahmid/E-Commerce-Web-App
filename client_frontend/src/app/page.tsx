"use client"
import React from 'react'
import SliderCosmeticThree from '@/components/Slider/SliderCosmeticThree'
import Banner from '@/components/Toys/Banner'
import HotProduct from '@/components/Cosmetic3/HotProduct'
import Benefit from '@/components/Cosmetic3/Benefit'
import Footer from '@/components/Footer/Footer'
import MenuOne from '@/components/Header/Menu/MenuOne'
import useProducts from '@/hooks/useProducts'

export default function HomeCosmeticThree() {
  const { products, loading, error } = useProducts();
  console.log(products);
  return (
    <>
      <div id="header" className='relative w-full'>
        <MenuOne props="bg-white" />
        <SliderCosmeticThree />
      </div>

      {loading ? (
        <div className="flex justify-center items-center py-20">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-gray-900"></div>
        </div>
      ) : error ? (
        <div className="text-center py-20 text-red-500">
          Error loading products: {error}
        </div>
      ) : (
        <HotProduct data={products} start={0} limit={9} />
      )}

      <Banner />
      <Benefit props="md:py-20 py-10" />

      <Footer />
    </>
  )
}