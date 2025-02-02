import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';


const ProductCategoryCreate = () => {
    const [categoryName, setCategoryName] = useState('');
    const [categoryDescription, setCategoryDescription] = useState("");
    const [subCategories, setSubCategories] = useState([{ name: '', description: '' }]); // Add description field
    const [categories, setCategories] = useState([]);
    const [prevSubCategories, setPrevSubCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState('');
    const API_BASE_URL = 'http://127.0.0.1:8000/server_api/product';

    useEffect(() => {

        axios.get(`${API_BASE_URL}/categories/fetch-all/`, {
            headers: {
                Authorization: `Bearer ${Cookies.get("accessToken")}`, // Ensure token is not undefined/null
                "Content-Type": "application/json"
            }
        })
            .then(response => {
                console.log("Categories Response:", response.data); // Debug response
                setCategories(response.data.product_category);
            })
            .catch(error => {
                console.error("Error fetching categories:", error.response ? error.response.data : error);
            });
    }, []);

    useEffect(() => {
        if (selectedCategory) {

            axios.get(`${API_BASE_URL}/sub-categories/fetch-all-product-sub-categories-for-a-category/${selectedCategory}/`, {
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`, // Ensure token is not undefined/null
                    "Content-Type": "application/json"
                }
            })
                .then(response => {
                    console.log("Categories Response:", response.data); // Debug response
                    // Ensure response.data is an array
                    setPrevSubCategories(Array.isArray(response.data.product_category) ? response.data.product_category : []);
                })
                .catch(error => {
                    console.error("Error fetching categories:", error.response ? error.response.data : error);
                });
        }

    }, []);


    const handleAddSubCategory = () => {
        setSubCategories([...subCategories, { name: '', description: '' }]); // Add an empty description field
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

        // Validate input fields
        if (!categoryName.trim()) {
            alert("Category name is required!");
            return;
        }

        if (!categoryDescription.trim()) {
            alert("Category description is required!");
            return;
        }

        axios.post(`${API_BASE_URL}/categories/create/`, {
            category_name: categoryName,
            description: categoryDescription  // Now sending the description as well
        },
            {
                headers: {
                    Authorization: `Bearer ${Cookies.get('accessToken')}`,  // Send token in request headers
                    "Content-Type": "application/json"
                }
            })
            .then(response => {
                alert("Category Created Successfully!");
                setCategories([...categories, response.data.product_category]); // Update UI
                setCategoryName("");
                setCategoryDescription("");  // Clear the input fields

                // Refresh the page after category creation
                window.location.reload(); // This will reload the page
            })
            .catch(error => {
                console.error("Error creating category:", error);
                alert("Failed to create category.");
            });
    };

    const handleSubmitSubCategories = (e) => {
        e.preventDefault();

        // Validation: Check if a category is selected
        if (!selectedCategory) {
            alert("Please select a category first!");
            return;
        }

        // Validation: Ensure no empty subcategories and descriptions
        const validSubCategories = subCategories
            .map(sub => ({ name: sub.name.trim(), description: sub.description.trim() }))
            .filter(sub => sub.name !== "" && sub.description !== ""); // Ensure both name and description are filled

        if (validSubCategories.length === 0) {
            alert("Please enter at least one valid subcategory name and description.");
            return;
        }

        // Submit each valid subcategory
        validSubCategories.forEach(subCategory => {
            axios.post(`${API_BASE_URL}/product/sub-categories/create/${selectedCategory}/`, subCategory)
                .then(response => {
                    alert(`Subcategory "${subCategory.name}" Created Successfully!`);
                })
                .catch(error => console.error("Error creating subcategory:", error));
        });

        // Reset input fields after successful submission
        setSubCategories([{ name: '', description: '' }]);
    };



    return (
        <div className="col-xl-12 p-2">
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
                                    <input
                                        type="text"
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
                        <div className="row px-4 py-4">
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

                        {selectedCategory && ( // Conditional rendering based on selectedCategory
                            <div className="row px-4 py-4">
                                <div className="col-xl-6">
                                    {prevSubCategories.length > 0 && (
                                        <>
                                            <h6 className="fw-bold">Sub Categories:</h6>
                                            <ul className='list-unstyled'>
                                                {prevSubCategories.map((subCategory, index) => (
                                                    <li key={index} className="d-flex gap-2 mb-2">
                                                        {subCategory.name}
                                                    </li>
                                                ))}
                                            </ul>
                                        </>
                                    )}

                                    <h6 className="fw-bold">New Sub Categories:</h6>
                                    {subCategories.map((subCategory, index) => (
                                        <div key={index} className="d-flex gap-2 mb-2">
                                            <input
                                                type="text"
                                                className={`form-control ${subCategory.name.trim() === "" ? "border-danger" : ""}`}
                                                value={subCategory.name}
                                                onChange={(e) => handleSubCategoryChange(index, 'name', e.target.value)}
                                                placeholder="Subcategory Name"
                                                required
                                            />
                                            <input
                                                type="text"
                                                className={`form-control ${subCategory.description.trim() === "" ? "border-danger" : ""}`}
                                                value={subCategory.description}
                                                onChange={(e) => handleSubCategoryChange(index, 'description', e.target.value)}
                                                placeholder="Subcategory Description"
                                                required
                                            />
                                            <button type="button" className="btn btn-danger" onClick={() => handleRemoveSubCategory(index)}>-</button>
                                        </div>
                                    ))}

                                    <div className="d-flex gap-2">
                                        <button type="button" className="btn btn-secondary mt-2" onClick={handleAddSubCategory}>+ Add Subcategory</button>
                                        <button type="submit" className="btn btn-success mt-2">Create Subcategories</button>
                                    </div>
                                </div>
                            </div>
                        )}
                    </form>

                </div>
            </div>
        </div>
    );
}

export default ProductCategoryCreate;
