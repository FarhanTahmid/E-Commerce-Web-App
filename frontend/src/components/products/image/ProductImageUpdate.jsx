import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { Link, useParams, useNavigate } from 'react-router-dom';

const ProductImageUpdate = () => {
    const { id } = useParams(); // Get product ID from URL
    const navigate = useNavigate();
    const [productImages, setProductImages] = useState([]);
    const [selectedImage, setSelectedImage] = useState(null);
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState('');

    const API_BASE_URL = 'http://127.0.0.1:8000/server_api/product/product-images';

    useEffect(() => {
        fetchProductImages();
    }, []);

    const fetchProductImages = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/fetch-product-image/`, {
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                    "Content-Type": "application/json"
                },
                params: { product_pk: id }
            });
            setProductImages(response.data.product_image_data || []);
        } catch (error) {
            console.error('Error fetching product images:', error);
        }
    };

    const handleImageChange = (event, imageId) => {
        const file = event.target.files[0];
        if (file) {
            updateProductImage(imageId, file);
        }
    };

    const updateProductImage = async (imageId, file) => {
        const formData = new FormData();
        formData.append('product_image', file);

        try {
            await axios.put(`${API_BASE_URL}/update/${imageId}/`, formData, {
                headers: {
                    Authorization: `Bearer ${Cookies.get('accessToken')}`,
                    'Content-Type': 'multipart/form-data'
                }
            });
            setMessage('Product image updated successfully!');
            setMessageType('success');
            fetchProductImages();
        } catch (error) {
            setMessage('Failed to update the image.');
            setMessageType('danger');
        }
    };

    const deleteProductImage = async (imageId) => {
        try {
            await axios.delete(`${API_BASE_URL}/delete/${imageId}/`, {
                headers: { Authorization: `Bearer ${Cookies.get('accessToken')}` }
            });
            setMessage('Product image deleted successfully!');
            setMessageType('success');
            fetchProductImages();
        } catch (error) {
            setMessage('Failed to delete the image.');
            setMessageType('danger');
        }
    };

    return (
        <div className="col-xl-12 p-2">
            {message && (
                <div
                    className={`alert alert-${messageType} alert-dismissible fade show`}
                    role="alert"
                    style={{ marginBottom: '20px' }}
                >
                    <strong>{messageType === 'danger' ? 'Error: ' : 'Success: '}</strong> {message}
                    <button
                        type="button"
                        className="btn-close"
                        data-bs-dismiss="alert"
                        aria-label="Close"
                        onClick={() => setMessage('')} // Close message on button click
                    ></button>
                </div>
            )}

            <div className="card invoice-container">
                <div className="card-header">
                    <h5>Product Image Update & Deletion</h5>
                    <Link to="/products/image" className="btn btn-primary">← Back</Link>
                </div>
                <div className="card-body p-0">
                    {productImages.length > 0 ? (
                        <div className="row">
                            {productImages.map(image => (
                                <div key={image.id} className="col-md-3 text-center">
                                    <img src={image.image_url} alt="Product" className="img-fluid" />
                                    <input type="file" className="form-control mt-2" onChange={(e) => handleImageChange(e, image.id)} />
                                    <button className="btn btn-danger mt-2" onClick={() => deleteProductImage(image.id)}>Delete</button>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="alert alert-info">No images added. <button className="btn btn-primary" onClick={() => navigate(`/products/image/${id}/create`)}>Add Images</button></div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ProductImageUpdate;
