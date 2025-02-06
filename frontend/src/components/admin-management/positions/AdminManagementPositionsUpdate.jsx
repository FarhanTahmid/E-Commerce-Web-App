import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { Link, useParams } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import ConfirmationModal from '../../ConfirmationModal'; // Import the modal component

const AdminManagementPositionsUpdate = () => {
    const { id } = useParams(); // Get the ID from the URL
    const [positionName, setPositionName] = useState(''); // Initialize the position name state
    const [positionDescription, setPositionDescription] = useState(""); // Initialize the position description state
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState(''); // 'success' or 'danger'
    const [showDeleteModal, setShowDeleteModal] = useState(false); // Show/hide the delete modal
    const [deleteAction, setDeleteAction] = useState(null); // Store the delete action type

    const API_BASE_URL = 'http://127.0.0.1:8000/server_api/business-admin/admin-position'; // Define the API base URL

    const navigate = useNavigate(); // Initialize the navigate hook

    const handleDeletePosition = () => {
        setDeleteAction({ type: 'position' });
        setShowDeleteModal(true);
    };

    const confirmDelete = () => {
        if (deleteAction.type === 'position') {
            fetch(`${API_BASE_URL}/delete/${id}/`, {
                method: 'DELETE',
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                    "Content-Type": "application/json"
                },
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to delete position');
                    }
                    setMessage('Position deleted successfully!');
                    setMessageType('success');

                    // Redirect to the position list page after deletion
                    navigate('/admin-management/positions');
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
        axios.get(`${API_BASE_URL}/fetch-positions/`, {
            headers: {
                Authorization: `Bearer ${Cookies.get("accessToken")}`,
                "Content-Type": "application/json"
            },
            params: { pk: id }
        })
            .then(response => {
                setPositionName(response.data.admin_positions.name || '');
                setPositionDescription(response.data.admin_positions.description || '');
            })
            .catch(error => {
                console.error("Error fetching categories:", error.response ? error.response.data : error);
            });
    }, []);


    const handleSubmitCategory = (e) => {
        e.preventDefault();

        // Validate input fields
        if (!positionName.trim()) {
            alert("Position name is required!");
            return;
        }

        if (!positionDescription.trim()) {
            alert("Position description is required!");
            return;
        }

        // Change the method to PUT or PATCH based on your backend
        axios.put(`${API_BASE_URL}/update/${id}/`, {
            name: positionName,
            description: positionDescription
        }, {
            headers: {
                Authorization: `Bearer ${Cookies.get('accessToken')}`,
                "Content-Type": "application/json"
            }
        })
            .then(response => {
                setPositionName(response.data.name);
                setPositionDescription(response.data.description);
                setMessage("Position Updated Successfully!");
                setMessageType('success');
            })
            .catch(error => {
                console.error("Error Updating position:", error.response ? error.response.data : error.message);
            });

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
                    <h5>Admin Position Update & Deletion</h5>
                    <Link to="/admin-management/positions" className="btn btn-primary">← Back</Link>
                </div>
                <div className="card-body p-0">
                    <form onSubmit={handleSubmitCategory}>
                        <div className="px-4 py-4 row justify-content-between">
                            <div className="col-xl-6">
                                <div className="form-group mb-3 mt-3">
                                    <label htmlFor="Position" className="form-label">Position Name:</label>
                                    <input
                                        type="text"
                                        className="form-control mb-2"
                                        value={positionName}
                                        onChange={(e) => setPositionName(e.target.value)}
                                        id="PositionName"
                                        placeholder="Position Name"
                                        required
                                    />
                                    <label htmlFor="Position" className="form-label">Position Description:</label>
                                    <textarea
                                        type="text"
                                        className="form-control mb-2"
                                        id="PositionDescription"
                                        placeholder="Position Description"
                                        value={positionDescription}
                                        onChange={(e) => setPositionDescription(e.target.value)}
                                        required
                                    />
                                </div>
                                <div className='d-flex gap-2'>
                                    <button type="submit" className="btn btn-success">Update Admin Position</button>
                                    <button
                                        type="button"
                                        className="btn btn-danger"
                                        onClick={handleDeletePosition}  // Call the function here
                                    >
                                        Delete Admin Position
                                    </button>
                                </div>
                            </div>
                        </div>
                    </form>

                    <ConfirmationModal
                        show={showDeleteModal}
                        onClose={cancelDelete}
                        onConfirm={confirmDelete}
                        message={`Are you sure you want to delete this position?`}
                    />
                </div>
            </div>
        </div>
    );
}

export default AdminManagementPositionsUpdate;
