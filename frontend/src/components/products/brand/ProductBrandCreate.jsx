import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import Select from "react-select";
import { Link } from 'react-router-dom';

const ProductBrandCreate = () => {
    const [brandName, setBrandName] = useState('');
    const [brandEstablishedYear, setBrandEstablishedYear] = useState('');
    const [isOwnBrand, setIsOwnBrand] = useState(false);
    const [brandCountry, setBrandCountry] = useState('');
    const [brandDescription, setBrandDescription] = useState('');
    const [brandLogo, setBrandLogo] = useState(null);
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState(''); // 'success' or 'danger'
    const [countries, setCountries] = useState([]);

    useEffect(() => {
        // Fetch list of countries
        fetch("https://restcountries.com/v3.1/all")
            .then(response => response.json())
            .then(data => {
                // Sort countries alphabetically by their common name
                const sortedCountries = data
                    .map(country => ({
                        value: country.name.common,
                        label: country.name.common
                    }))
                    .sort((a, b) => a.label.localeCompare(b.label));

                setCountries(sortedCountries);
            })
            .catch(error => console.error("Error fetching countries:", error));
    }, []);

    const API_BASE_URL = 'http://127.0.0.1:8000/server_api/product';

    const handleSubmit = (e) => {
        e.preventDefault();

        // Validate required fields
        if (!brandName.trim()) {
            setMessage('Brand name is required!');
            setMessageType('danger');
            return;
        }
        if (!brandEstablishedYear.trim()) {
            setMessage('Brand established year is required!');
            setMessageType('danger');
            return;
        }

        // Prepare form data
        const formData = new FormData();
        formData.append('brand_name', brandName);
        formData.append('brand_established_year', brandEstablishedYear);
        formData.append('is_own_brand', isOwnBrand ? 'True' : 'False'); // Send 'True' or 'False' as strings
        formData.append('brand_country', brandCountry);
        formData.append('brand_description', brandDescription);
        if (brandLogo) {
            formData.append('brand_logo', brandLogo);
        }

        // Make API request
        axios.post(`${API_BASE_URL}/product-brand/create/`, formData, {
            headers: {
                Authorization: `Bearer ${Cookies.get("accessToken")}`,
                "Content-Type": "multipart/form-data"
            }
        })
            .then(response => {
                setMessage(response.data.message);
                setMessageType('success');
                // Reset form fields
                setBrandName('');
                setBrandEstablishedYear('');
                setIsOwnBrand(false);
                setBrandCountry('');
                setBrandDescription('');
                setBrandLogo('');
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
                    <h5>Create Product Brand</h5>
                    <Link to="/products/brand" className="btn btn-primary">← Back</Link>
                </div>
                <div className="card-body p-0">
                    <form onSubmit={handleSubmit}>
                        <div className="px-4 py-4 row justify-content-between">
                            <div className="col-xl-6">
                                <div className="form-group mb-3 mt-3">
                                    <label htmlFor="brandName" className="form-label">Brand Name</label>
                                    <input
                                        type="text"
                                        className="form-control mb-2"
                                        id="brandName"
                                        placeholder="Brand Name"
                                        value={brandName}
                                        onChange={(e) => setBrandName(e.target.value)}
                                        required
                                    />
                                    <label htmlFor="brandEstablishedYear" className="form-label">Brand Established Year</label>
                                    <input
                                        type="number"
                                        className="form-control mb-2"
                                        id="brandEstablishedYear"
                                        placeholder="Year"
                                        value={brandEstablishedYear}
                                        onChange={(e) => setBrandEstablishedYear(e.target.value)}
                                        required
                                    />
                                    <label htmlFor="isOwnBrand" className="form-label">Is it your own brand?</label><br />
                                    <div className="form-check form-check-inline">
                                        <input
                                            type="radio"
                                            className="form-check-input form-control mb-2"
                                            id="yesOption"
                                            name="isOwnBrand"
                                            value="yes"
                                            checked={isOwnBrand === true}
                                            onChange={() => setIsOwnBrand(true)}  // Ensure boolean value here
                                        />
                                        <label htmlFor="yesOption" className="form-check-label">Yes</label>
                                    </div>
                                    <div className="form-check form-check-inline mb-2">
                                        <input
                                            type="radio"
                                            className="form-check-input form-control mb-2"
                                            id="noOption"
                                            name="isOwnBrand"
                                            value="no"
                                            checked={isOwnBrand === false}
                                            onChange={() => setIsOwnBrand(false)}  // Ensure boolean value here
                                        />
                                        <label htmlFor="noOption" className="form-check-label">No</label>
                                    </div>

                                    <br />
                                    <label htmlFor="brandCountry" className="form-label">Brand Country</label>
                                    <Select
                                        id="brandCountry"
                                        className='mb-2'
                                        value={brandCountry ? { value: brandCountry, label: brandCountry } : null}
                                        onChange={(selectedOption) => setBrandCountry(selectedOption.value)}
                                        options={countries}
                                        placeholder="Select a country"
                                        isClearable
                                    />
                                    <label htmlFor="brandDescription" className="form-label">Brand Description</label>
                                    <textarea
                                        className="form-control mb-2"
                                        id="brandDescription"
                                        placeholder="Brand Description"
                                        value={brandDescription}
                                        onChange={(e) => setBrandDescription(e.target.value)}
                                    />
                                    <label htmlFor="brandLogo" className="form-label">Brand Logo</label>
                                    <input
                                        type="file"
                                        className="form-control mb-2"
                                        id="brandLogo"
                                        accept="image/*"  // This restricts the input to image files only
                                        onChange={(e) => setBrandLogo(e.target.files[0])}
                                    />
                                </div>
                                <button type="submit" className="btn btn-success">Create Brand</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default ProductBrandCreate;
