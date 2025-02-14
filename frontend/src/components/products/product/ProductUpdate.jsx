import React, { useState, useEffect } from "react";
import axios from "axios";
import Cookies from "js-cookie";
import { Link, useParams, useNavigate } from "react-router-dom";
import ConfirmationModal from "../../ConfirmationModal";
import Select from "react-select";
import ReactQuill from "react-quill";
import 'react-quill/dist/react-quill'; // Import Quill CSS
import QuillToolbar, { modules, formats } from '@/components/QuillToolbar';

const ProductUpdate = () => {
    const { id } = useParams();
    const navigate = useNavigate();

    const [productName, setProductName] = useState("");
    const [productDescription, setProductDescription] = useState("");
    const [productSummary, setProductSummary] = useState("");
    const [productIngredients, setProductIngredients] = useState("");
    const [productUsageDirection, setProductUsageDirection] = useState("");

    const [categories, setCategories] = useState([]);
    const [subCategories, setSubCategories] = useState([]);
    const [brands, setBrands] = useState([]);

    const [selectedCategories, setSelectedCategories] = useState([]);
    const [selectedSubCategories, setSelectedSubCategories] = useState([]);
    const [selectedBrand, setSelectedBrand] = useState(null);

    const [message, setMessage] = useState("");
    const [messageType, setMessageType] = useState("");
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [deleteAction, setDeleteAction] = useState(null); // Store the delete action type


    const API_BASE_URL = "http://127.0.0.1:8000/server_api/product";

    // Fetch Categories & Brands on Mount
    useEffect(() => {
        const fetchData = async () => {
            try {
                const [categoriesRes, brandsRes] = await Promise.all([
                    axios.get(`${API_BASE_URL}/categories/fetch-all/`, {
                        headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` }
                    }),
                    axios.get(`${API_BASE_URL}/product-brand/fetch-product-brands/`, {
                        headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` }
                    })
                ]);

                const categoryOptions = categoriesRes.data.product_category.map(c => ({ value: c.id, label: c.category_name }));
                const brandOptions = brandsRes.data.product_brands.map(b => ({ value: b.id, label: b.brand_name }));

                setCategories(categoryOptions);
                setBrands(brandOptions);

                fetchProductDetails(categoryOptions, brandOptions);
            } catch (error) {
                console.error("Error fetching initial data:", error);
            }
        };

        fetchData();
    }, []);

    // Fetch Product Details
    const fetchProductDetails = async (categoryOptions, brandOptions) => {
        try {
            const response = await axios.get(`${API_BASE_URL}/fetch-product/`, {
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` },
                params: { product_pk: id },
            });

            const product = response.data.product_data;
            setProductName(product.product_name);
            setProductDescription(product.product_description);
            setProductSummary(product.product_summary);
            setProductIngredients(product.product_ingredients);
            setProductUsageDirection(product.product_usage_direction);

            const selectedCat = categoryOptions.filter(c => product.product_category.includes(c.value));
            const selectedBrand = brandOptions.find(b => b.value === product.product_brand) || null;

            setSelectedCategories(selectedCat);
            setSelectedBrand(selectedBrand);

            fetchSubcategoriesForCategories(selectedCat, product.product_sub_category);
        } catch (error) {
            console.error("Error fetching product details:", error);
        }
    };

    // Fetch subcategories dynamically based on selected categories
    const fetchSubcategoriesForCategories = async (selectedCategories, existingSubCategoryIds = []) => {
        try {
            const subCategoryRequests = selectedCategories.map(cat =>
                axios.get(`${API_BASE_URL}/sub-categories/fetch-all-product-sub-categories-for-a-category/${cat.value}/`, {
                    headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` }
                })
            );

            const responses = await Promise.all(subCategoryRequests);

            const newSubCategories = responses.flatMap(res => res.data.product_sub_category)
                .map(sc => ({ value: sc.id, label: sc.sub_category_name, categoryId: sc.category_id }));

            setSubCategories(newSubCategories);

            // Set only existing subcategories that belong to selected categories
            setSelectedSubCategories(newSubCategories.filter(sc => existingSubCategoryIds.includes(sc.value)));
        } catch (error) {
            console.error("Error fetching subcategories:", error);
        }
    };

    // Handle Category Selection
    const handleCategoryChange = async (selectedOptions) => {
        setSelectedCategories(selectedOptions);
        fetchSubcategoriesForCategories(selectedOptions);
    };

    // Handle Product Update
    const handleUpdateProduct = async (e) => {
        e.preventDefault();

        if (!productName.trim() || !selectedCategories.length || !selectedSubCategories.length || !selectedBrand) {
            alert("All required fields must be filled!");
            return;
        }

        try {
            await axios.put(`${API_BASE_URL}/update/${id}/`, {
                product_name: productName,
                product_category_pk_list: selectedCategories.map(c => c.value),
                product_sub_category_pk_list: selectedSubCategories.map(sc => sc.value),
                product_description: productDescription,
                product_summary: productSummary,
                product_brand_pk: selectedBrand.value,
                product_ingredients: productIngredients,
                product_usage_direction: productUsageDirection,
            }, {
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                    "Content-Type": "application/json"
                },
            });
            setMessage("Product Updated Successfully!");
            setMessageType("success");
        } catch (error) {
            console.error("Error updating product:", error);
            setMessage("Failed to update the product.");
            setMessageType("danger");
        }
    };


    /** Handle product deletion */
    const handleDeleteProduct = () => {
        setDeleteAction({ type: "product" });
        setShowDeleteModal(true);
    };

    const confirmDelete = () => {
        if (deleteAction?.type === "product") {
            axios
                .delete(`${API_BASE_URL}/delete/${id}/`, {
                    headers: {
                        Authorization: `Bearer ${Cookies.get("accessToken")}`,
                    },
                })
                .then(() => {
                    setMessage("Product deleted successfully!");
                    setMessageType("success");
                    navigate("/products");
                })
                .catch((error) => {
                    setMessage("Failed to delete product.");
                    setMessageType("danger");
                    console.error("Delete error:", error.response?.data || error.message);
                });
        }
        setShowDeleteModal(false);
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
                    <h5>Product Update & Deletion</h5>
                    <div className="d-flex gap-2">
                        <Link to={`/products/image/${id}`} className="btn btn-primary">Add Product Images</Link>
                        <Link to="/products" className="btn btn-primary">← Back</Link>
                    </div>
                </div>
                <div className="card-body p-0">
                    <form onSubmit={handleUpdateProduct}>
                        <div className="px-4 py-4 row justify-content-between">
                            <div className="col-xl-6">
                                <div className="form-group">
                                    <div className="mb-3">
                                        <label className="form-label">Product Name</label>
                                        <input type="text" className="form-control" value={productName} onChange={(e) => setProductName(e.target.value)} required />
                                    </div>

                                    <div className="mb-3 editor">
                                        <label className="form-label">Product Description</label>
                                        <QuillToolbar toolbarId={'t1'} />
                                        <ReactQuill
                                            theme="snow"
                                            value={productDescription}
                                            onChange={setProductDescription}
                                            modules={modules('t1')}
                                            formats={formats}
                                        />
                                        <hr />
                                        {!productDescription.trim() && <small className="text-danger">Product description is required.</small>}

                                    </div>

                                    <div className="mb-3">
                                        <label className="form-label">Product Summary</label>
                                        <textarea className="form-control" value={productSummary} onChange={(e) => setProductSummary(e.target.value)} required />
                                        {!productSummary.trim() && <small className="text-danger">Product summary is required.</small>}
                                    </div>

                                    <div className="mb-3">
                                        <label className="form-label">Categories</label>
                                        <Select isMulti options={categories} value={selectedCategories} onChange={handleCategoryChange} />
                                        {selectedCategories.length === 0 && <small className="text-danger">At least one category is required.</small>}

                                    </div>

                                    <div className="mb-3">
                                        <label className="form-label">Subcategories</label>
                                        <Select isMulti options={subCategories} value={selectedSubCategories} onChange={setSelectedSubCategories} />
                                        {selectedSubCategories.length === 0 && <small className="text-danger">At least one subcategory is required.</small>}

                                    </div>

                                    <div className="mb-3">
                                        <label className="form-label">Brand</label>
                                        <Select options={brands} value={selectedBrand} onChange={setSelectedBrand} isClearable />
                                        {!selectedBrand && <small className="text-danger">Brand is required.</small>}

                                    </div>

                                    <div className="mb-3 editor">
                                        <label className="form-label">Ingredients</label>
                                        <QuillToolbar toolbarId={'t2'} />
                                        <ReactQuill
                                            theme="snow"
                                            value={productIngredients}
                                            onChange={setProductIngredients}
                                            modules={modules('t2')}
                                            formats={formats}
                                        />
                                        <hr />
                                    </div>

                                    <div className="mb-3 editor">
                                        <label className="form-label">Usage Direction</label>
                                        <QuillToolbar toolbarId={'t3'} />
                                        <ReactQuill
                                            theme="snow"
                                            value={productUsageDirection}
                                            onChange={setProductUsageDirection}
                                            modules={modules('t3')}
                                            formats={formats}
                                        />
                                        <hr />
                                    </div>
                                    <div className='d-flex gap-2'>
                                        <button type="submit" className="btn btn-success">Update Product</button>
                                        <button type="button" className="btn btn-danger" onClick={handleDeleteProduct}>Delete Product</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                    <ConfirmationModal show={showDeleteModal} onClose={() => setShowDeleteModal(false)} onConfirm={confirmDelete} message="Are you sure you want to delete this product?" />

                </div>
            </div>
        </div>
    );
};

export default ProductUpdate;