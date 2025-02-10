import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import Select from "react-select";
import { Link } from 'react-router-dom';

const ProductFlavourCreate = () => {
    const [flavourName, setFlavourName] = useState('');
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState(''); // 'success' or 'danger'

    const API_BASE_URL = 'http://127.0.0.1:8000/server_api/product';

    const handleSubmit = (e) => {
        e.preventDefault();

        if (!flavourName.trim()) {
            setMessage('Flavour name is required!');
            setMessageType('danger');
            return;
        }

        axios.post(`${API_BASE_URL}/product-flavour/create/`, {
            product_flavour_name: flavourName
        }, {
            headers: {
                Authorization: `Bearer ${Cookies.get("accessToken")}`,
                "Content-Type": "application/json"
            }
        })
            .then(response => {
                setMessage(response.data.message);
                setMessageType('success');
                setFlavourName('');
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
                    <h5>Create Product Flavour</h5>
                    <Link to="/products/flavour" className="btn btn-primary">← Back</Link>
                </div>
                <div className="card-body p-0">
                    <form onSubmit={handleSubmit}>
                        <div className="px-4 py-4 row justify-content-between">
                            <div className="col-xl-6">
                                <div className="form-group mb-3 mt-3">
                                    <label htmlFor="flavourName" className="form-label">Flavour Name</label>
                                    <input
                                        type="text"
                                        className="form-control mb-2"
                                        id="flavourName"
                                        placeholder="Flavour Name"
                                        value={flavourName}
                                        onChange={(e) => setFlavourName(e.target.value)}
                                        required
                                    />
                                </div>
                                <button type="submit" className="btn btn-success">Create Flavour</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default ProductFlavourCreate;
