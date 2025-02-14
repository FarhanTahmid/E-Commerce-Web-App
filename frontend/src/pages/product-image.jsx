import React from 'react'
import PageHeader from '@/components/shared/pageHeader/PageHeader'
import Footer from '@/components/shared/Footer'
import ProductImageTable from '@/components/products/image/ProductImageTable'

const ProductImage = () => {
    return (
        <>
            <PageHeader>
            </PageHeader>
            <div className='main-content'>
                <div className='row'>
                    <ProductImageTable />
                </div>
            </div>
            <Footer />
        </>
    )
}

export default ProductImage