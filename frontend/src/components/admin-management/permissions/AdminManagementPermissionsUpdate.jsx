import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { Link, useParams, useNavigate } from 'react-router-dom';
import ConfirmationModal from '../../ConfirmationModal';
import { BackendUrlMainAPI } from '../../../BackendUrlMainAPI';

const AdminManagementPermissionsUpdate = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const API_BASE_URL = `${BackendUrlMainAPI}server_api/business-admin`;
    const [positions, setPositions] = useState([]);
    const [permissions, setPermissions] = useState([]);
    const [rolePermissions, setRolePermissions] = useState([]);
    const [selectedPermissions, setSelectedPermissions] = useState([]);
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState('');

    useEffect(() => {
        fetchPermissions();
        fetchRolePermission();
        fetchPositions();
    }, []);

    const fetchPositions = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/admin-position/fetch-positions/`, {
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` }
            });

            const PositionsList = response.data.admin_positions.map(c => ({ value: c.id, label: c.name }));

            // Find the Positions name based on Positions_id
            const selectedPosition = PositionsList.find(positions => positions.value === parseInt(id));

            if (selectedPosition) {
                setPositions(selectedPosition.label);
            }
        } catch (error) {
            console.error("Error fetching positions:", error);
        }
    };

    const fetchPermissions = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/admin-permissions/fetch-admin-permissions/`, {
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` }
            });
            setPermissions(response.data.admin_permission);
        } catch (error) {
            console.error("Error fetching permissions:", error);
        }
    };

    const fetchRolePermission = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/admin-role-permission/fetch-role-permissions/`, {
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` },
                params: { admin_position_pk: id }
            });
            const assignedPermissions = response.data.admin_role_permission.map(perm => perm.permission);
            setRolePermissions(response.data.admin_role_permission);
            setSelectedPermissions(assignedPermissions);
        } catch (error) {
            console.error("Error fetching role permissions:", error);
        }
    };

    const handleCheckboxChange = (permId) => {
        setSelectedPermissions(prev =>
            prev.includes(permId) ? prev.filter(id => id !== permId) : [...prev, permId]
        );
    };

    const handleCreatePermissions = async () => {
        try {
            await axios.post(`${API_BASE_URL}/admin-role-permission/create/`, {
                admin_position_pk: id,
                admin_permission_pk_list: selectedPermissions
            }, {
                headers: { Authorization: `Bearer ${Cookies.get('accessToken')}` }
            });
            setMessage("Permissions assigned successfully!");
            setMessageType('success');
            window.location.reload();
        } catch (error) {
            console.error("Error assigning permissions:", error);
        }
    };

    const handleUpdatePermissions = async () => {
        try {
            await axios.put(`${API_BASE_URL}/admin-role-permission/update/${id}/`, {
                admin_permission_pk_list: selectedPermissions
            }, {
                headers: { Authorization: `Bearer ${Cookies.get('accessToken')}` }
            });
            setMessage("Permissions updated successfully!");
            setMessageType('success');
            window.location.reload();
        } catch (error) {
            console.error("Error updating permissions:", error);
        }
    };

    const handleRemovePermissions = async () => {
        try {
            await axios.delete(`${API_BASE_URL}/admin-role-permission/delete/${id}/`, {
                headers: { Authorization: `Bearer ${Cookies.get('accessToken')}` }
            });
            setSelectedPermissions([]);
            setMessage("Permissions removed successfully!");
            setMessageType('success');
            window.location.reload();
        } catch (error) {
            console.error("Error removing permissions:", error);
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
            <div className="card">
                <div className="card-header">
                    <h5>Manage Role Permissions for {positions}</h5>
                    <Link to="/admin-management/role-permissions" className="btn btn-primary">← Back</Link>
                </div>
                <div className="card-body">
                    <h6>Assign Permissions:</h6>
                    {permissions.map((perm) => (
                        <div key={perm.id} style={{ marginBottom: '5px', display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                            <input
                                type="checkbox"
                                id={`perm-${perm.id}`}
                                checked={selectedPermissions.includes(perm.id)}
                                onChange={() => handleCheckboxChange(perm.id)}
                                style={{ cursor: 'pointer' }}
                            />
                            <label htmlFor={`perm-${perm.id}`} style={{ marginLeft: '5px', cursor: 'pointer' }}>{perm.permission_name}</label>
                        </div>
                    ))}
                    <div className="mt-3">
                        {!rolePermissions.length ? (
                            <button className="btn btn-success" onClick={handleCreatePermissions}>Assign Permissions</button>
                        ) : (
                            <>
                                <div className='d-flex gap-2'>
                                    <button className="btn btn-warning" onClick={handleUpdatePermissions}>Update Permissions</button>
                                    <button className="btn btn-danger" onClick={handleRemovePermissions}>Remove All Permissions</button>
                                </div>
                            </>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AdminManagementPermissionsUpdate;
