import React, { useState } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { Link, useParams, useNavigate } from 'react-router-dom';

const ProductImageCreate = () => {
    const { id } = useParams();
    const navigate = useNavigate();

    const [productImages, setProductImages] = useState([]);
    const [previewImages, setPreviewImages] = useState([]);
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState(''); // 'success' or 'danger'

    const API_BASE_URL = 'http://127.0.0.1:8000/server_api/product';

    const handleImageChange = (e) => {
        const files = Array.from(e.target.files);
        setProductImages(files);
        const previewUrls = files.map(file => URL.createObjectURL(file));
        setPreviewImages(previewUrls);
    };

    const handleRemoveImages = () => {
        setProductImages([]);
        setPreviewImages([]);
        document.getElementById("productImages").value = "";
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (productImages.length === 0) {
            setMessage('At least one image is required!');
            setMessageType('danger');
            return;
        }

        const formData = new FormData();
        productImages.forEach(image => {
            formData.append('product_image_list', image);
        });

        axios.post(`${API_BASE_URL}/product-images/create/${id}/`, formData, {
            headers: {
                Authorization: `Bearer ${Cookies.get("accessToken")}`,
                "Content-Type": "multipart/form-data"
            }
        })
            .then(response => {
                setMessage(response.data.message);
                setMessageType('success');
                setProductImages([]);
                setPreviewImages([]);
                document.getElementById("productImages").value = "";
                navigate(`/products/image/${id}`);
            })
            .catch(error => {
                setMessage(error.response ? error.response.data.error : error.message);
                setMessageType('danger');
                navigate("/404");
            });
    };

    return (
        <div className="col-xl-12 p-2">
            {message && (
                <div className={`alert alert-${messageType} alert-dismissible fade show`} role="alert">
                    <strong>{messageType === 'danger' ? 'Error: ' : 'Success: '}</strong> {message}
                    <button type="button" className="btn-close" data-bs-dismiss="alert" aria-label="Close" onClick={() => setMessage('')}></button>
                </div>
            )}
            <div className="card invoice-container">
                <div className="card-header">
                    <h5>Upload Product Images</h5>
                    <Link to={`/products/image/${id}`} className="btn btn-primary">← Back</Link>

                </div>
                <div className="card-body p-0">
                    <form onSubmit={handleSubmit}>
                        <div className="px-4 py-4 row justify-content-between">
                            <div className="col-xl-6">
                                <div className="form-group mb-3 mt-3">

                                    <label htmlFor="productImages" className="form-label">Upload Product Images</label>
                                    <input
                                        type="file"
                                        className="form-control mb-2"
                                        id="productImages"
                                        accept="image/jpeg, image/png, image/jpg"
                                        multiple
                                        onChange={handleImageChange}
                                    />
                                    {previewImages.length > 0 && (
                                        <div className="mt-2 text-center">
                                            {previewImages.map((image, index) => (
                                                <img
                                                    key={index}
                                                    src={image}
                                                    alt={`Preview ${index + 1}`}
                                                    style={{ maxWidth: '200px', maxHeight: '150px', margin: '5px', display: 'inline-block' }}
                                                />
                                            ))}
                                            <button type="button" className="btn btn-danger mt-2" onClick={handleRemoveImages}>Remove Images</button>
                                        </div>
                                    )}
                                </div>
                                <button type="submit" className="btn btn-success">Upload Images</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default ProductImageCreate;
