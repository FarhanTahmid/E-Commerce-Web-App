import React from 'react'
import PageHeader from '@/components/shared/pageHeader/PageHeader'
import Footer from '@/components/shared/Footer'
import ProductFlavourTable from '@/components/products/flavour/ProductFlavourTable'
import ProductFlavourHeader from '@/components/products/flavour/ProductFlavourHeader'

const ProductFlavour = () => {
    return (
        <>
            <PageHeader>
                <ProductFlavourHeader />
            </PageHeader>
            <div className='main-content'>
                <div className='row'>
                    <ProductFlavourTable />
                </div>
            </div>
            <Footer />
        </>
    )
}

export default ProductFlavour