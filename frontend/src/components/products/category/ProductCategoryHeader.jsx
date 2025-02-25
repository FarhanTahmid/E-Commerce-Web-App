import React from 'react'
import { FiPlus } from 'react-icons/fi'
import { Link } from 'react-router-dom'

const ProductCategoryHeader = () => {
    return (
        <>
            <div className="d-flex align-items-center gap-2 page-header-right-items-wrapper">
                <Link to="/products/category/create" className="btn btn-primary">
                    <FiPlus size={16} className='me-2' />
                    <span>Create Category</span>
                </Link>
            </div>
        </>
    );
};

export default ProductCategoryHeader;
