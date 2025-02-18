import React from 'react'
import PageHeader from '@/components/shared/pageHeader/PageHeader'
import Footer from '@/components/shared/Footer'
import ProductDeliveryTimeHeader from '@/components/products/deliveryTime/ProductDeliveryTimeHeader'
import ProductDeliveryTimeTable from '@/components/products/deliveryTime/ProductDeliveryTimeTable'


const ProductDeliveryTime = () => {
    return (
        <>
            <PageHeader>
                <ProductDeliveryTimeHeader />
            </PageHeader>
            <div className='main-content'>
                <div className='row'>
                    <ProductDeliveryTimeTable />
                </div>
            </div>
            <Footer />
        </>
    )
}

export default ProductDeliveryTime