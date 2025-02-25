import React from 'react'
import PageHeader from '@/components/shared/pageHeader/PageHeader'
import Footer from '@/components/shared/Footer'
import ProductTable from '@/components/products/product/ProductTable'
import ProductHeader from '@/components/products/product/ProductHeader'

const Product = () => {
    return (
        <>
            <PageHeader>
                <ProductHeader />
            </PageHeader>
            <div className='main-content'>
                <div className='row'>
                    <ProductTable />
                </div>
            </div>
            <Footer />
        </>
    )
}

export default Product