import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import Select from "react-select";
import { Link } from 'react-router-dom';
import ReactQuill from 'react-quill'; // Import ReactQuill
import 'react-quill/dist/react-quill'; // Import Quill CSS
import QuillToolbar, { modules, formats } from '@/components/QuillToolbar';

const ProductCreate = () => {
    const [productName, setProductName] = useState('');
    const [productDescription, setProductDescription] = useState('');
    const [productSummary, setProductSummary] = useState('');
    const [productIngredients, setProductIngredients] = useState('');
    const [productUsageDirection, setProductUsageDirection] = useState('');
    const [categories, setCategories] = useState([]);
    const [selectedCategories, setSelectedCategories] = useState([]);
    const [subCategories, setSubCategories] = useState([]);
    const [selectedSubCategories, setSelectedSubCategories] = useState([]);
    const [brands, setBrands] = useState([]);
    const [selectedBrand, setSelectedBrand] = useState(null);
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState('');

    const API_BASE_URL = 'http://127.0.0.1:8000/server_api/product';

    useEffect(() => {
        fetchCategories();
        fetchBrands();
    }, []);

    const fetchCategories = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/categories/fetch-all/`, {
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` }
            });
            setCategories(response.data.product_category.map(c => ({ value: c.id, label: c.category_name })));
        } catch (error) {
            console.error("Error fetching categories:", error);
        }
    };

    const fetchSubCategories = async (categoryId) => {
        try {
            const response = await axios.get(`${API_BASE_URL}/sub-categories/fetch-all-product-sub-categories-for-a-category/${categoryId}/`, {
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` }
            });
            setSubCategories(response.data.product_sub_category.map(sc => ({ value: sc.id, label: sc.sub_category_name })));
        } catch (error) {
            console.error("Error fetching subcategories:", error);
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

    // useEffect(() => {
    //     if (selectedCategories.length > 0) {
    //         fetchSubCategories(selectedCategories.map(c => c.value));
    //     } else {
    //         setSubCategories([]);
    //     }
    // }, [selectedCategories]);

    const fetchBrands = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/product-brand/fetch-product-brands/`, {
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` }
            });
            setBrands(response.data.product_brands.map(b => ({ value: b.id, label: b.brand_name })));
        } catch (error) {
            console.error("Error fetching brands:", error);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!productName.trim()) {
            setMessage("Product name is required.");
            setMessageType("danger");
            return;
        }
        if (!productDescription.trim()) {
            setMessage("Product description is required.");
            setMessageType("danger");
            return;
        }
        if (!productSummary.trim()) {
            setMessage("Product summary is required.");
            setMessageType("danger");
            return;
        }
        if (selectedCategories.length === 0) {
            setMessage("At least one category is required.");
            setMessageType("danger");
            return;
        }
        if (selectedSubCategories.length === 0) {
            setMessage("At least one subcategory is required.");
            setMessageType("danger");
            return;
        }
        if (!selectedBrand) {
            setMessage("Brand is required.");
            setMessageType("danger");
            return;
        }
        console.log(selectedBrand);
        try {
            const response = await axios.post(`${API_BASE_URL}/create/`, {
                product_name: productName,
                product_category_pk_list: selectedCategories.map(c => c.value),
                product_sub_category_pk_list: selectedSubCategories.map(sc => sc.value),
                product_description: productDescription,
                product_summary: productSummary,
                product_brand_pk: selectedBrand.value,
                product_ingredients: productIngredients,
                product_usage_direction: productUsageDirection,
            }, {
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}`, "Content-Type": "application/json" }
            });

            setMessage(response.data.message);
            setMessageType('success');

            // Reset form fields
            setProductName('');
            setSelectedCategories([]);
            setSelectedSubCategories([]);
            setProductDescription('');
            setProductSummary('');
            setSelectedBrand(null);
            setProductIngredients('');
            setProductUsageDirection('');
        } catch (error) {
            setMessage(error.response ? error.response.data.error : error.message);
            setMessageType('danger');
        }
    };


    return (
        <div className="col-xl-12 p-2">
            {message && (
                <div className={`alert alert-${messageType} alert-dismissible fade show`} role="alert">
                    <strong>{messageType === 'danger' ? 'Error: ' : 'Success: '}</strong> {message}
                    <button type="button" className="btn-close" data-bs-dismiss="alert" aria-label="Close" onClick={() => setMessage('')}></button>
                </div>
            )}
            <div className="card">
                <div className="card-header">
                    <h5>Create Product</h5>
                    <Link to="/products" className="btn btn-primary">← Back</Link>
                </div>
                <div className="card-body">
                    <form onSubmit={handleSubmit}>
                        <div className="row justify-content-between">
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

                                    <button type="submit" className="btn btn-success">Create Product</button>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default ProductCreate;
