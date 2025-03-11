// import React from 'react'
// import TopNavOne from '@/components/Header/TopNav/TopNavOne'
// import MenuOne from '@/components/Header/Menu/MenuOne'
// import SliderOne from '@/components/Slider/SliderOne'
// import WhatNewOne from '@/components/Home1/WhatNewOne'
// import productData from '@/data/Product.json'
// import Collection from '@/components/Home1/Collection'
// import TabFeatures from '@/components/Home1/TabFeatures'
// import Banner from '@/components/Home1/Banner'
// import Benefit from '@/components/Home1/Benefit'
// import testimonialData from '@/data/Testimonial.json'
// import Testimonial from '@/components/Home1/Testimonial'
// import Instagram from '@/components/Home1/Instagram'
// import Brand from '@/components/Home1/Brand'
// import Footer from '@/components/Footer/Footer'
// import ModalNewsletter from '@/components/Modal/ModalNewsletter'

// export default function Home() {
//   return (
//     <>
//       {/* <TopNavOne props="style-one bg-black" slogan="New customers save 10% with the code GET10" /> */}
//       <div id="header" className='relative w-full'>
//         <MenuOne props="bg-transparent" />
//         <SliderOne />
//       </div>
//       <WhatNewOne data={productData} start={0} limit={4} />
//       <Collection />
//       <TabFeatures data={productData} start={0} limit={6} />
//       <Banner />
//       <Benefit props="md:py-20 py-10" />
//       <Testimonial data={testimonialData} limit={6} />
//       <Instagram />
//       <Brand />
//       <Footer />
//       {/* <ModalNewsletter /> */}
//     </>
//   )
// }
import React from 'react'
import TopNavOne from '@/components/Header/TopNav/TopNavOne'
import MenuCosmeticThree from '@/components/Header/Menu/MenuCosmeticThree'
import SliderCosmeticThree from '@/components/Slider/SliderCosmeticThree'
import BannerTop from '@/components/Cosmetic3/BannerTop'
import Banner from '@/components/Toys/Banner'
import productData from '@/data/Product.json'
import HotProduct from '@/components/Cosmetic3/HotProduct'
import FeaturedProduct from '@/components/Cosmetic3/FeaturedProduct'
import BuyPack from '@/components/Cosmetic1/BuyPack'
import AdsPhoto from '@/components/Cosmetic1/AdsPhoto.jsx'
import BestSellers from '@/components/Cosmetic3/BestSellers'
import Benefit from '@/components/Cosmetic3/Benefit'
import VideoTutorial from '@/components/Cosmetic3/VideoTutorial'
import Newsletter from '@/components/Cosmetic3/Newsletter'
import Footer from '@/components/Footer/Footer'
import ModalNewsletter from '@/components/Modal/ModalNewsletter'
import MenuOne from '@/components/Header/Menu/MenuOne'

export default function HomeCosmeticThree() {
  return (
    <>
      {/* <TopNavOne props="style-one bg-black" slogan='New customers save 10% with the code GET10' /> */}
      <div id="header" className='relative w-full'>
        <MenuOne props="bg-white" />
        <SliderCosmeticThree />
        {/* <BannerTop props="bg-[#F4C6A5] md:py-8 py-4" textColor='text-black' bgLine='bg-black' /> */}
      </div>

      {/* <Banner /> */}
      <HotProduct data={productData} start={3} limit={9} />
      {/* <BuyPack />
            <AdsPhoto />
            <FeaturedProduct data={productData} />
            <BestSellers data={productData} start={9} limit={20} /> */}
      <Banner />
      <Benefit props="md:py-20 py-10" />
      {/* <VideoTutorial /> */}
      {/* <Newsletter props="bg-transparent" /> */}
      <Footer />
      {/* <ModalNewsletter /> */}
    </>
  )
}
