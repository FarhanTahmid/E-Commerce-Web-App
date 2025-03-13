"use client"
import React, { useEffect, useState } from 'react'
import SliderCosmeticThree from '@/components/Slider/SliderCosmeticThree'
import Banner from '@/components/Toys/Banner'
import productData from '@/data/Product.json'
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

      <HotProduct data={productData} start={3} limit={9} />

      <Banner />
      <Benefit props="md:py-20 py-10" />

      <Footer />
    </>
  )
}
