import React, { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import axios from 'axios';
import Cookies from 'js-cookie';

const AdminManagementAdminsOperation = () => {
    const { admin_user_name } = useParams();
    const [adminPosition, setAdminPosition] = useState('');
    const [positions, setPositions] = useState([]);
    const [selectedPositionId, setSelectedPositionId] = useState('');
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState(''); // 'success' or 'danger'

    const API_BASE_URL = 'http://127.0.0.1:8000/server_api/business-admin/admin-position';

    const fetchAdminPosition = () => {
        axios.post(`${API_BASE_URL}/fetch-position-for-admin/`, {
            admin_user_name: admin_user_name
        }, {
            headers: {
                Authorization: `Bearer ${Cookies.get("accessToken")}`,
                "Content-Type": "application/json",
            }
        })
            .then(response => {
                console.log("Admin Position Data:", response.data.position); // Debugging
                setAdminPosition(response.data.position); // Ensure only a string is stored
            })
            .catch(error => {
                console.error("API Error:", error.response);
                setMessage(error.response ? error.response.data.message : error.message);
                setMessageType('danger');
            });
    };



    const fetchPositions = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/fetch-positions/`, {
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                }
            });

            console.log("API Response:", response.data); // Debugging Step

            if (Array.isArray(response.data.admin_positions)) {
                const filteredPositions = response.data.admin_positions.filter(pos => pos.name !== adminPosition);
                setPositions(filteredPositions);
            } else {
                console.error("Expected an array, but received:", response.data);
                setMessage("Invalid response format from server.");
                setMessageType('danger');
            }
        } catch (error) {
            setMessage(error.response?.data?.message || error.message);
            setMessageType('danger');
        }
    };



    useEffect(() => {
        fetchAdminPosition();
        fetchPositions();
    }, [adminPosition]);

    // Handle Position Update
    const handleUpdatePosition = async (e) => {
        e.preventDefault();

        if (!selectedPositionId) {
            setMessage("Please select a position!");
            setMessageType('danger');
            return;
        }

        try {
            const response = await axios.post(`${API_BASE_URL}/add-or-update-position-for-admin/`, {
                admin_user_name: admin_user_name,
                position_pk: selectedPositionId
            }, {
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                    "Content-Type": "application/json",
                }
            });

            setMessage(response.data.message);
            setMessageType('success');
            fetchAdminPosition();
            fetchPositions();
        } catch (error) {
            setMessage(error.response?.data.message || error.message);
            setMessageType('danger');
        }
    };

    // Handle Position Removal
    const handleRemovePosition = async () => {
        try {
            const response = await axios.post(`${API_BASE_URL}/remove-admin-position/`, {
                admin_user_name
            });

            setMessage(response.data.message);
            setMessageType('success');
            setAdminPosition('');
            fetchPositions();
        } catch (error) {
            setMessage(error.response?.data.message || error.message);
            setMessageType('danger');
        }
    };

    return (
        <div className="col-xl-12 p-2">
            {/* Message Container */}
            {message && (
                <div className={`alert alert-${messageType} alert-dismissible fade show`} role="alert">
                    <strong>{messageType === 'danger' ? 'Error: ' : 'Success: '}</strong> {message}
                    <button type="button" className="btn-close" data-bs-dismiss="alert" aria-label="Close" onClick={() => setMessage('')}></button>
                </div>
            )}

            <div className="card invoice-container">
                <div className="card-header">
                    <h5>Admin Position Management</h5>
                    <Link to="/admin-management/admins" className="btn btn-primary">← Back</Link>
                </div>
                <div className="card-body p-0">
                    <form onSubmit={handleUpdatePosition}>
                        <div className="px-4 py-4 row justify-content-between">
                            <h5 className="mt-3">Admin Username: {admin_user_name}</h5>
                            <span className="mt-3">
                                Admin Position: {adminPosition?.name || "Not Assigned"}
                            </span>
                            <div className="col-xl-6">
                                <div className="form-group mb-3 mt-3">
                                    <label htmlFor="Position" className="form-label">Select Position:</label>
                                    <select
                                        className="form-control mb-2"
                                        value={selectedPositionId}
                                        onChange={(e) => setSelectedPositionId(e.target.value)}
                                    >
                                        <option value="">Select a new position</option>
                                        {positions.map((position) => (
                                            <option key={position.id} value={position.id}>{position.name}</option>
                                        ))}
                                    </select>
                                </div>
                                <button type="submit" className="btn btn-success">Update Admin Position</button>
                                {adminPosition && (
                                    <button type="button" className="btn btn-danger ms-2" onClick={handleRemovePosition}>
                                        Remove Admin Position
                                    </button>
                                )}
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default AdminManagementAdminsOperation;
