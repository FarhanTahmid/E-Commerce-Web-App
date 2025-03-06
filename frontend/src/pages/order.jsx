import React from 'react'
import PageHeader from '@/components/shared/pageHeader/PageHeader'
import Footer from '@/components/shared/Footer'
import OrderTable from '@/components/orders/order/OrderTable'


const Order = () => {
    return (
        <>
            <PageHeader>
            </PageHeader>
            <div className='main-content'>
                <div className='row'>
                    <OrderTable />
                </div>
            </div>
            <Footer />
        </>
    )
}

export default Order