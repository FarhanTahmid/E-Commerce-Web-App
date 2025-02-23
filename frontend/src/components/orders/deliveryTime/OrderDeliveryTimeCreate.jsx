import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import Select from "react-select";
import { Link } from 'react-router-dom';

const OrderDeliveryTimeCreate = () => {
    const [deliveryName, setDeliveryName] = useState('');
    const [estimatedTime, setEstimatedTime] = useState('');
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState(''); // 'success' or 'danger'

    const API_BASE_URL = 'http://127.0.0.1:8000/server_api/business-admin';

    const handleSubmit = (e) => {
        e.preventDefault();

        if (!deliveryName.trim()) {
            setMessage('Delivery name is required!');
            setMessageType('danger');
            return;
        }

        if (!estimatedTime.trim()) {
            setMessage('Estimated Time is required!');
            setMessageType('danger');
            return;
        }

        axios.post(`${API_BASE_URL}/delivery-time/create/`, {
            delivery_name: deliveryName,
            estimated_time: estimatedTime
        }, {
            headers: {
                Authorization: `Bearer ${Cookies.get("accessToken")}`,
                "Content-Type": "application/json"
            }
        })
            .then(response => {
                setMessage(response.data.message);
                setMessageType('success');
                setDeliveryName('');
                setEstimatedTime('');
            })
            .catch(error => {
                setMessage(error.response ? error.response.data.message : error.message);
                setMessageType('danger');
            });
    };

    return (
        <div className="col-xl-12 p-2">
            {message && (
                <div className={`alert alert-${messageType} alert-dismissible fade show`} role="alert">
                    <strong>{messageType === 'danger' ? 'Error: ' : 'Success: '}</strong> {message}
                    <button type="button" className="btn-close" data-bs-dismiss="alert" aria-label="Close" onClick={() => setMessage('')}></button>
                </div>
            )}
            <div className="card invoice-container">
                <div className="card-header">
                    <h5>Create Delivery Time</h5>
                    <Link to="/orders/delivery-time" className="btn btn-primary">← Back</Link>
                </div>
                <div className="card-body p-0">
                    <form onSubmit={handleSubmit}>
                        <div className="px-4 py-4 row justify-content-between">
                            <div className="col-xl-6">
                                <div className="form-group mb-3 mt-3">
                                    <label htmlFor="deliveryName" className="form-label">Delivery Name</label>
                                    <input
                                        type="text"
                                        className="form-control mb-2"
                                        id="deliveryName"
                                        placeholder="Delivery Name (e.g. Inside Dhaka)"
                                        value={deliveryName}
                                        onChange={(e) => setDeliveryName(e.target.value)}
                                        required
                                    />
                                </div>
                                <div className="form-group mb-3 mt-3">
                                    <label htmlFor="estimatedTime" className="form-label">Estimated Time</label>
                                    <input
                                        type="text"
                                        className="form-control mb-2"
                                        id="estimatedTime"
                                        placeholder="Estimated Time (e.g. 1-2 days)"
                                        value={estimatedTime}
                                        onChange={(e) => setEstimatedTime(e.target.value)}
                                        required
                                    />
                                </div>
                                <button type="submit" className="btn btn-success">Create Delivery Time</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default OrderDeliveryTimeCreate;
