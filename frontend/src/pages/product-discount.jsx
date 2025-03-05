import React from 'react'
import PageHeader from '@/components/shared/pageHeader/PageHeader'
import Footer from '@/components/shared/Footer'
import ProductDiscountHeader from '@/components/products/discount/ProductDiscountHeader'
import ProductDiscountTable from '@/components/products/discount/ProductDiscountTable'

const ProductDiscount = () => {
    return (
        <>
            <PageHeader>
                <ProductDiscountHeader />
            </PageHeader>
            <div className='main-content'>
                <div className='row'>
                    <ProductDiscountTable />
                </div>
            </div>
            <Footer />
        </>
    )
}

export default ProductDiscount