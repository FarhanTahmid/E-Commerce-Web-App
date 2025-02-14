import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { Link, useParams, useNavigate } from 'react-router-dom';
import ConfirmationModal from '../../ConfirmationModal';

const ProductImageUpdate = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [products, setProducts] = useState('');
    const [productImages, setProductImages] = useState([]);
    const [selectedImages, setSelectedImages] = useState({});
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState('');
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [deleteImageId, setDeleteImageId] = useState(null);
    const [showUpdateModal, setShowUpdateModal] = useState(false);
    const [updateImageId, setUpdateImageId] = useState(null);

    const API_BASE_URL = 'http://127.0.0.1:8000/server_api/product';

    useEffect(() => {
        fetchProducts();
    });


    const fetchProducts = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/fetch-product/`, {
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` }
            });

            const productList = response.data.product_data.map(c => ({ value: c.id, label: c.product_name }));

            // Find the product name based on product_id
            const selectedProduct = productList.find(product => product.value === parseInt(id));

            if (selectedProduct) {
                setProducts(selectedProduct.label);
            }
        } catch (error) {
            console.error("Error fetching products:", error);
        }
    };

    useEffect(() => {
        fetchProductImages();
    }, []);

    const fetchProductImages = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/product-images/fetch-product-image/`, {
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

    const handleDeleteRequest = (imageId) => {
        setDeleteImageId(imageId);
        setShowDeleteModal(true);
    };

    const confirmDelete = async () => {
        try {
            await axios.delete(`${API_BASE_URL}/product-image/delete/${deleteImageId}/`, {
                headers: { Authorization: `Bearer ${Cookies.get('accessToken')}` }
            });
            window.location.reload();
        } catch (error) {
            setMessage('Failed to delete the image.');
            setMessageType('danger');
        }
        setShowDeleteModal(false);
    };

    const handleFileChange = (e, imageId) => {
        setSelectedImages(prevState => ({ ...prevState, [imageId]: e.target.files[0] }));
    };

    const handleUpdateRequest = (imageId) => {
        setUpdateImageId(imageId);
        setShowUpdateModal(true);
    };

    const confirmUpdate = async () => {
        if (!selectedImages[updateImageId]) return;

        const formData = new FormData();
        formData.append('new_image', selectedImages[updateImageId]);

        try {
            await axios.put(`${API_BASE_URL}/product-image/update/${updateImageId}/`, formData, {
                headers: {
                    Authorization: `Bearer ${Cookies.get('accessToken')}`,
                    'Content-Type': 'multipart/form-data'
                }
            });
            window.location.reload();
        } catch (error) {
            setMessage('Failed to update the image.');
            setMessageType('danger');
        }
        setShowUpdateModal(false);
    };

    return (
        <div className="col-xl-12 p-2">
            {message && (
                <div className={`alert alert-${messageType} alert-dismissible fade show`} role="alert">
                    <strong>{messageType === 'danger' ? 'Error: ' : 'Success: '}</strong> {message}
                    <button type="button" className="btn-close" data-bs-dismiss="alert" onClick={() => setMessage('')}></button>
                </div>
            )}
            <div className="card invoice-container">
                <div className="card-header">
                    <h5>{products}</h5>
                    <div className="d-flex gap-2">
                        {productImages.length > 0 ? <Link to={`/products/image/${id}/create`} className="btn btn-primary">Add More</Link> : null}
                        <Link to="/products/image" className="btn btn-primary">← Back</Link>
                    </div>
                </div>
                <div className="card-body p-4">
                    {productImages.length > 0 ? (
                        <div className="row gap-4" style={{
                            justifyContent: 'space-between',
                        }}>
                            {productImages.map(image => (
                                <div key={image.id} className="col-md-3 text-center">
                                    <img src={image.product_image} alt="Product" style={{ cursor: "pointer" }} className="img-fluid" onClick={() => window.open(image.product_image, '_blank')} />
                                    <input type="file" className="form-control mt-2" accept=".jpg,.jpeg,.png" onChange={(e) => handleFileChange(e, image.id)} />
                                    {selectedImages[image.id] && <button className="btn btn-warning mt-2" onClick={() => handleUpdateRequest(image.id)}>Update</button>}
                                    <button className="btn btn-danger mt-2" onClick={() => handleDeleteRequest(image.id)}>Delete</button>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="alert alert-info">No images added. <button className="btn btn-primary" onClick={() => navigate(`/products/image/${id}/create`)}>Add Images</button></div>
                    )}
                </div>
            </div>

            <ConfirmationModal
                show={showDeleteModal}
                onClose={() => setShowDeleteModal(false)}
                onConfirm={confirmDelete}
                message="Are you sure you want to delete this image?"
            />
            <ConfirmationModal
                show={showUpdateModal}
                onClose={() => setShowUpdateModal(false)}
                onConfirm={confirmUpdate}
                message="Are you sure you want to update this image?"
                option="Update"
            />
        </div>
    );
};

export default ProductImageUpdate;
