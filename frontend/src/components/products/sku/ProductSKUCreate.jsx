import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import Select from "react-select";
import { Link, useNavigate, useParams } from 'react-router-dom';


const ProductSKUCreate = () => {
    const navigate = useNavigate();
    const { product_id } = useParams();
    const [products, setProducts] = useState('');
    const [productPrice, setProductPrice] = useState('');
    const [productStock, setProductStock] = useState('');
    const [productFlavours, setProductFlavours] = useState([]);
    const [selectedProductFlavours, setSelectedProductFlavours] = useState([]);
    const [productColor, setProductColor] = useState("#000000");
    const [hexError, setHexError] = useState("");
    const [productSize, setProductSize] = useState('');
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState('');

    const API_BASE_URL = 'http://127.0.0.1:8000/server_api/product';


    // Function to validate hex code
    const handleHexChange = (e) => {
        const hex = e.target.value.toUpperCase();
        setProductColor(hex);

        // Validate hex format
        if (/^#([0-9A-F]{3}){1,2}$/i.test(hex)) {
            setHexError(""); // Clear error if valid
        } else {
            setHexError("Invalid hex code");
        }
    };


    useEffect(() => {
        fetchProducts();
        fetchProductFlavours();
    }, []);

    const fetchProducts = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/fetch-product/`, {
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` }
            });

            const productList = response.data.product_data.map(c => ({ value: c.id, label: c.product_name }));

            // Find the product name based on product_id
            const selectedProduct = productList.find(product => product.value === parseInt(product_id));

            if (selectedProduct) {
                setProducts(selectedProduct.label);
            }
            else {
                navigate("/404");
            }


            // setProducts(filteredProducts);
            // console.log(filteredProducts);
        } catch (error) {
            console.error("Error fetching products:", error);
        }
    };

    const fetchProductFlavours = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/product-flavour/fetch-product-flavour/`, {
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` }
            });
            setProductFlavours(response.data.product_flavours_data.map(c => ({ value: c.id, label: c.product_flavour_name })));
        } catch (error) {
            console.error("Error fetching product flavours:", error);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (selectedProductFlavours.length === 0) {
            setMessage("At least one flavour is required.");
            setMessageType("danger");
            return;
        }

        try {
            const response = await axios.post(`${API_BASE_URL}/product-sku/create/`, {
                product_pk: product_id,
                product_price: productPrice,
                product_stock: productStock,
                product_flavours_pk_list: selectedProductFlavours.map(c => c.value),
                product_color: productColor,
                product_size: productSize,
            }, {
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}`, "Content-Type": "application/json" }
            });

            setMessage(response.data.message);
            setMessageType('success');

            // Reset form fields
            setProductPrice('');
            setProductStock('');
            setSelectedProductFlavours([]);
            setProductColor("#000000");
            setProductSize('');
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
                    <h5>Create Product SKU</h5>
                    <Link to={`/products/sku/${product_id}`} className="btn btn-primary">← Back</Link>
                </div>
                <div className="card-body">
                    <form onSubmit={handleSubmit}>
                        <div className="row justify-content-between">
                            <div className="col-xl-6">
                                <div className="form-group">
                                    <div className="mb-3">
                                        <h3 className="">Product Name: {products}</h3>
                                    </div>
                                    <div className="mb-3">
                                        <label className="form-label">Product Price</label>
                                        <input type="number" className="form-control" value={productPrice} onChange={(e) => setProductPrice(e.target.value)} required />
                                    </div>
                                    <div className="mb-3">
                                        <label className="form-label">Product Stock</label>
                                        <input type="number" className="form-control" value={productStock} onChange={(e) => setProductStock(e.target.value)} required />
                                    </div>
                                    <div className="mb-3">
                                        <label className="form-label">Product Flavours</label>
                                        <Select isMulti options={productFlavours} value={selectedProductFlavours} onChange={setSelectedProductFlavours} />
                                    </div>
                                    <div className="mb-3">
                                        <label className="form-label">Product Color</label>
                                        <div className="d-flex align-items-center">
                                            {/* Color Picker */}
                                            <input
                                                type="color"
                                                className="form-control form-control-color me-2"
                                                style={{ width: "100px" }}
                                                value={productColor}
                                                onChange={(e) => setProductColor(e.target.value)}
                                            />

                                            {/* Hex Code Input */}
                                            <input
                                                type="text"
                                                className="form-control"
                                                style={{ width: "120px", textTransform: "uppercase" }}
                                                value={productColor}
                                                onChange={handleHexChange}
                                            />
                                        </div>
                                        {hexError && <small className="text-danger">{hexError}</small>}

                                    </div>

                                    <div className="mb-3">
                                        <label className="form-label">Product Size</label>
                                        <input type="text" className="form-control" value={productSize} onChange={(e) => setProductSize(e.target.value)} required />
                                    </div>
                                    <button type="submit" className="btn btn-success">Create Product SKU</button>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default ProductSKUCreate;