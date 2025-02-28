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
    const [showDeleteModal, setShowDeleteModal] = useState(false); // Show/hide the delete modal
    const [deleteAction, setDeleteAction] = useState(null); // Store the delete action type

    const API_BASE_URL = `${BackendUrlMainAPI}server_api/business-admin/admin-position`;
    const admin_extra_permissions_list = `${BackendUrlMainAPI}server_api/business-admin/admin-extra-permissions/fetch-extra-permissions-for-admin/`;

    const handleDeletePosition = () => {
        setDeleteAction({ type: 'position' });
        setShowDeleteModal(true);
    };

    const confirmDelete = () => {
        if (deleteAction.type === 'position') {
            fetch(`${API_BASE_URL}/delete-position-for-admin/`, {
                method: 'DELETE',
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ admin_user_name: admin_user_name, delete: "True" })
            })
                .then(response => {
                    console.log("response", response);

                    setMessage('Position deleted successfully!');
                    setMessageType('success');

                    window.location.reload();
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
        fetchAdminPosition();
        // fetchPermissions();
        fetchAdminExtraPermissions();
    }, []);

    const fetchAdminExtraPermissions = async () => {
        try {
            const response = await axios.post(admin_extra_permissions_list, {
                admin_user_name: admin_user_name
            }, {
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` }
            });

            const permissionsOptions = response.data.position.map(permission => ({
                value: permission.id,
                label: permission.permission_name
            }));

            setSelectedPermissions(permissionsOptions); // Set existing permissions

            fetchPermissions(permissionsOptions); // Pass existing permissions to filter later
        } catch (error) {
            console.error("Error fetching extra permissions:", error);
            fetchPermissions([]); // Pass existing permissions to filter later

        }
    };

    const fetchPermissions = async (existingPermissions = []) => {
        try {
            const response = await axios.get(`${BackendUrlMainAPI}server_api/business-admin/admin-permissions/fetch-admin-permissions/`, {
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` },
                params: { exclude: "True" }
            });

            const allPermissions = response.data.admin_permission.map(permission => ({
                value: permission.id,
                label: permission.permission_name
            }));

            // Filter out the permissions that are already assigned
            const filteredPermissions = allPermissions.filter(
                permission => !existingPermissions.some(existing => existing.value === permission.value)
            );

            setExtraPermissions(filteredPermissions); // Show only unassigned permissions
        } catch (error) {
            console.error("Error fetching permissions:", error);
        }
    };

    // Handle change in selection dynamically
    const handlePermissionChange = (selectedOptions) => {
        // Determine newly selected and deselected permissions
        const newlyDeselected = selectedPermissions.filter(sp => !selectedOptions.some(selected => selected.value === sp.value));

        // Update selected permissions
        setSelectedPermissions(selectedOptions);

        // Re-add deselected permissions to the available list
        setExtraPermissions(prevPermissions => [...prevPermissions, ...newlyDeselected]);
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

    // const fetchPermissions = async () => {
    //     try {
    //         const response = await axios.get(`${BackendUrlMainAPI}server_api/business-admin/admin-permissions/fetch-admin-permissions/`, {
    //             headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` },
    //             params: { exclude: "True" }
    //         });
    //         const permissionsOptions = response.data.admin_permission.map(permission => ({
    //             value: permission.id,
    //             label: permission.permission_name
    //         }));
    //         setExtraPermissions(permissionsOptions);
    //     } catch (error) {
    //         console.error("Error fetching permissions:", error);
    //     }
    // };

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
            console.log("selectedPermissions", selectedPermissions);
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
                    <h5>Admin Position Management</h5>
                    <Link to="/admin-management/admins" className="btn btn-primary">← Back</Link>
                </div>
                <div className="card-body">
                    <form onSubmit={handleSubmit}>
                        <h5>Admin Username: {admin_user_name}</h5>
                        <p>Admin Position: {adminPosition || "Not Assigned"}</p>



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
                            <Select isMulti options={extraPermissions} value={selectedPermissions} onChange={handlePermissionChange} />
                        </div>

                        <div className='d-flex gap-2 mb-3'>
                            <button type="submit" className="btn btn-primary mt-3">{adminPosition ? 'Update Admin Position' : 'Assign Admin Position'}</button>
                            {adminPosition && (
                                <button type="button" className="btn btn-danger mt-3 ml-3" onClick={handleDeletePosition}>Delete Admin Position</button>
                            )}
                        </div>


                        {adminPosition && !changePosition && (
                            <span style={{ cursor: "pointer" }} className="mb-3" onClick={() => setShowConfirmModal(true)}>
                                Want to change the position? Click here!
                            </span>
                        )}
                    </form>
                </div>
            </div>

            {showDeleteModal && (
                <ConfirmationModal
                    show={showDeleteModal}
                    onClose={cancelDelete}
                    onConfirm={confirmDelete}
                    message={`Are you sure you want to delete?`}
                />
            )}

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