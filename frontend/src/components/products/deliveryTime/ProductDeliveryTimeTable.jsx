import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import Cookies from 'js-cookie';
import {
    TablePagination
} from '@mui/material';

const ProductDeliveryTimeTable = () => {
    const [deliveries, setDeliveries] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(5);
    const API_BASE_URL = 'http://127.0.0.1:8000/server_api/business-admin/delivery-time';

    useEffect(() => {
        fetchCategories();
    }, []);

    const fetchCategories = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/fetch/`, {
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                    "Content-Type": "application/json"
                }
            });
            console.log(response.data);

            if (response.data && response.data.delivery_time_data) {
                setDeliveries(response.data.delivery_time_data);
            } else {
                console.error("Unexpected response format:", response.data);
            }
        } catch (error) {
            console.error("Error fetching deliveries:", error.response?.data || error);
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

    const filteredDeliveries = deliveries.filter(delivery =>
        (delivery.delivery_name || "").toLowerCase().includes(searchTerm.toLowerCase())
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

                                <div className="">
                                    <div className="col-xl-12 px-0">
                                        <table className="table table-hover dataTable no-footer" id='projectList'>
                                            <thead>
                                                <tr>
                                                    <th>Serial No</th>
                                                    <th>Delivery Name</th>
                                                    <th>Estimated Time</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {filteredDeliveries.length === 0 ? (
                                                    <tr>
                                                        <td colSpan="3" className="text-center">No records available</td>
                                                    </tr>
                                                ) : (
                                                    filteredDeliveries.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((delivery, index) => (
                                                        <tr key={delivery.id} className="single-item chat-single-item">
                                                            <td>{index + 1 + page * rowsPerPage}</td>
                                                            <td className="truncate-text">
                                                                <Link to={`/products/delivery-time/${delivery.id}`} className="fw-bold">
                                                                    {delivery.delivery_name}
                                                                </Link>
                                                            </td>
                                                            <td className="truncate-text">
                                                                <Link to={`/products/delivery-time/${delivery.id}`} className="fw-normal">
                                                                    {delivery.estimated_time}
                                                                </Link>
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
            </div>
            <TablePagination
                rowsPerPageOptions={[5, 10, 25]}
                component="div"
                count={filteredDeliveries.length}
                rowsPerPage={rowsPerPage}
                page={page}
                onPageChange={handleChangePage}
                onRowsPerPageChange={handleChangeRowsPerPage}
            />
        </>
    );
};

export default ProductDeliveryTimeTable;