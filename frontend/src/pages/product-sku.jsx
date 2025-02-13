import React from 'react'
import PageHeader from '@/components/shared/pageHeader/PageHeader'
import Footer from '@/components/shared/Footer'
// import ProductSKUTable from '@/components/products/sku/ProductSKUTable'
import ProductSKUHeader from '@/components/products/sku/ProductSKUHeader'
import ProductSKUList from '@/components/products/sku/ProductSKUList'

const ProductSKU = () => {
    return (
        <>
            <PageHeader>
                {/* <ProductSKUHeader /> */}
            </PageHeader>
            <div className='main-content'>
                <div className='row'>
                    <ProductSKUList />
                    {/* <ProductSKUTable /> */}
                </div>
            </div>
            <Footer />
        </>
    )
}

export default ProductSKU