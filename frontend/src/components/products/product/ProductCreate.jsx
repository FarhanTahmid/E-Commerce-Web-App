import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import Select from "react-select";
import { Link } from 'react-router-dom';
import ReactQuill from 'react-quill'; // Import ReactQuill
import 'react-quill/dist/react-quill'; // Import Quill CSS

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

    const API_BASE_URL = 'http://127.0.0.1:8000/product';

    useEffect(() => {
        fetchCategories();
        fetchBrands();
    }, []);

    const fetchCategories = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/categories/fetch-all/`, {
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` }
            });
            setCategories(response.data.product_category.map(c => ({ value: c.pk, label: c.name })));
        } catch (error) {
            console.error("Error fetching categories:", error);
        }
    };

    const fetchSubCategories = async (categoryId) => {
        try {
            const response = await axios.get(`${API_BASE_URL}/sub-categories/fetch-all-product-sub-categories-for-a-category/${categoryId}/`, {
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` }
            });
            setSubCategories(response.data.product_sub_category.map(sc => ({ value: sc.pk, label: sc.name })));
        } catch (error) {
            console.error("Error fetching subcategories:", error);
        }
    };

    useEffect(() => {
        if (selectedCategories.length > 0) {
            fetchSubCategories(selectedCategories.map(c => c.value));
        } else {
            setSubCategories([]);
        }
    }, [selectedCategories]);

    const fetchBrands = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/product-brand/fetch-product-brands/`, {
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` }
            });
            setBrands(response.data.product_brands.map(b => ({ value: b.pk, label: b.name })));
        } catch (error) {
            console.error("Error fetching brands:", error);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post(`${API_BASE_URL}/create/`, {
                product_name: productName,
                product_category_pk_list: selectedCategories.map(c => c.value),
                product_sub_category_pk_list: selectedSubCategories.map(sc => sc.value),
                product_description: productDescription,
                product_summary: productSummary,
                product_brand_pk: selectedBrand ? selectedBrand.value : null,
                product_ingredients: productIngredients,
                product_usage_direction: productUsageDirection,
            }, {
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}`, "Content-Type": "application/json" }
            });

            setMessage(response.data.message);
            setMessageType('success');
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

                                    <div className="mb-3">
                                        <label className="form-label">Product Description</label>
                                        <ReactQuill value={productDescription} onChange={setProductDescription} />
                                    </div>

                                    <div className="mb-3">
                                        <label className="form-label">Product Summary</label>
                                        <textarea className="form-control" value={productSummary} onChange={(e) => setProductSummary(e.target.value)} required />
                                    </div>

                                    <div className="mb-3">
                                        <label className="form-label">Categories</label>
                                        <Select isMulti options={categories} value={selectedCategories} onChange={setSelectedCategories} />
                                    </div>

                                    <div className="mb-3">
                                        <label className="form-label">Subcategories</label>
                                        <Select isMulti options={subCategories} value={selectedSubCategories} onChange={setSelectedSubCategories} />
                                    </div>

                                    <div className="mb-3">
                                        <label className="form-label">Brand</label>
                                        <Select options={brands} value={selectedBrand} onChange={setSelectedBrand} isClearable />
                                    </div>

                                    <div className="mb-3">
                                        <label className="form-label">Ingredients</label>
                                        <ReactQuill value={productIngredients} onChange={setProductIngredients} />
                                    </div>

                                    <div className="mb-3">
                                        <label className="form-label">Usage Direction</label>
                                        <ReactQuill value={productUsageDirection} onChange={setProductUsageDirection} />
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
