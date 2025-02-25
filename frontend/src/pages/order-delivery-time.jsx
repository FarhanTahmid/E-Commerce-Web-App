import React from 'react'
import PageHeader from '@/components/shared/pageHeader/PageHeader'
import Footer from '@/components/shared/Footer'
import OrderDeliveryTimeHeader from '@/components/orders/deliveryTime/OrderDeliveryTimeHeader'
import OrderDeliveryTimeTable from '@/components/orders/deliveryTime/OrderDeliveryTimeTable'


const OrderDeliveryTime = () => {
    return (
        <>
            <PageHeader>
                <OrderDeliveryTimeHeader />
            </PageHeader>
            <div className='main-content'>
                <div className='row'>
                    <OrderDeliveryTimeTable />
                </div>
            </div>
            <Footer />
        </>
    )
}

export default OrderDeliveryTime