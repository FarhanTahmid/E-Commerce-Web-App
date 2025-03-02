import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import Cookies from 'js-cookie';
import { TablePagination, Switch } from '@mui/material';
import { BackendUrlMainAPI } from '../../../BackendUrlMainAPI';

const AdminManagementLoginRequestsTable = () => {
    const [admins, setAdmins] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(5);
    const API_BASE_URL = `${BackendUrlMainAPI}server_api/business-admin/admin`;

    useEffect(() => {
        fetchAdmins();
    }, []);

    const fetchAdmins = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/fetch-all/`, {
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                    "Content-Type": "application/json"
                }
            });
            const adminUsers = response.data.admin_users;
            const adminsWithRequests = await Promise.all(
                adminUsers.map(async (admin) => {
                    const loginRequest = await fetchLoginRequest(admin.admin_unique_id);
                    return { ...admin, login_request: loginRequest };
                })
            );
            setAdmins(adminsWithRequests);
        } catch (error) {
            console.error("Error fetching admins:", error.response ? error.response.data : error);
        }
    };

    const fetchLoginRequest = async (adminId) => {
        try {
            const response = await axios.get(`${BackendUrlMainAPI}server_api/business-admin/login-request/fetch/?admin_unique_id=${adminId}`, {
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                    "Content-Type": "application/json"
                }
            });
            return response.data.fetched_data?.login_request || false;
        } catch (error) {
            console.error(`Error fetching login request for admin ${adminId}:`, error);
            return false;
        }
    };

    const handleSearch = (event) => {
        setSearchTerm(event.target.value);
    };

    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };

    const handleToggleAccess = async (adminId, currentStatus) => {
        try {
            await axios.put(`${BackendUrlMainAPI}server_api/business-admin/login-request/update/${adminId}/`, {
                status: currentStatus ? "False" : "True"
            }, {
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                    "Content-Type": "application/json"
                }
            });
            setAdmins((prevAdmins) =>
                prevAdmins.map((admin) =>
                    admin.admin_unique_id === adminId ? { ...admin, login_request: !currentStatus } : admin
                )
            );
        } catch (error) {
            console.error(`Error updating login request for admin ${adminId}:`, error);
        }
    };

    const filteredAdmins = admins.filter(admin =>
        admin.admin_full_name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <>
            <div className="col-lg-12">
                <div className="card stretch stretch-full function-table">
                    <div className="card-body p-0">
                        <div className="table-responsive">
                            <div className='dataTables_wrapper dt-bootstrap5 no-footer'>
                                <div className='row gy-2'>
                                    <div className='col-xl-12 col-md-6 ps-0 m-0 pb-10'>
                                        <div className='dataTables_filter d-flex justify-content-md-end justify-content-center'>
                                            <label className='d-inline-flex align-items-center gap-2'>
                                                Search:
                                                <input
                                                    type="text"
                                                    value={searchTerm}
                                                    onChange={handleSearch}
                                                    placeholder='Search...'
                                                    className="form-control form-control-sm"
                                                />
                                            </label>
                                        </div>
                                    </div>
                                </div>
                                <div className="col-xl-12 px-0">
                                    <table className="table table-hover dataTable no-footer" id='projectList'>
                                        <thead>
                                            <tr>
                                                <th>Serial No</th>
                                                <th>Admin Full Name</th>
                                                <th>Admin Email Address</th>
                                                <th>Login Request Access</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {filteredAdmins.length === 0 ? (
                                                <tr>
                                                    <td colSpan="4" className="text-center">
                                                        No records available
                                                    </td>
                                                </tr>
                                            ) : (
                                                filteredAdmins.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((admin, index) => (
                                                    <tr key={admin.id || admin.admin_email} className='single-item chat-single-item'>
                                                        <td>{index + 1 + page * rowsPerPage}</td>
                                                        <td className="truncate-text">
                                                            <Link to={`/admin-management/admins/${admin.admin_user_name}`} className='fw-bold'>{admin.admin_full_name}</Link>
                                                        </td>
                                                        <td className="truncate-text">{admin.admin_email}</td>
                                                        <td>
                                                            <Switch
                                                                checked={admin.login_request}
                                                                onChange={() => handleToggleAccess(admin.admin_unique_id, admin.login_request)}
                                                            />
                                                        </td>
                                                    </tr>
                                                ))
                                            )}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <TablePagination
                rowsPerPageOptions={[5, 10, 25]}
                component="div"
                count={filteredAdmins.length}
                rowsPerPage={rowsPerPage}
                page={page}
                onPageChange={handleChangePage}
                onRowsPerPageChange={handleChangeRowsPerPage}
            />
        </>
    );
};

export default AdminManagementLoginRequestsTable;
