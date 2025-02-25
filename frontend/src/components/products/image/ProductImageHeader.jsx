import React from 'react'
import { FiPlus } from 'react-icons/fi'
import { Link } from 'react-router-dom'

const ProductImageHeader = () => {
    return (
        <>
            <div className="d-flex align-items-center gap-2 page-header-right-items-wrapper">
                <Link to="/products/image/create" className="btn btn-primary">
                    <FiPlus size={16} className='me-2' />
                    <span>Add Product Image</span>
                </Link>
            </div>
        </>
    );
};

export default ProductImageHeader;
