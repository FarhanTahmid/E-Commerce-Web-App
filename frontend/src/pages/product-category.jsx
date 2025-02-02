import React from 'react'
import PageHeader from '@/components/shared/pageHeader/PageHeader'
import ProductCategoryHeader from '@/components/products/ProductCategoryHeader'
import Footer from '@/components/shared/Footer'
import ProductCategoryTable from '@/components/products/ProductCategoryTable'

const ProductCategory = () => {
    return (
        <>
            <PageHeader>
                <ProductCategoryHeader />
            </PageHeader>
            <div className='main-content'>
                <div className='row'>
                    <ProductCategoryTable />
                </div>
            </div>
            <Footer />
        </>
    )
}

export default ProductCategory