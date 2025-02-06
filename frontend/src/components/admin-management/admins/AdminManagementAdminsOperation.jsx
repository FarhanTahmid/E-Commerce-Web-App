import React, { useState, useEffect } from 'react';
import Cookies from 'js-cookie';
import { Link } from 'react-router-dom';

const AdminManagementAdminsOperation = () => {
    const [positionName, setPositionName] = useState('');
    const [positionDescription, setPositionDescription] = useState('');
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState(''); // 'success' or 'danger'
    const [positions, setPositions] = useState([]);
    const [editMode, setEditMode] = useState(false);
    const [currentPositionId, setCurrentPositionId] = useState(null);
    const [selectedPositionId, setSelectedPositionId] = useState(null);

    const API_BASE_URL = 'http://127.0.0.1:8000/server_api/business-admin/admin-position';

    // Dummy Data for Existing Positions
    useEffect(() => {
        // Simulating fetching positions
        setPositions([
            { id: 1, name: 'Manager', description: 'Oversees department activities' },
            { id: 2, name: 'Developer', description: 'Develops software products' },
            { id: 3, name: 'Designer', description: 'Designs user interfaces and experiences' },
        ]);
    }, []);

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

        const apiCall = editMode
            ? axios.put(`${API_BASE_URL}/update/${currentPositionId}/`, {
                name: positionName,
                description: positionDescription
            })
            : axios.post(`${API_BASE_URL}/create/`, {
                name: positionName,
                description: positionDescription
            });

        apiCall
            .then(response => {
                setMessage(response.data.message);
                setMessageType('success');
                setPositionName("");
                setPositionDescription("");
                setEditMode(false);
                setCurrentPositionId(null);
                setSelectedPositionId(null);
                // Simulate refresh of positions (in real use, call fetchPositions)
                setPositions([...positions, { id: Math.random(), name: positionName, description: positionDescription }]);
            })
            .catch(error => {
                setMessage(error.response ? error.response.data.message : error.message);
                setMessageType('danger');
            });
    };

    const handleEditPosition = (position) => {
        setPositionName(position.name);
        setPositionDescription(position.description);
        setEditMode(true);
        setCurrentPositionId(position.id);
        setSelectedPositionId(position.id);
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
                    <h5>Admin Position Management</h5>
                    <Link to="/admin-management/positions" className="btn btn-primary">← Back</Link>
                </div>
                <div className="card-body p-0">
                    <form onSubmit={handleSubmitCategory}>
                        <div className="px-4 py-4 row justify-content-between">
                            <div className="col-xl-6">
                                <div className="form-group mb-3 mt-3">
                                    {/* Dropdown to Select Position */}
                                    <label htmlFor="Position" className="form-label">Select Position:</label>
                                    <select
                                        className="form-control mb-2"
                                        value={selectedPositionId || ''}
                                        onChange={(e) => {
                                            const selectedId = e.target.value;
                                            setSelectedPositionId(selectedId);
                                            if (selectedId) {
                                                const selectedPosition = positions.find(position => position.id === parseInt(selectedId));
                                                setPositionName(selectedPosition.name);
                                                setPositionDescription(selectedPosition.description);
                                                setEditMode(true);
                                                setCurrentPositionId(selectedPosition.id);
                                            } else {
                                                setPositionName('');
                                                setPositionDescription('');
                                                setEditMode(false);
                                            }
                                        }}
                                    >
                                        <option value="">Select an existing position</option>
                                        {positions.map((position) => (
                                            <option key={position.id} value={position.id}>{position.name}</option>
                                        ))}
                                    </select>

                                    {/* Position Name and Description */}
                                    <label htmlFor="PositionName" className="form-label">Position Name:</label>
                                    <input
                                        type="text"
                                        className="form-control mb-2"
                                        value={positionName}
                                        onChange={(e) => setPositionName(e.target.value)}
                                        id="PositionName"
                                        placeholder="Position Name"
                                        required
                                    />
                                    <label htmlFor="PositionDescription" className="form-label">Position Description:</label>
                                    <textarea
                                        className="form-control mb-2"
                                        id="PositionDescription"
                                        placeholder="Position Description"
                                        value={positionDescription}
                                        onChange={(e) => setPositionDescription(e.target.value)}
                                        required
                                    />
                                </div>
                                <button type="submit" className="btn btn-success">
                                    {editMode ? 'Update Admin Position' : 'Create Admin Position'}
                                </button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default AdminManagementAdminsOperation;
