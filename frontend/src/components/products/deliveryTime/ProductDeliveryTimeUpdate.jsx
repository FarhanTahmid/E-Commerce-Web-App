import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { Link, useParams } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import ConfirmationModal from '../../ConfirmationModal'; // Import the modal component
import Select from "react-select";
import { set } from 'date-fns';


const ProductDeliveryTimeUpdate = () => {
    const { id } = useParams(); // Get the ID from the URL
    const [flavourName, setFlavourName] = useState(''); // Initialize the flavour name state
    const [deliveryName, setDeliveryName] = useState('');
    const [estimatedTime, setEstimatedTime] = useState('');
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState(''); // 'success' or 'danger'
    const [showDeleteModal, setShowDeleteModal] = useState(false); // Show/hide the delete modal
    const [deleteAction, setDeleteAction] = useState(null); // Store the delete action type

    const API_BASE_URL = 'http://127.0.0.1:8000/server_api/business-admin/delivery-time'; // Define the API base URL

    const navigate = useNavigate(); // Initialize the navigate hook

    const handleDeleteflavour = () => {
        setDeleteAction({ type: 'flavour' });
        setShowDeleteModal(true);
    };

    const confirmDelete = () => {
        if (deleteAction.type === 'flavour') {
            fetch(`${API_BASE_URL}/delete/${id}/`, {
                method: 'DELETE',
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                    "Content-Type": "application/json"
                },
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to delete flavour');
                    }
                    setMessage('Flavour deleted successfully!');
                    setMessageType('success');

                    // Redirect to the flavour list page after deletion
                    navigate('/products/flavour');
                })
                .catch(error => {
                    setMessage(error.message);
                    setMessageType('danger');
                });
        }

        // Close the modal after confirmation
        setShowDeleteModal(false);
    };

    const cancelDelete = () => {
        setShowDeleteModal(false);
    };


    useEffect(() => {
        axios.get(`${API_BASE_URL}/fetch/`, {
            headers: {
                Authorization: `Bearer ${Cookies.get("accessToken")}`,
                "Content-Type": "application/json"
            },
            params: { delivery_pk: id }
        })
            .then(response => {
                console.log(response.data);
                setDeliveryName(response.data.delivery_time_data.delivery_name || '');
                setEstimatedTime(response.data.delivery_time_data.estimated_delivery_time || '');
            })
            .catch(error => {
                console.error("Error fetching Flavour data:", error.response ? error.response.data : error);
            });
    }, []);




    const handleSubmitCategory = async (e) => {
        e.preventDefault();

        // Validate input fields
        if (!flavourName.trim()) {
            alert("Flavour name is required!");
            return;
        }

        try {
            const response = await axios.put(`${API_BASE_URL}/update/${id}/`, {
                product_flavour_name: flavourName
            }, {
                headers: {
                    Authorization: `Bearer ${Cookies.get('accessToken')}`,
                    "Content-Type": "application/json",
                },
            });

            setFlavourName(response.data.name);
            setMessage("Flavour Updated Successfully!");
            setMessageType('success');
        } catch (error) {
            console.error("Error Updating Flavour:", error.response ? error.response.data : error.message);
            setMessage("Failed to update the Flavour.");
            setMessageType('danger');
        }
    };



    return (
        <div className="col-xl-12 p-2">
            {/* Message Container */}
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
                    <h5>Flavour Update & Deletion</h5>
                    <Link to="/products/delivery-time" className="btn btn-primary">← Back</Link>
                </div>
                <div className="card-body p-0">
                    <form onSubmit={handleSubmitCategory}>
                        <div className="px-4 py-4 row justify-content-between">
                            <div className="col-xl-6">
                                <div className="form-group mb-3 mt-3">
                                    <label htmlFor="deliveryName" className="form-label">Delivery Name</label>
                                    <input
                                        type="text"
                                        className="form-control mb-2"
                                        id="deliveryName"
                                        placeholder="Delivery Name (e.g. Inside Dhaka)"
                                        value={deliveryName}
                                        onChange={(e) => setDeliveryName(e.target.value)}
                                        required
                                    />
                                </div>
                                <div className="form-group mb-3 mt-3">
                                    <label htmlFor="estimatedTime" className="form-label">Estimated Time</label>
                                    <input
                                        type="text"
                                        className="form-control mb-2"
                                        id="estimatedTime"
                                        placeholder="Estimated Time (e.g. 1-2 days)"
                                        value={estimatedTime}
                                        onChange={(e) => setEstimatedTime(e.target.value)}
                                        required
                                    />
                                </div>
                                <div className='d-flex gap-2'>
                                    <button type="submit" className="btn btn-success">Update Product Flavour</button>
                                    <button
                                        type="button"
                                        className="btn btn-danger"
                                        onClick={handleDeleteflavour}  // Call the function here
                                    >
                                        Delete Product Flavour
                                    </button>
                                </div>
                            </div>
                        </div>
                    </form>

                    <ConfirmationModal
                        show={showDeleteModal}
                        onClose={cancelDelete}
                        onConfirm={confirmDelete}
                        message={`Are you sure you want to delete this flavour?`}
                    />
                </div>
            </div>
        </div>
    );
}

export default ProductDeliveryTimeUpdate;
