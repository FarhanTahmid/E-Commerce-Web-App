import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { Link, useParams } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import ConfirmationModal from '../../ConfirmationModal'; // Import the modal component
import Select from "react-select";
import { set } from 'date-fns';


const ProductBrandUpdate = () => {
    const { id } = useParams(); // Get the ID from the URL
    const [brandName, setBrandName] = useState(''); // Initialize the position name state
    const [brandDescription, setBrandDescription] = useState(""); // Initialize the position description state
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState(''); // 'success' or 'danger'
    const [showDeleteModal, setShowDeleteModal] = useState(false); // Show/hide the delete modal
    const [deleteAction, setDeleteAction] = useState(null); // Store the delete action type
    const [brandEstablishedYear, setBrandEstablishedYear] = useState('');
    const [isOwnBrand, setIsOwnBrand] = useState(false);
    const [previewLogo, setPreviewLogo] = useState(null);
    const [brandCountry, setBrandCountry] = useState('');
    const [brandLogo, setBrandLogo] = useState(null);
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

    const API_BASE_URL = 'http://127.0.0.1:8000/server_api/product/product-brand'; // Define the API base URL
    const handleLogoChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setBrandLogo(file); // Store new file
            setPreviewLogo(URL.createObjectURL(file)); // Show new preview
        }
    };



    const handleRemoveLogo = () => {
        setPreviewLogo(null); // Remove preview
        setBrandLogo(null); // Clear file state
        document.getElementById("brandLogo").value = ""; // Reset file input
    };

    const navigate = useNavigate(); // Initialize the navigate hook

    const handleDeletePosition = () => {
        setDeleteAction({ type: 'position' });
        setShowDeleteModal(true);
    };

    const confirmDelete = () => {
        if (deleteAction.type === 'position') {
            fetch(`${API_BASE_URL}/delete/${id}/`, {
                method: 'DELETE',
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                    "Content-Type": "application/json"
                },
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to delete position');
                    }
                    setMessage('Brand deleted successfully!');
                    setMessageType('success');

                    // Redirect to the position list page after deletion
                    navigate('/products/brand');
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
        axios.get(`${API_BASE_URL}/fetch-product-brands/`, {
            headers: {
                Authorization: `Bearer ${Cookies.get("accessToken")}`,
                "Content-Type": "application/json"
            },
            params: { pk: id }
        })
            .then(response => {
                const fetchedLogo = response.data.product_brands.brand_logo || null;

                setBrandName(response.data.product_brands.brand_name || '');
                setBrandDescription(response.data.product_brands.brand_description || '');
                setBrandCountry(response.data.product_brands.brand_country || '');
                setBrandEstablishedYear(response.data.product_brands.brand_established_year || '');
                setIsOwnBrand(response.data.product_brands.is_own_brand || false);

                // If there is a brand logo, store only in preview, not in brandLogo state
                setPreviewLogo(fetchedLogo);
                setBrandLogo(null);
            })
            .catch(error => {
                console.error("Error fetching brand data:", error.response ? error.response.data : error);
            });
    }, []);




    const handleSubmitCategory = async (e) => {
        e.preventDefault();

        // Validate input fields
        if (!brandName.trim()) {
            alert("Brand name is required!");
            return;
        }

        if (!brandDescription.trim()) {
            alert("Brand description is required!");
            return;
        }

        // Ensure logo is present if the user removed the existing one
        if (!previewLogo && !brandLogo) {
            alert("You must upload a new brand logo after removing the previous one!");
            return;
        }

        const formData = new FormData();
        formData.append("brand_name", brandName);
        formData.append("brand_description", brandDescription);
        formData.append("brand_country", brandCountry);
        formData.append("brand_established_year", brandEstablishedYear);
        formData.append("is_own_brand", isOwnBrand ? 'True' : 'False');

        // Send "" if fetched logo was kept, otherwise send new file
        if (!brandLogo && previewLogo) {
            formData.append("brand_logo", ""); // Keep existing logo
        } else if (brandLogo) {
            formData.append("brand_logo", brandLogo); // Include new logo
        }
        console.log("🔍 FormData Debugging:");
        for (let pair of formData.entries()) {
            console.log(`${pair[0]}:`, pair[1]);
        }

        try {
            const response = await axios.put(`${API_BASE_URL}/update/${id}/`, formData, {
                headers: {
                    Authorization: `Bearer ${Cookies.get('accessToken')}`,
                    "Content-Type": "multipart/form-data",
                },
            });

            setBrandName(response.data.name);
            setBrandDescription(response.data.description);
            setMessage("Brand Updated Successfully!");
            setMessageType('success');

            // Reload the window after 1 second
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } catch (error) {
            console.error("Error Updating Brand:", error.response ? error.response.data : error.message);
            setMessage("Failed to update the brand.");
            setMessageType('danger');
        }
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
                    <h5>Brand Update & Deletion</h5>
                    <Link to="/products/brand" className="btn btn-primary">← Back</Link>
                </div>
                <div className="card-body p-0">
                    <form onSubmit={handleSubmitCategory}>
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


                                    {/* Show file input if no preview logo (or if the user removed it) */}
                                    {!previewLogo || brandLogo ? (
                                        <>
                                            <input
                                                type="file"
                                                className="form-control mb-2"
                                                id="brandLogo"
                                                accept="image/jpeg, image/png, image/jpg"
                                                onChange={handleLogoChange}
                                                required={!previewLogo && !brandLogo} // Required if no preview or existing logo
                                            />
                                        </>
                                    ) : null}

                                    {/* If there's a preview logo, show only the preview */}
                                    {previewLogo && (
                                        <div className="mt-2 text-center">
                                            <img
                                                src={previewLogo}
                                                alt="Brand Logo Preview"
                                                style={{ maxWidth: '200px', maxHeight: '150px', display: 'block', cursor: 'pointer' }}
                                                onClick={() => window.open(previewLogo, "_blank")}
                                            />
                                            <button type="button" className="btn btn-danger mt-2" onClick={handleRemoveLogo}>
                                                Remove Logo
                                            </button>
                                        </div>
                                    )}


                                </div>
                                <div className='d-flex gap-2'>
                                    <button type="submit" className="btn btn-success">Update Product Brand</button>
                                    <button
                                        type="button"
                                        className="btn btn-danger"
                                        onClick={handleDeletePosition}  // Call the function here
                                    >
                                        Delete Product Brand
                                    </button>
                                </div>
                            </div>
                        </div>
                    </form>

                    <ConfirmationModal
                        show={showDeleteModal}
                        onClose={cancelDelete}
                        onConfirm={confirmDelete}
                        message={`Are you sure you want to delete this position?`}
                    />
                </div>
            </div>
        </div>
    );
}

export default ProductBrandUpdate;
