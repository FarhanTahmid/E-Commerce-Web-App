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
    const [adminPositionPK, setAdminPositionPK] = useState('');
    const [positions, setPositions] = useState([]);
    const [selectedPositionId, setSelectedPositionId] = useState('');
    const [extraPermissions, setExtraPermissions] = useState([]);
    const [selectedPermissions, setSelectedPermissions] = useState([]);
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState('');
    const [showConfirmModal, setShowConfirmModal] = useState(false);
    const [changePosition, setChangePosition] = useState(false);

    const API_BASE_URL = `${BackendUrlMainAPI}server_api/business-admin/admin-position`;
    const admin_extra_permissions_list = `${BackendUrlMainAPI}server_api/business-admin/admin-extra-permissions/fetch-extra-permissions-for-admin/`;

    useEffect(() => {
        fetchAdminPosition();
        fetchPermissions();
        fetchAdminExtraPermissions();
    }, []);

    const fetchAdminExtraPermissions = async () => {
        try {
            const response = await axios.post(admin_extra_permissions_list, {
                admin_user_name: admin_user_name
            }, {
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` }
            });
            console.log(response.data.position);

            const permissionsOptions = response.data.position.map(permission => ({
                value: permission.id,
                label: permission.permission_name
            }));

            console.log(permissionsOptions);
        } catch (error) {
            console.error("Error fetching extra permissions:", error);
        }
    };

    const fetchAdminPosition = async () => {
        try {
            const response = await axios.post(`${API_BASE_URL}/fetch-position-for-admin/`, {
                admin_user_name
            }, {
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` }
            });
            setAdminPositionPK(response.data.position?.id || '');
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
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` }
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
            const permissionsOptions = response.data.admin_permission.map(permission => ({
                value: permission.id,
                label: permission.permission_name
            }));
            setExtraPermissions(permissionsOptions);
        } catch (error) {
            console.error("Error fetching permissions:", error);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        let position_pk = changePosition ? selectedPositionId : adminPositionPK;
        if (!adminPosition) {
            position_pk = selectedPositionId;
        }
        if (!position_pk) {
            setMessage("Please select a position!");
            setMessageType('danger');
            return;
        }

        try {
            const url = adminPosition ? `${API_BASE_URL}/update-position-for-admin/` : `${API_BASE_URL}/add-position-for-admin/`;
            await axios({
                method: adminPosition ? 'put' : 'post',
                url,
                data: {
                    admin_user_name,
                    extra_permissions_pk_list: selectedPermissions.map(p => p.value),
                    position_pk
                },
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` }
            });
            setMessage("Admin position updated successfully!");
            setMessageType('success');
            window.location.reload();
        } catch (error) {
            setMessage(error.response?.data.message || error.message);
            setMessageType('danger');
        }
    };

    return (
        <div className="col-xl-12 p-2">
            {message && <div className={`alert alert-${messageType}`} role="alert">{message}</div>}
            <div className="card">
                <div className="card-header">
                    <h5>Admin Position Management</h5>
                    <Link to="/admin-management/admins" className="btn btn-primary">← Back</Link>
                </div>
                <div className="card-body">
                    <form onSubmit={handleSubmit}>
                        <h5>Admin Username: {admin_user_name}</h5>
                        <p>Admin Position: {adminPosition || "Not Assigned"}</p>

                        {adminPosition && !changePosition && (
                            <button type="button" className="btn btn-warning mb-3" onClick={() => setShowConfirmModal(true)}>
                                I want to change the position
                            </button>
                        )}

                        {(changePosition || !adminPosition) && (
                            <div className="form-group">
                                <label>Select Position:</label>
                                <select className="form-control" value={selectedPositionId} onChange={(e) => setSelectedPositionId(e.target.value)} required>
                                    <option value="">Select a position</option>
                                    {positions.map(pos => <option key={pos.id} value={pos.id}>{pos.name}</option>)}
                                </select>
                            </div>
                        )}

                        <div className="form-group">
                            <label>Select Extra Permissions:</label>
                            <Select isMulti options={extraPermissions} value={selectedPermissions} onChange={setSelectedPermissions} />
                        </div>

                        <button type="submit" className="btn btn-primary mt-3">{adminPosition ? 'Update Admin Position' : 'Assign Admin Position'}</button>
                        {adminPosition && (
                            <button type="button" className="btn btn-danger mt-3 ml-3" onClick={() => setChangePosition(false)}>Delete Admin Position</button>
                        )}
                    </form>
                </div>
            </div>

            {showConfirmModal && (
                <ConfirmationModal
                    show={showConfirmModal}
                    onClose={() => setShowConfirmModal(false)}
                    onConfirm={() => { setChangePosition(true); setShowConfirmModal(false); }}
                    title="Change Position Confirmation"
                    message="Are you sure you want to change the position?"
                    option="Yes"
                />
            )}
        </div>
    );
};

export default AdminManagementAdminsOperation;