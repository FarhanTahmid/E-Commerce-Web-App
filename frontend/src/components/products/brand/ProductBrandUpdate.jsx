import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import ConfirmationModal from '../../ConfirmationModal'; // Import the modal component




const ProductBrandUpdate = () => {
    const { id } = useParams();
    const [categoryName, setCategoryName] = useState('');
    const [categoryDescription, setCategoryDescription] = useState("");
    const [subCategories, setSubCategories] = useState([{ name: '', description: '' }]); // Add description field
    const [prevSubCategories, setPrevSubCategories] = useState([]);
    const API_BASE_URL = 'http://127.0.0.1:8000/server_api/product';
    const [newSubCategoryName, setNewSubCategoryName] = useState('');
    const [newSubCategoryDescription, setNewSubCategoryDescription] = useState('');
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState(''); // 'success' or 'danger'

    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [deleteAction, setDeleteAction] = useState(null);  // To track what is being deleted (category or subcategory)


    // Inside your component:
    const navigate = useNavigate();


    const handleDeleteSubCategory = (index) => {
        setDeleteAction({ type: 'subcategory', index });
        setShowDeleteModal(true);
    };

    const handleDeleteCategory = () => {
        setDeleteAction({ type: 'category' });
        setShowDeleteModal(true);
    };

    const confirmDelete = () => {
        if (deleteAction.type === 'subcategory') {
            const subCategoryId = prevSubCategories[deleteAction.index].id;

            fetch(`${API_BASE_URL}/sub-categories/delete/${subCategoryId}/`, {
                method: 'DELETE',
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                    "Content-Type": "application/json"
                },
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to delete subcategory');
                    }
                    setPrevSubCategories(prevSubCategories.filter((_, i) => i !== deleteAction.index));
                    setMessage('Subcategory deleted successfully!');
                    setMessageType('success');
                })
                .catch(error => {
                    setMessage(error.message);
                    setMessageType('danger');
                });
        } else if (deleteAction.type === 'category') {
            fetch(`${API_BASE_URL}/categories/delete/${id}/`, {
                method: 'DELETE',
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                    "Content-Type": "application/json"
                },
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to delete category');
                    }
                    setMessage('Category deleted successfully!');
                    setMessageType('success');

                    // Redirect to the category list page after deletion
                    navigate('/products/category');
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





    const handleAddSubCategory = () => {
        if (newSubCategoryName.trim() && newSubCategoryDescription.trim()) {
            const newSubCategory = {
                sub_category_name: newSubCategoryName,
                description: newSubCategoryDescription
            };

            fetch(`${API_BASE_URL}/sub-categories/create/${id}/`, {
                method: 'POST',
                body: JSON.stringify(newSubCategory),
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                    "Content-Type": "application/json"
                }
            })
                .then((response) => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error('Failed to add subcategory');
                    }
                })
                .then(() => {
                    setPrevSubCategories((prev) => [
                        ...prev,
                        newSubCategory
                    ]);
                    setNewSubCategoryName('');
                    setNewSubCategoryDescription('');
                    setMessage('Subcategory added successfully!');
                    setMessageType('success');
                })
                .catch((error) => {
                    setMessage(error.message);
                    setMessageType('danger');
                });
        } else {
            setMessage("Both name and description are required");
            setMessageType('danger');
        }
    };



    const handleUpdateSubCategory = (index) => {
        const updatedSubCategories = [...prevSubCategories];
        const updatedSubCategory = updatedSubCategories[index];
        const categoryPkList = id;
        const subCategoryName = updatedSubCategory.sub_category_name;
        const description = updatedSubCategory.description;

        if (!subCategoryName || !description) {
            setMessage("All fields are required: Product Categories, Sub Category Name, Description.");
            setMessageType('danger');
            return;
        }

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
            .then((response) => response.json())
            .then((data) => {
                if (data && data.message) {
                    setMessage("Sub-Category is Updated Successfully!");
                    setMessageType('success');
                    setPrevSubCategories(updatedSubCategories);
                } else {
                    setMessage(`Error: ${data.error || 'Something went wrong'}`);
                    setMessageType('danger');
                }
            })
            .catch((error) => {
                setMessage("Error updating subcategory: " + error.message);
                setMessageType('danger');
            });
    };




    // const handleDeleteSubCategory = (index) => {
    //     const subCategoryId = prevSubCategories[index].id;

    //     fetch(`${API_BASE_URL}/sub-categories/delete/${subCategoryId}/`, {
    //         method: 'DELETE',
    //         headers: {
    //             Authorization: `Bearer ${Cookies.get("accessToken")}`,
    //             "Content-Type": "application/json"
    //         },
    //     })
    //         .then((response) => {
    //             if (!response.ok) {
    //                 throw new Error(`Failed to delete subcategory: ${response.statusText}`);
    //             }

    //             if (response.status === 204) {
    //                 const updatedSubCategories = prevSubCategories.filter((_, i) => i !== index);
    //                 setPrevSubCategories(updatedSubCategories);
    //                 setMessage('Subcategory deleted successfully!');
    //                 setMessageType('success');
    //             } else {
    //                 return response.json();
    //             }
    //         })
    //         .catch((error) => {
    //             setMessage("Error deleting subcategory: " + error.message);
    //             setMessageType('danger');
    //         });
    // };




    useEffect(() => {

        axios.get(`${API_BASE_URL}/categories/${id}/`, {
            headers: {
                Authorization: `Bearer ${Cookies.get("accessToken")}`, // Ensure token is not undefined/null
                "Content-Type": "application/json"
            }
        })
            .then(response => {
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
            description: categoryDescription
        }, {
            headers: {
                Authorization: `Bearer ${Cookies.get('accessToken')}`,
                "Content-Type": "application/json"
            }
        })
            .then(response => {
                setCategoryName(response.data.category_name);
                setCategoryDescription(response.data.description);
                setMessage("Category Updated Successfully!");
                setMessageType('success');
            })
            .catch(error => {
                console.error("Error Updating category:", error.response ? error.response.data : error.message);
            });

    };
    // const handleDeleteCategory = () => {
    //     fetch(`${API_BASE_URL}/categories/delete/${id}/`, {
    //         method: 'DELETE',
    //         headers: {
    //             Authorization: `Bearer ${Cookies.get("accessToken")}`,
    //             "Content-Type": "application/json",
    //         },
    //     })
    //         .then((response) => {
    //             if (!response.ok) {
    //                 throw new Error('Error deleting category');
    //             }

    //             if (response.status === 204) {
    //                 setMessage("Category is Deleted Successfully!");
    //                 setMessageType('success');
    //                 navigate('/products/category');
    //             } else {
    //                 return response.json();
    //             }
    //         })
    //         .catch((error) => {
    //             setMessage("Error deleting category: " + error.message);
    //             setMessageType('danger');
    //         });
    // };





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

                    <ConfirmationModal
                        show={showDeleteModal}
                        onClose={cancelDelete}
                        onConfirm={confirmDelete}
                        message={`Are you sure you want to delete this ${deleteAction?.type === 'subcategory' ? 'subcategory' : 'category'}?`}
                    />
                </div>
            </div>
        </div>
    );
}

export default ProductBrandUpdate;
