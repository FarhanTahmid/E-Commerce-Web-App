import React from 'react'
import PageHeader from '@/components/shared/pageHeader/PageHeader'
import Footer from '@/components/shared/Footer'
import ProductBrandTable from '@/components/products/brand/ProductBrandTable'
import ProductBrandHeader from '@/components/products/brand/ProductBrandHeader'

const ProductBrand = () => {
    return (
        <>
            <PageHeader>
                <ProductBrandHeader />
            </PageHeader>
            <div className='main-content'>
                <div className='row'>
                    <ProductBrandTable />
                </div>
            </div>
            <Footer />
        </>
    )
}

export default ProductBrand