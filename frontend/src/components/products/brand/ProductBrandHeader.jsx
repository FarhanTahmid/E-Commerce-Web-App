import React from 'react'
import { FiPlus } from 'react-icons/fi'
import { Link } from 'react-router-dom'

const ProductBrandHeader = () => {
    return (
        <>
            <div className="d-flex align-items-center gap-2 page-header-right-items-wrapper">
                <Link to="/products/brand/create" className="btn btn-primary">
                    <FiPlus size={16} className='me-2' />
                    <span>Create Brand</span>
                </Link>
            </div>
        </>
    );
};

export default ProductBrandHeader;
