import React, { useState, useEffect } from "react";
import axios from "axios";
import Cookies from "js-cookie";
import { Link, useParams, useNavigate } from "react-router-dom";
import ConfirmationModal from "../../ConfirmationModal";
import Select from "react-select";

const ProductSKUUpdate = () => {
    const { product_id, id } = useParams();

    const navigate = useNavigate();
    const [products, setProducts] = useState('');
    const [productPrice, setProductPrice] = useState('');
    const [productStock, setProductStock] = useState('');
    const [productFlavours, setProductFlavours] = useState([]);
    const [selectedProductFlavours, setSelectedProductFlavours] = useState([]);
    const [productColor, setProductColor] = useState("#000000");
    const [hexError, setHexError] = useState("");
    const [productSize, setProductSize] = useState('');

    const [message, setMessage] = useState("");
    const [messageType, setMessageType] = useState("");
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [deleteAction, setDeleteAction] = useState(null); // Store the delete action type


    const API_BASE_URL = "http://127.0.0.1:8000/server_api/product";

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
    });


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
        } catch (error) {
            console.error("Error fetching products:", error);
        }
    };


    // Fetch Categories & Brands on Mount
    useEffect(() => {
        const fetchData = async () => {
            try {
                const [flavoursRes] = await Promise.all([
                    axios.get(`${API_BASE_URL}/product-flavour/fetch-product-flavour/`, {
                        headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` }
                    })
                ]);

                const flavourOptions = flavoursRes.data.product_flavours_data.map(c => ({ value: c.id, label: c.product_flavour_name }));

                setProductFlavours(flavourOptions);

                fetchProductDetails(flavourOptions);
            } catch (error) {
                console.error("Error fetching initial data:", error);
            }
        };

        fetchData();
    }, []);

    // Fetch Product Details
    const fetchProductDetails = async (flavourOptions) => {
        try {
            const response = await axios.get(`${API_BASE_URL}/product-sku/fetch-product-sku/`, {
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` },
                params: { pk: id },
            });

            const product = response.data.product_sku_fetch;
            setProductColor(product.product_color);
            setProductPrice(product.product_price);
            setProductStock(product.product_stock);
            setProductSize(product.product_size);

            const selectedflav = flavourOptions.filter(c => product.product_flavours.includes(c.value));

            setSelectedProductFlavours(selectedflav);

        } catch (error) {
            console.error("Error fetching product details:", error);
            navigate("/404");
        }
    };


    // Handle Product Update
    const handleUpdateProduct = async (e) => {
        e.preventDefault();

        if (selectedProductFlavours.length === 0) {
            setMessage("At least one flavour is required.");
            setMessageType("danger");
            return;
        }

        try {
            await axios.put(`${API_BASE_URL}/product-sku/update/${id}/`, {
                product_id: product_id,
                product_price: productPrice,
                product_stock: productStock,
                product_flavours_pk_list: selectedProductFlavours.map(c => c.value),
                product_color: productColor,
                product_size: productSize,
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
                .delete(`${API_BASE_URL}/product-sku/delete/${id}/`, {
                    headers: {
                        Authorization: `Bearer ${Cookies.get("accessToken")}`,
                    },
                })
                .then(() => {
                    setMessage("Product deleted successfully!");
                    setMessageType("success");
                    navigate(`/products/sku/${product_id}/`);
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
                    <Link to={`/products/sku/${product_id}/`} className="btn btn-primary">← Back</Link>
                </div>
                <div className="card-body p-0">
                    <form onSubmit={handleUpdateProduct}>
                        <div className="px-4 py-4 row justify-content-between">
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

export default ProductSKUUpdate;