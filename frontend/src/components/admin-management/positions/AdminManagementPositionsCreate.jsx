import React, { useState } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { Link } from 'react-router-dom';

const AdminManagementPositionsCreate = () => {
    const [positionName, setPositionName] = useState('');
    const [positionDescription, setPositionDescription] = useState('');
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState(''); // 'success' or 'danger'

    const API_BASE_URL = 'http://127.0.0.1:8000/server_api/business-admin/admin-position';


    const handleSubmitCategory = (e) => {
        e.preventDefault();

        if (!positionName.trim()) {
            setMessage("Position name is required!");
            setMessageType('danger');
            return;
        }

        if (!positionDescription.trim()) {
            setMessage("Position description is required!");
            setMessageType('danger');
            return;
        }

        axios.post(`${API_BASE_URL}/create/`, {
            name: positionName,
            description: positionDescription
        }, {
            headers: {
                Authorization: `Bearer ${Cookies.get('accessToken')}`,
                "Content-Type": "application/json"
            }
        })
            .then(response => {
                setMessage(response.data.message);
                setMessageType('success');
                setPositionName("");
                setPositionDescription("");
            })
            .catch(error => {
                setMessage(error.response ? error.response.data.message : error.message);
                setMessageType('danger');
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
                    <h5>Admin Position Creation</h5>
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
                                    <label htmlFor="Position" className="form-label">Position Name:</label>
                                    <textarea
                                        className="form-control mb-2"
                                        id="PositionDescription"
                                        placeholder="Position Description"
                                        value={positionDescription}
                                        onChange={(e) => setPositionDescription(e.target.value)}
                                        required
                                    />
                                </div>
                                <button type="submit" className="btn btn-success">Create Admin Position</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default AdminManagementPositionsCreate;
