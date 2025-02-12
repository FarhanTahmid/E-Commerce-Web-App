import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import Select from "react-select";
import { Link } from 'react-router-dom';

const ProductSKUCreate = () => {
    // product_pk = self.request.data.get('product_pk',"")
    // product_price = self.request.data.get('product_price',"")
    // product_stock = self.request.data.get('product_stock',"")
    // product_flavours_pk_list = self.request.data.get('product_flavours_pk_list',[])

    // #can none
    // product_color = self.request.data.get('product_color',"")
    // product_size = self.request.data.get('product_size',"")

    const [products, setProducts] = useState([]);
    const [selectedProduct, setSelectedProduct] = useState('');
    const [productPrice, setProductPrice] = useState('');
    const [productStock, setProductStock] = useState('');
    const [productFlavours, setProductFlavours] = useState([]);
    const [selectedProductFlavours, setSelectedProductFlavours] = useState([]);
    const [productColor, setProductColor] = useState('');
    const [productSize, setProductSize] = useState('');


    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState('');

    const API_BASE_URL = 'http://127.0.0.1:8000/server_api/product';

    useEffect(() => {
        fetchProducts();
        fetchProductFlavours();
    }, []);

    const fetchProducts = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/fetch-product/`, {
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` }
            });
            setProducts(response.data.product_data.map(c => ({ value: c.id, label: c.product_name })));
        } catch (error) {
            console.error("Error fetching categories:", error);
        }
    };
    const fetchProductFlavours = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/product-flavour/fetch-product-flavour/`, {
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}` }
            });
            setProductFlavours(response.data.product_flavours_data.map(c => ({ value: c.id, label: c.product_flavour_name })));
        } catch (error) {
            console.error("Error fetching categories:", error);
        }
    };



    const handleSubmit = async (e) => {
        e.preventDefault();
        if (selectedProduct.length === 0) {
            setMessage("Product is required.");
            setMessageType("danger");
            return;
        }
        if (selectedProductFlavours.length === 0) {
            setMessage("At least one flavour is required.");
            setMessageType("danger");
            return;
        }

        try {
            const response = await axios.post(`${API_BASE_URL}/create/`, {
                product_pk: selectedProduct,
                product_price: productPrice,
                product_stock: productStock,
                product_flavours_pk_list: selectedProductFlavours.map(c => c.value),
                product_color: "test",
                product_size: productSize,
            }, {
                headers: { Authorization: `Bearer ${Cookies.get("accessToken")}`, "Content-Type": "application/json" }
            });

            setMessage(response.data.message);
            setMessageType('success');

            // Reset form fields
            setSelectedProduct('');
            setProductPrice('');
            setProductStock('');
            setSelectedProductFlavours([]);
            setProductColor('');
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
                    <Link to="/products" className="btn btn-primary">← Back</Link>
                </div>
                <div className="card-body">
                    <form onSubmit={handleSubmit}>
                        <div className="row justify-content-between">
                            <div className="col-xl-6">
                                <div className="form-group">
                                    <div className="mb-3">
                                        <label className="form-label">Product</label>
                                        <Select options={products} value={selectedProduct} onChange={setSelectedProduct} />
                                        {!selectedProduct && <small className="text-danger">Product is required.</small>}
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
                                        {selectedProductFlavours.length === 0 && <small className="text-danger">At least one flavours is required.</small>}
                                    </div>
                                    <div className="mb-3">
                                        <label className="form-label">Product Size</label>
                                        <input type="number" className="form-control" value={productSize} onChange={(e) => setProductSize(e.target.value)} required />
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
