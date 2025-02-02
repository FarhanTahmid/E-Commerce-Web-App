import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';



const ProductCategoryUpdate = () => {
    const { id } = useParams();
    const [categoryName, setCategoryName] = useState('');
    const [categoryDescription, setCategoryDescription] = useState("");
    const [subCategories, setSubCategories] = useState([{ name: '', description: '' }]); // Add description field
    const [categories, setCategories] = useState([]);
    const [prevSubCategories, setPrevSubCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState('');
    const API_BASE_URL = 'http://127.0.0.1:8000/server_api/product';
    const [newSubCategoryName, setNewSubCategoryName] = useState('');
    const [newSubCategoryDescription, setNewSubCategoryDescription] = useState('');
    // Inside your component:
    const navigate = useNavigate();

    const handleAddSubCategory = () => {
        if (newSubCategoryName.trim() && newSubCategoryDescription.trim()) {
            const newSubCategory = {
                sub_category_name: newSubCategoryName,
                description: newSubCategoryDescription
            };

            // Make the API call to create a new subcategory
            fetch(`${API_BASE_URL}/sub-categories/create/${id}/`, {
                method: 'POST',
                body: JSON.stringify(newSubCategory),
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`, // Ensure token is not undefined/null
                    "Content-Type": "application/json"
                }
            })
                .then((response) => {
                    // Check if the response is successful
                    if (response.ok) {
                        return response.json(); // Return the JSON response
                    } else {
                        throw new Error('Failed to add subcategory');
                    }
                })
                .then((data) => {
                    // Update the state with the new subcategory (Add it to the list)
                    setPrevSubCategories((prev) => [
                        ...prev,
                        newSubCategory // Assuming the API returns the new subcategory data
                    ]);
                    // Clear input fields after adding the subcategory
                    setNewSubCategoryName('');
                    setNewSubCategoryDescription('');
                })
                .catch((error) => {
                    console.error("Error adding subcategory:", error);
                });
        } else {
            console.error("Both name and description are required");
        }
    };


    const handleUpdateSubCategory = (index) => {
        const updatedSubCategories = [...prevSubCategories];
        const updatedSubCategory = updatedSubCategories[index];

        const categoryPkList = id;  // Assuming category pk list needs to be passed
        const subCategoryName = updatedSubCategory.sub_category_name;
        const description = updatedSubCategory.description;

        // Check if all fields are present
        if (!subCategoryName || !description) {
            alert("All fields are required: Product Categories, Sub Category Name, Description.");
            return;
        }

        // API call to update the subcategory
        fetch(`${API_BASE_URL}/sub-categories/update/${updatedSubCategory.id}/`, {
            method: 'PUT',
            body: JSON.stringify({
                category_pk_list: categoryPkList,
                sub_category_name: subCategoryName,
                description: description
            }),
            headers: {
                Authorization: `Bearer ${Cookies.get("accessToken")}`,
                "Content-Type": "application/json",
            },
        })
            .then((response) => response.json())  // Parse response
            .then((data) => {
                if (data && data.message) {
                    alert("Sub-Category is Updated Successfully!");
                    setPrevSubCategories(updatedSubCategories);
                } else {
                    console.error("Error updating subcategory:", data);
                    alert(`Error: ${data.error || 'Something went wrong'}`);
                }
            })
            .catch((error) => {
                console.error("Error updating subcategory:", error);
                alert("Error updating subcategory: " + error.message);
            });
    };




    const handleDeleteSubCategory = (index) => {
        const subCategoryId = prevSubCategories[index].id;

        fetch(`${API_BASE_URL}/sub-categories/delete/${subCategoryId}/`, {
            method: 'DELETE',
            headers: {
                Authorization: `Bearer ${Cookies.get("accessToken")}`, // Ensure token is not undefined/null
                "Content-Type": "application/json"
            },
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`Failed to delete subcategory: ${response.statusText}`);
                }

                // If the response is empty, we can proceed without trying to parse JSON
                if (response.status === 204) {
                    // Status 204 (No Content) typically means the deletion was successful
                    const updatedSubCategories = prevSubCategories.filter((_, i) => i !== index);
                    setPrevSubCategories(updatedSubCategories);
                } else {
                    // If there's content, parse it as JSON (for status codes other than 204)
                    return response.json();
                }
            })
            .then(() => {
                // Optionally handle success or failure (e.g., display a success message)
            })
            .catch((error) => {
                console.error("Error deleting subcategory:", error);
                alert("Error deleting subcategory: " + error.message); // Optional: Display the error in an alert
            });
    };




    useEffect(() => {

        axios.get(`${API_BASE_URL}/categories/${id}/`, {
            headers: {
                Authorization: `Bearer ${Cookies.get("accessToken")}`, // Ensure token is not undefined/null
                "Content-Type": "application/json"
            }
        })
            .then(response => {
                console.log("Categories Response:", response.data); // Debug response
                setCategoryName(response.data.product_category.category_name);
                setCategoryDescription(response.data.product_category.description);
            })
            .catch(error => {
                console.error("Error fetching categories:", error.response ? error.response.data : error);
            });
    }, []);

    useEffect(() => {
        axios.get(`${API_BASE_URL}/sub-categories/fetch-all-product-sub-categories-for-a-category/${id}/`, {
            headers: {
                Authorization: `Bearer ${Cookies.get("accessToken")}`,
                "Content-Type": "application/json"
            }
        })
            .then(response => {
                console.log("Subcategories Response:", response.data); // Debug response
                setPrevSubCategories(Array.isArray(response.data.product_sub_category) ? response.data.product_sub_category : []);
            })
            .catch(error => {
                console.error("Error fetching subcategories:", error.response ? error.response.data : error);
            });
    }, []);


    const handleSubCategoryChange = (index, field, value) => {
        const updatedSubCategories = [...prevSubCategories];
        updatedSubCategories[index] = {
            ...updatedSubCategories[index],
            [field]: value,
        };
        setPrevSubCategories(updatedSubCategories);
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

        // Change the method to PUT or PATCH based on your backend
        axios.put(`${API_BASE_URL}/categories/update/${id}/`, {
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
                alert("Category Updated Successfully!");
                // Refresh the page after category creation
                window.location.reload(); // This will reload the page
            })
            .catch(error => {
                console.error("Error Updating category:", error);
            });
    };
    const handleDeleteCategory = () => {
        // API call to delete using categoryId
        fetch(`${API_BASE_URL}/categories/delete/${id}/`, {
            method: 'DELETE',
            headers: {
                Authorization: `Bearer ${Cookies.get("accessToken")}`,
                "Content-Type": "application/json",
            },
        })
            .then((response) => {
                if (!response.ok) {
                    // Handle error status (e.g., 400 or 500)
                    throw new Error('Error deleting category');
                }

                // Check if the response body is empty
                if (response.status === 204) {
                    alert("Category is Deleted Successfully!");
                    navigate('/products/category'); // Redirect
                }
                else {
                    return response.json(); // Proceed to parse JSON
                }
            })
            .then(() => {

            })
            .catch((error) => {
                console.error("Error deleting category:", error);
                alert("Error deleting category: " + error.message);
            });
    };





    return (
        <div className="col-xl-12 p-2">
            <div className="card invoice-container">
                <div className="card-header">
                    <h5>Category & Subcategory Update</h5>
                </div>
                <div className="card-body p-0">
                    <form onSubmit={handleSubmitCategory}>
                        <div className="px-4 row justify-content-between">
                            <div className="col-xl-6">
                                <div className="form-group mb-3 mt-3">
                                    <label htmlFor="Category" className="form-label">Category Name:</label>
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
                                        type="text"
                                        className="form-control mb-2"
                                        id="CategoryDescription"
                                        placeholder="Category Description"
                                        value={categoryDescription}
                                        onChange={(e) => setCategoryDescription(e.target.value)}
                                        required
                                    />
                                </div>
                                <div className='d-flex gap-2'>
                                    <button type="submit" className="btn btn-success">Update Category</button>
                                    <button
                                        type="button"
                                        className="btn btn-danger"
                                        onClick={handleDeleteCategory}  // Call the function here
                                    >
                                        Delete Category
                                    </button>
                                </div>
                            </div>
                        </div>
                    </form>


                    <hr className="border-dashed" />

                    <form onSubmit={(e) => e.preventDefault()}>
                        <div className="row px-4 py-4">

                            <div className="col-xl-6 mb-4">
                                <h6 className="fw-bold">Add New Sub Category:</h6>
                                <div className="d-flex gap-2">
                                    <input
                                        type="text"
                                        className="form-control"
                                        value={newSubCategoryName}
                                        onChange={(e) => setNewSubCategoryName(e.target.value)}
                                        placeholder="Sub Category Name"
                                        required
                                    />
                                    <textarea
                                        className="form-control"
                                        value={newSubCategoryDescription}
                                        onChange={(e) => setNewSubCategoryDescription(e.target.value)}
                                        placeholder="Description"
                                        required
                                    />
                                    <button type="button" className="btn btn-primary" onClick={handleAddSubCategory}>Add Sub-Category</button>
                                </div>
                            </div>
                            <div className="col-xl-6">
                                {prevSubCategories.length > 0 && (
                                    <>
                                        <h6 className="fw-bold">Sub Categories:</h6>
                                        <div className="border rounded p-2">
                                            {prevSubCategories.map((subCategory, index) => (
                                                <div key={subCategory.id} className="d-flex gap-2 mb-2">
                                                    <input
                                                        type="text"
                                                        className={`form-control ${subCategory.sub_category_name?.trim() === "" ? "border-danger" : ""}`}
                                                        value={subCategory.sub_category_name || ""}
                                                        onChange={(e) => handleSubCategoryChange(index, 'sub_category_name', e.target.value)}
                                                        placeholder="Name"
                                                        required
                                                    />
                                                    <textarea
                                                        className={`form-control ${subCategory.description?.trim() === "" ? "border-danger" : ""}`}
                                                        value={subCategory.description || ""}
                                                        onChange={(e) => handleSubCategoryChange(index, 'description', e.target.value)}
                                                        placeholder="Description"
                                                        required
                                                    />
                                                    <button type="button" className="btn btn-success" onClick={() => handleUpdateSubCategory(index)}>✓</button>
                                                    <button type="button" className="btn btn-danger" onClick={() => handleDeleteSubCategory(index)}>X</button>
                                                </div>
                                            ))}
                                        </div>
                                    </>
                                )}

                            </div>

                        </div>
                    </form>


                </div>
            </div>
        </div>
    );
}

export default ProductCategoryUpdate;
