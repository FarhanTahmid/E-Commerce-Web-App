import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';

const ProductCategoryCreate = () => {
    const [categoryName, setCategoryName] = useState('');
    const [categoryDescription, setCategoryDescription] = useState('');
    const [subCategories, setSubCategories] = useState([{ name: '', description: '' }]);
    const [categories, setCategories] = useState([]);
    const [prevSubCategories, setPrevSubCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState('');
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState(''); // 'success' or 'danger'

    const API_BASE_URL = 'http://127.0.0.1:8000/server_api/product';



    useEffect(() => {
        axios.get(`${API_BASE_URL}/categories/fetch-all/`, {
            headers: {
                Authorization: `Bearer ${Cookies.get("accessToken")}`,
                "Content-Type": "application/json"
            }
        })
            .then(response => {
                setCategories(response.data.product_category);
            })
            .catch(error => {
                setMessage(error.response ? error.response.data.message : error.message);
                setMessageType('danger');
            });
    }, []);

    useEffect(() => {
        if (selectedCategory) {
            axios.get(`${API_BASE_URL}/sub-categories/fetch-all-product-sub-categories-for-a-category/${selectedCategory}/`, {
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                    "Content-Type": "application/json"
                }
            })
                .then(response => {
                    setPrevSubCategories(response.data.product_sub_category || []);
                })
                .catch(error => {
                    setMessage(error.response ? error.response.data.message : error.message);
                    setMessageType('danger');
                });
        } else {
            setPrevSubCategories([]);
        }
    }, [selectedCategory]);

    const handleAddSubCategory = () => {
        setSubCategories([...subCategories, { name: '', description: '' }]);
    };

    const handleSubCategoryChange = (index, field, value) => {
        const updatedSubCategories = [...subCategories];
        updatedSubCategories[index][field] = value;
        setSubCategories(updatedSubCategories);
    };

    const handleRemoveSubCategory = (index) => {
        const updatedSubCategories = subCategories.filter((_, i) => i !== index);
        setSubCategories(updatedSubCategories);
    };

    const handleSubmitCategory = (e) => {
        e.preventDefault();

        if (!categoryName.trim()) {
            setMessage("Category name is required!");
            setMessageType('danger');
            return;
        }

        if (!categoryDescription.trim()) {
            setMessage("Category description is required!");
            setMessageType('danger');
            return;
        }

        axios.post(`${API_BASE_URL}/categories/create/`, {
            category_name: categoryName,
            description: categoryDescription
        }, {
            headers: {
                Authorization: `Bearer ${Cookies.get('accessToken')}`,
                "Content-Type": "application/json"
            }
        })
            .then(response => {
                setMessage(response.data.message);
                setMessageType('success');
                setCategoryName("");
                setCategoryDescription("");

                // Fetch updated categories instead of reloading
                axios.get(`${API_BASE_URL}/categories/fetch-all/`, {
                    headers: {
                        Authorization: `Bearer ${Cookies.get("accessToken")}`,
                        "Content-Type": "application/json"
                    }
                })
                    .then(response => {
                        setCategories(response.data.product_category);
                    })
                    .catch(error => {
                        console.error("Error fetching categories:", error);
                    });

            })
            .catch(error => {
                setMessage(error.response ? error.response.data.message : error.message);
                setMessageType('danger');
            });
    };

    const handleSubmitSubCategories = async (e) => {
        e.preventDefault();

        if (!selectedCategory) {
            setMessage("Please select a category first!");
            setMessageType('danger');
            return;
        }

        const validSubCategories = subCategories
            .map(sub => ({ sub_category_name: sub.name.trim(), description: sub.description.trim() }))
            .filter(sub => sub.sub_category_name !== "" && sub.description !== "");

        if (validSubCategories.length === 0) {
            setMessage("Please enter at least one valid subcategory name and description.");
            setMessageType('danger');
            return;
        }

        for (const subCategory of validSubCategories) {
            try {
                await axios.post(`${API_BASE_URL}/sub-categories/create/${selectedCategory}/`, subCategory, {
                    headers: {
                        Authorization: `Bearer ${Cookies.get('accessToken')}`,
                        "Content-Type": "application/json"
                    }
                });
            } catch (error) {
                console.error("Error creating subcategory:", error.response ? error.response.data : error);
            }
        }

        setMessage("All subcategories submitted successfully!");
        setMessageType('success');
        setSubCategories([{ name: '', description: '' }]); // Reset input fields
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
                    <h5>Category & Subcategory Creation</h5>
                </div>
                <div className="card-body p-0">
                    <form onSubmit={handleSubmitCategory}>
                        <div className="px-4 row justify-content-between">
                            <div className="col-xl-6">
                                <div className="form-group mb-3 mt-3">
                                    <label htmlFor="Category" className="form-label">New Category</label>
                                    <input
                                        type="text"
                                        className="form-control mb-2"
                                        value={categoryName}
                                        onChange={(e) => setCategoryName(e.target.value)}
                                        id="Category"
                                        placeholder="Category Name"
                                        required
                                    />
                                    <label htmlFor="Category" className="form-label">Category Description:</label>
                                    <textarea
                                        className="form-control mb-2"
                                        id="CategoryDescription"
                                        placeholder="Category Description"
                                        value={categoryDescription}
                                        onChange={(e) => setCategoryDescription(e.target.value)}
                                        required
                                    />
                                </div>
                                <button type="submit" className="btn btn-success">Create Category</button>
                            </div>
                        </div>
                    </form>

                    <hr className="border-dashed" />

                    <form onSubmit={handleSubmitSubCategories}>
                        <div className="row px-4 py-2">
                            <div className="col-xl-6">
                                <label htmlFor="CategorySelect" className="form-label">Select Category to create their Sub Categories</label>
                                <select
                                    className="form-control"
                                    id="CategorySelect"
                                    value={selectedCategory}
                                    onChange={(e) => setSelectedCategory(e.target.value)}
                                    required
                                >
                                    <option value="">Select a Category</option>
                                    {Array.isArray(categories) ? categories.map(category => (
                                        <option key={category.id} value={category.id}>{category.category_name}</option>
                                    )) : <option disabled>Loading...</option>}
                                </select>
                            </div>
                        </div>

                        {selectedCategory && (
                            <div className="row px-4 py-4">
                                <div className="col-xl-12">
                                    <div className='flex-wrap col-12 justify-content-between gap-3'>
                                        {/* Previous Sub Categories */}
                                        <div className='col-lg-12 col-md-12 col-sm-12 col-xl-6'>
                                            {prevSubCategories.length > 0 && (
                                                <>
                                                    <div className="card shadow-sm">
                                                        <div className="card-header d-flex justify-content-between align-items-center">
                                                            <h6 className="fw-bold mb-0">Sub Categories</h6>
                                                            <button
                                                                className="btn btn-primary btn-sm"
                                                                type="button"
                                                                data-bs-toggle="collapse"
                                                                data-bs-target="#subCategoriesCollapse"
                                                                aria-expanded="false"
                                                                aria-controls="subCategoriesCollapse"
                                                                id="toggleButton"
                                                            >
                                                                SHOW
                                                            </button>
                                                        </div>
                                                        <div id="subCategoriesCollapse" className="collapse">
                                                            <div className="card-body p-2">
                                                                <div className="border rounded p-2" style={{ maxHeight: '200px', overflowY: 'auto' }}>
                                                                    <ul className="list-unstyled mb-0">
                                                                        {prevSubCategories.map((subCategory, index) => (
                                                                            <li key={index} className="d-flex justify-content-between mb-3">
                                                                                <div>
                                                                                    {index + 1}. <strong>Name: {subCategory.sub_category_name}</strong>
                                                                                    <p className="mb-0">Description: {subCategory.description}</p>
                                                                                </div>
                                                                            </li>
                                                                        ))}
                                                                    </ul>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </>
                                            )}
                                        </div>


                                        {/* Sub Category Inputs */}
                                        <div className='col-lg-12 col-md-12 col-sm-12 col-xl-6 mt-4'>
                                            {subCategories.map((subCategory, index) => (
                                                <div key={index} className="form-group mb-3">
                                                    <label className="form-label">New Sub Category {index + 1}</label>
                                                    <input
                                                        type="text"
                                                        className="form-control mb-2"
                                                        placeholder="Sub Category Name"
                                                        value={subCategory.name}
                                                        onChange={(e) => handleSubCategoryChange(index, 'name', e.target.value)}
                                                    />
                                                    <textarea
                                                        type="text"
                                                        className="form-control mb-2"
                                                        placeholder="Sub Category Description"
                                                        value={subCategory.description}
                                                        onChange={(e) => handleSubCategoryChange(index, 'description', e.target.value)}
                                                    />
                                                    <button
                                                        type="button"
                                                        className="btn btn-danger mb-2"
                                                        onClick={() => handleRemoveSubCategory(index)}
                                                    >
                                                        Remove
                                                    </button>
                                                </div>
                                            ))}
                                        </div>
                                    </div>


                                    <hr className="border-dashed" />
                                    <div className="d-flex gap-3">
                                        <button type="button" className="btn btn-primary" onClick={handleAddSubCategory}>Add Sub Category</button>
                                        <button type="submit" className="btn btn-success">Submit Sub Categories</button>
                                    </div>
                                </div>
                            </div>
                        )}
                    </form>
                </div>
            </div>
        </div>
    );
};

export default ProductCategoryCreate;
