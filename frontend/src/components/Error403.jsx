import React from 'react'
import { Link } from 'react-router-dom'

const Error403 = () => {
    return (
        <div className="card mb-4 mt-5 mx-5 position-relative">
            <div className="card-body p-sm-5 text-center">
                <h2 className="fw-bolder mb-4" style={{ fontSize: 120 }}>4<span className="text-danger">0</span>3</h2>
                <h4 className="fw-bold mb-2">Page not found</h4>
                <p className="fs-12 fw-medium text-muted">Sorry, the page you are looking for can't be found. Please check the URL or try to a different page on our site.</p>
                <div className="mt-5">
                    <Link to="/" className="btn btn-light-brand w-100">Back Home</Link>
                </div>
            </div>
        </div>

    )
}

export default Error403