import React from 'react'
import { FiPlus } from 'react-icons/fi'
import { Link } from 'react-router-dom'

const OrderDeliveryTimeHeader = () => {
    return (
        <>
            <div className="d-flex align-items-center gap-2 page-header-right-items-wrapper">
                <Link to="/orders/delivery-time/create" className="btn btn-primary">
                    <FiPlus size={16} className='me-2' />
                    <span>Create Delivery Time</span>
                </Link>
            </div>
        </>
    );
};

export default OrderDeliveryTimeHeader;
