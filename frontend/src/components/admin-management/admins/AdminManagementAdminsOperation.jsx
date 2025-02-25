import React, { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import axios from 'axios';
import Cookies from 'js-cookie';
import Select from "react-select";
import ConfirmationModal from '../../ConfirmationModal';
import { BackendUrlMainAPI } from "../../../BackendUrlMainAPI";

const AdminManagementAdminsOperation = () => {
    const { admin_user_name } = useParams();
    const [adminPosition, setAdminPosition] = useState('');
    const [positions, setPositions] = useState([]);
    const [selectedPositionId, setSelectedPositionId] = useState('');
    const [extraPermissions, setExtraPermissions] = useState([]);
    const [selectedPermissions, setSelectedPermissions] = useState([]);
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState('');
    const [showDeleteModal, setShowDeleteModal] = useState(false);

    const API_BASE_URL = `${BackendUrlMainAPI}server_api/business-admin/admin-position`;
    const PERMISSIONS_API_URL = `${BackendUrlMainAPI}server_api/business-admin/admin-role-permission/fetch-role-permissions/`;

    useEffect(() => {
        fetchAdminPosition();
        fetchPermissions();
        // fetchExtraPermissions();
    }, []);

    // useEffect(() => {
    //     if (selectedPositionId) {
    //     }
    // }, [selectedPositionId]);

    const fetchAdminPosition = async () => {
        try {
            const response = await axios.post(`${API_BASE_URL}/fetch-position-for-admin/`, {
                admin_user_name: admin_user_name
            }, {
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                    "Content-Type": "application/json",
                }
            });
            setAdminPosition(response.data.position?.name || "");
            fetchPositions(response.data.position?.name || "");
        } catch (error) {
            console.error("Error fetching admin position:", error);
            fetchPositions("");
        }
    };

    const fetchPositions = async (adminPositionName) => {
        try {
            const response = await axios.get(`${API_BASE_URL}/fetch-positions/`, {
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` },
                params: { available: "True" }
            });
            const filteredPositions = response.data.admin_positions.filter(pos => pos.name !== adminPositionName);
            setPositions(filteredPositions);
        } catch (error) {
            setMessage(error.response?.data?.message || error.message);
            setMessageType('danger');
        }
    };

    const fetchPermissions = async () => {
        try {
            const response = await axios.get(`${BackendUrlMainAPI}server_api/business-admin/admin-permissions/fetch-admin-permissions/`, {
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` },
                params: { exclude: "True" }
            });
            console.log(response.data.admin_permission);
            const permissionsOptions = response.data.admin_permission.map(permission => ({
                value: permission.id,
                label: permission.permission_name
            }));
            setExtraPermissions(permissionsOptions);
        } catch (error) {
            console.error("Error fetching permissions:", error);
        }
    };

    // const fetchExtraPermissions = async () => {
    //     try {
    //         const response = await axios.get(PERMISSIONS_API_URL, {
    //             headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` },
    //         });
    //         console.log(response.data.admin_role_permission);
    //         const permissionsOptions = response.data.admin_role_permission.map(permission => ({
    //             value: permission.id,
    //             label: permission.name
    //         }));
    //         setExtraPermissions(permissionsOptions);
    //     } catch (error) {
    //         setMessage(error.response?.data?.message || error.message);
    //         setMessageType('danger');
    //     }
    // };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!selectedPositionId) {
            setMessage("Please select a position!");
            setMessageType('danger');
            return;
        }
        try {
            const url = adminPosition ? `${API_BASE_URL}/update-position-for-admin/` : `${API_BASE_URL}/add-position-for-admin/`;
            console.log(url);
            await axios({
                method: adminPosition ? 'put' : 'post',
                url: url,
                data: {
                    admin_user_name: admin_user_name,
                    extra_permissions_pk_list: selectedPermissions.map(p => p.value),
                    position_pk: selectedPositionId
                },
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                    "Content-Type": "application/json",
                }
            });
            setMessage("Admin position updated successfully!");
            setMessageType('success');
            fetchAdminPosition();
        } catch (error) {
            setMessage(error.response?.data.message || error.message);
            setMessageType('danger');
        }
    };

    return (
        <div className="col-xl-12 p-2">
            {message && (
                <div className={`alert alert-${messageType} alert-dismissible fade show`} role="alert">
                    <strong>{messageType === 'danger' ? 'Error: ' : 'Success: '}</strong> {message}
                    <button type="button" className="btn-close" onClick={() => setMessage('')}></button>
                </div>
            )}

            <div className="card invoice-container">
                <div className="card-header">
                    <h5>Admin Position Management</h5>
                    <Link to="/admin-management/admins" className="btn btn-primary">← Back</Link>
                </div>
                <div className="card-body p-0">
                    <form onSubmit={handleSubmit}>
                        <div className="px-4 py-4 row justify-content-between">
                            <h5 className="mt-3">Admin Username: {admin_user_name}</h5>
                            <span className="mt-3">Admin Position: {adminPosition || "Not Assigned"}</span>
                            <div className="col-xl-6">
                                <div className="form-group mb-3 mt-3">
                                    <label className="form-label">Select Position:</label>
                                    <select className="form-control" value={selectedPositionId} onChange={(e) => setSelectedPositionId(e.target.value)}>
                                        <option value="">Select a position</option>
                                        {positions.map(pos => <option key={pos.id} value={pos.id}>{pos.name}</option>)}
                                    </select>
                                </div>
                                <div className="form-group mb-3 mt-3">
                                    <label className="form-label">Select Extra Permissions:</label>
                                    <Select isMulti options={extraPermissions} value={selectedPermissions} onChange={setSelectedPermissions} />
                                </div>
                                <button type="submit" className="btn btn-primary mt-3">{adminPosition ? 'Update Admin Position' : 'Assign Admin Position'}</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default AdminManagementAdminsOperation;