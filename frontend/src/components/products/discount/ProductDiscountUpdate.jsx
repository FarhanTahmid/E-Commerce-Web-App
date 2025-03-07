import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { Link, useParams } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import ConfirmationModal from '../../ConfirmationModal';

const ProductDiscountUpdate = () => {
    const { id } = useParams();
    const navigate = useNavigate();

    // Discount details
    const [discountName, setDiscountName] = useState("");
    const [discountAmount, setDiscountAmount] = useState("");
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");

    // Target selection
    const [selectedType, setSelectedType] = useState(""); // "product", "brand", "category", "sub_category"
    const [selectedId, setSelectedId] = useState(""); // ID of selected type

    // Data lists
    const [categories, setCategories] = useState([]);
    const [subCategories, setSubCategories] = useState([]);
    const [brands, setBrands] = useState([]);
    const [products, setProducts] = useState([]);
    const [options, setOptions] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState("");

    // Discount target IDs from the original discount
    const [productDiscountProductIdPk, setProductDiscountProductIdPk] = useState("");
    const [productDiscountBrandIdPk, setProductDiscountBrandIdPk] = useState("");
    const [productDiscountCategoryIdPk, setProductDiscountCategoryIdPk] = useState("");
    const [productDiscountSubCategoryIdPk, setProductDiscountSubCategoryIdPk] = useState("");

    // UI state
    const [message, setMessage] = useState("");
    const [messageType, setMessageType] = useState("");
    const [showDeleteModal, setShowDeleteModal] = useState(false);

    const API_BASE_URL = "http://127.0.0.1:8000/server_api/product";

    // Fetch the discount details on component mount
    useEffect(() => {
        axios.get(`${API_BASE_URL}/product-discounts/fetch-product-discount/?product_discount_pk=${id}`, {
            headers: {
                Authorization: `Bearer ${Cookies.get("accessToken")}`,
                "Content-Type": "application/json"
            }
        })
            .then(response => {
                const discountData = response.data.product_discount;

                console.log("Discount data:", discountData);

                // Set discount details
                setDiscountName(discountData.discount_name || "");
                setDiscountAmount(discountData.discount_amount || "");

                // Format dates for input fields
                if (discountData.start_date) {
                    const startDateObj = new Date(discountData.start_date);
                    setStartDate(startDateObj.toISOString().split('T')[0]);
                }

                if (discountData.end_date) {
                    const endDateObj = new Date(discountData.end_date);
                    setEndDate(endDateObj.toISOString().split('T')[0]);
                }

                // Determine discount type and set selected type and ID
                if (discountData.product_id_pk) {
                    setSelectedType("product");
                    setSelectedId(discountData.product_id_pk);
                    setProductDiscountProductIdPk(discountData.product_id_pk);
                } else if (discountData.brand_id_pk) {
                    setSelectedType("brand");
                    setSelectedId(discountData.brand_id_pk);
                    setProductDiscountBrandIdPk(discountData.brand_id_pk);
                } else if (discountData.category_id_pk) {
                    setSelectedType("category");
                    setSelectedId(discountData.category_id_pk);
                    setProductDiscountCategoryIdPk(discountData.category_id_pk);
                } else if (discountData.sub_category_id_pk) {
                    setSelectedType("sub_category");
                    setSelectedId(discountData.sub_category_id_pk);
                    setProductDiscountSubCategoryIdPk(discountData.sub_category_id_pk);
                }
            })
            .catch(error => {
                console.error("Error fetching discount:", error.response ? error.response.data : error);
                setMessage("Error fetching discount details");
                setMessageType("danger");
                // navigate("/404");
            });
    }, [id]);

    // Fetch categories and all subcategories
    useEffect(() => {
        axios
            .get(`${API_BASE_URL}/categories/fetch-all/`, {
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                    "Content-Type": "application/json",
                },
            })
            .then(async (response) => {
                const fetchedCategories = response.data.product_category;
                setCategories(fetchedCategories);

                // Fetch all subcategories for all categories
                const subcategoryPromises = fetchedCategories.map((category) =>
                    axios
                        .get(`${API_BASE_URL}/sub-categories/fetch-all-product-sub-categories-for-a-category/${category.id}/`, {
                            headers: {
                                Authorization: `Bearer ${Cookies.get("accessToken")}`,
                                "Content-Type": "application/json",
                            },
                        })
                        .then((subRes) => subRes.data.product_sub_category || [])
                        .catch((error) => {
                            console.error(`Error fetching subcategories for category ${category.id}:`, error);
                            return [];
                        })
                );

                // Resolve all subcategory requests and flatten into one array
                const allSubcategories = (await Promise.all(subcategoryPromises)).flat();
                setSubCategories(allSubcategories);
            })
            .catch((error) => {
                console.error("Error fetching categories:", error);
                setMessage("Error fetching categories");
                setMessageType("danger");
            });
    }, []);

    useEffect(() => {
        axios
            .get(`${API_BASE_URL}/fetch-product/`, {
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                    "Content-Type": "application/json",
                },
            })
            .then((response) => {
                const data = response.data.product_data;
                setProducts(data);
            })
            .catch((error) => {
                console.error("Error fetching options:", error);
            });
    }, []);

    useEffect(() => {
        axios
            .get(`${API_BASE_URL}/product-brand/fetch-product-brands/`, {
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                    "Content-Type": "application/json",
                },
            })
            .then((response) => {
                const data = response.data.product_brands;
                setBrands(data);
            })
            .catch((error) => {
                console.error("Error fetching options:", error);
            });
    }, []);

    // Update options based on selected type
    useEffect(() => {
        if (selectedType) {
            let url = "";
            switch (selectedType) {
                case "product":
                    url = `${API_BASE_URL}/fetch-product/`;
                    break;
                case "brand":
                    url = `${API_BASE_URL}/product-brand/fetch-product-brands/`;
                    break;
                case "category":
                    setOptions(categories);
                    return;
                case "sub_category":
                    setOptions(subCategories);
                    return;
                default:
                    setOptions([]);
                    return;
            }

            axios
                .get(url, {
                    headers: {
                        Authorization: `Bearer ${Cookies.get("accessToken")}`,
                        "Content-Type": "application/json",
                    },
                })
                .then((response) => {
                    const data = selectedType === "product"
                        ? response.data.product_data
                        : response.data.product_brands;
                    setOptions(data || []);
                })
                .catch((error) => {
                    console.error("Error fetching options:", error);
                    setMessage(`Error fetching ${selectedType} options`);
                    setMessageType("danger");
                });
        }
    }, [selectedType, categories, subCategories]);

    // Filter subcategories when a category is selected (only if type is sub_category)
    useEffect(() => {
        if (selectedType === "sub_category" && selectedCategory) {
            const filteredSubcats = subCategories.filter(
                (subcat) => subcat.category_pk === selectedCategory
            );
            setOptions(filteredSubcats);
        }
    }, [selectedCategory, selectedType, subCategories]);

    const handleDeleteDiscount = () => {
        setShowDeleteModal(true);
    };

    const confirmDelete = () => {
        // Format dates correctly without "Z"
        const formattedStartDate = new Date(startDate).toISOString().replace("Z", "");
        const formattedEndDate = new Date(endDate).toISOString().replace("Z", "");

        // Create request data
        const requestData = {
            discount_name: discountName,
            discount_amount: parseFloat(discountAmount),
            start_date: formattedStartDate,
            end_date: formattedEndDate,
            delete: true,
        };

        // Add the appropriate ID fields based on the discount type
        if (productDiscountProductIdPk) requestData.product_discount_product_id_pk = productDiscountProductIdPk;
        if (productDiscountBrandIdPk) requestData.product_discount_brand_id_pk = productDiscountBrandIdPk;
        if (productDiscountCategoryIdPk) requestData.product_discount_category_id_pk = productDiscountCategoryIdPk;
        if (productDiscountSubCategoryIdPk) requestData.product_discount_sub_category_id_pk = productDiscountSubCategoryIdPk;

        // Add the new target ID
        switch (selectedType) {
            case "product":
                requestData.product_id = selectedId;
                break;
            case "brand":
                requestData.brand_id = selectedId;
                break;
            case "category":
                requestData.category_id = selectedId;
                break;
            case "sub_category":
                requestData.sub_category_id = selectedId;
                break;
            default:
                break;
        }

        console.log("Update request data:", requestData);

        axios.put(`${API_BASE_URL}/product-discounts/update/`, requestData, {
            headers: {
                Authorization: `Bearer ${Cookies.get("accessToken")}`,
                "Content-Type": "application/json"
            }
        })
            .then(response => {
                setMessage("Discount deleted successfully!");
                setMessageType("success");
                setTimeout(() => {
                    navigate("/products/discount");
                }, 2000);
            })
            .catch(error => {
                console.error("Error deleting discount:", error);
                setMessage("Error deleting discount: " + (error.response?.data?.message || error.message));
                setMessageType("danger");
            });

        setShowDeleteModal(false);
    };

    const cancelDelete = () => {
        setShowDeleteModal(false);
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        // Validate input fields
        if (!discountName.trim()) {
            setMessage("Discount name is required!");
            setMessageType("danger");
            return;
        }

        if (!discountAmount.trim() || isNaN(parseFloat(discountAmount))) {
            setMessage("Valid discount amount is required!");
            setMessageType("danger");
            return;
        }

        if (!startDate || !endDate) {
            setMessage("Start and end dates are required!");
            setMessageType("danger");
            return;
        }

        if (!selectedType || !selectedId) {
            setMessage("Please select a discount type and target!");
            setMessageType("danger");
            return;
        }

        if ((new Date(startDate) > new Date(endDate))) {
            setMessage("Start date must be before the end date.");
            setMessageType("danger");
            return;
        }

        // Check if start date and end date are the same
        if (new Date(startDate).getTime() === new Date(endDate).getTime()) {
            setMessage("Start date and end date cannot be the same.");
            setMessageType("danger");
            return;
        }

        // Format dates correctly without "Z"
        const formattedStartDate = new Date(startDate).toISOString().replace("Z", "");
        const formattedEndDate = new Date(endDate).toISOString().replace("Z", "");

        // Create request data
        const requestData = {
            discount_name: discountName,
            discount_amount: parseFloat(discountAmount),
            start_date: formattedStartDate,
            end_date: formattedEndDate,
        };

        // Add the appropriate ID fields based on the discount type
        if (productDiscountProductIdPk) requestData.product_discount_product_id_pk = productDiscountProductIdPk;
        if (productDiscountBrandIdPk) requestData.product_discount_brand_id_pk = productDiscountBrandIdPk;
        if (productDiscountCategoryIdPk) requestData.product_discount_category_id_pk = productDiscountCategoryIdPk;
        if (productDiscountSubCategoryIdPk) requestData.product_discount_sub_category_id_pk = productDiscountSubCategoryIdPk;

        // Add the new target ID
        switch (selectedType) {
            case "product":
                requestData.product_id = selectedId;
                break;
            case "brand":
                requestData.brand_id = selectedId;
                break;
            case "category":
                requestData.category_id = selectedId;
                break;
            case "sub_category":
                requestData.sub_category_id = selectedId;
                break;
            default:
                break;
        }

        console.log("Update request data:", requestData);

        // Send update request
        axios.put(`${API_BASE_URL}/product-discounts/update/`, requestData, {
            headers: {
                Authorization: `Bearer ${Cookies.get("accessToken")}`,
                "Content-Type": "application/json"
            }
        })
            .then(response => {
                setMessage("Discount updated successfully!");
                setMessageType("success");
            })
            .catch(error => {
                setMessage("Error updating discount: " + (error.response?.data?.message || error.message));
                setMessageType("danger");
            });
    };

    // Get the name field based on the entity type
    const getDisplayField = (option) => {
        if (!option) return "";

        switch (selectedType) {
            case "product":
                return option.product_name || "Unnamed Product";
            case "brand":
                return option.brand_name || "Unnamed Brand";
            case "category":
                return option.category_name || "Unnamed Category";
            case "sub_category":
                return option.sub_category_name || "Unnamed Subcategory";
            default:
                return "Unknown";
        }
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
                        onClick={() => setMessage('')}
                    ></button>
                </div>
            )}
            <div className="card invoice-container">
                <div className="card-header">
                    <h5>Product Discount Update</h5>
                    <Link to="/products/discounts" className="btn btn-primary">← Back</Link>
                </div>
                <div className="card-body p-0">
                    <form onSubmit={handleSubmit}>
                        <div className="px-4 py-3">
                            <div className="row">
                                <div className="col-md-6">
                                    <div className="form-group mb-3">
                                        <label htmlFor="discountName" className="form-label">Discount Name:</label>
                                        <input
                                            type="text"
                                            className="form-control"
                                            id="discountName"
                                            value={discountName}
                                            onChange={(e) => setDiscountName(e.target.value)}
                                            placeholder="Enter discount name"
                                            required
                                        />
                                    </div>
                                </div>
                                <div className="col-md-6">
                                    <div className="form-group mb-3">
                                        <label htmlFor="discountAmount" className="form-label">Discount Amount (%):</label>
                                        <input
                                            type="number"
                                            step="0.01"
                                            min="0"
                                            max="100"
                                            className="form-control"
                                            id="discountAmount"
                                            value={discountAmount}
                                            onChange={(e) => setDiscountAmount(e.target.value)}
                                            placeholder="Enter discount percentage"
                                            required
                                        />
                                    </div>
                                </div>
                            </div>
                            <div className="row">
                                <div className="col-md-6">
                                    <div className="form-group mb-3">
                                        <label htmlFor="startDate" className="form-label">Start Date:</label>
                                        <input
                                            type="date"
                                            className="form-control"
                                            id="startDate"
                                            value={startDate}
                                            onChange={(e) => setStartDate(e.target.value)}
                                            required
                                        />
                                    </div>
                                </div>
                                <div className="col-md-6">
                                    <div className="form-group mb-3">
                                        <label htmlFor="endDate" className="form-label">End Date:</label>
                                        <input
                                            type="date"
                                            className="form-control"
                                            id="endDate"
                                            value={endDate}
                                            onChange={(e) => setEndDate(e.target.value)}
                                            required
                                        />
                                    </div>
                                </div>
                            </div>

                            <div className="row">
                                {/* <div className="col-md-6">
                                    <div className="form-group mb-3">
                                        <label htmlFor="discountType" className="form-label">Discount Type:</label>
                                        <select
                                            className="form-select"
                                            id="discountType"
                                            value={selectedType}
                                            onChange={handleTypeChange}
                                            required
                                        >
                                            <option value="">Select Discount Type</option>
                                            <option value="product">Product</option>
                                            <option value="brand">Brand</option>
                                            <option value="category">Category</option>
                                            <option value="sub_category">Sub Category</option>
                                        </select>
                                    </div>
                                </div> */}

                                {selectedType && (
                                    <div className="col-md-6">
                                        <div className="form-group mb-3">
                                            <label htmlFor="selectTarget" className="form-label">
                                                Select {selectedType === "product"
                                                    ? "Product"
                                                    : selectedType === "brand"
                                                        ? "Brand"
                                                        : selectedType === "category"
                                                            ? "Category"
                                                            : "Sub Category"}:
                                            </label>
                                            <select
                                                className="form-select"
                                                id="selectTarget"
                                                value={selectedId}
                                                onChange={(e) => setSelectedId(e.target.value)}
                                                required
                                            >
                                                <option value="">Select Option</option>
                                                {options.map((option) => (
                                                    <option
                                                        key={option.id}
                                                        value={option.id}
                                                    >
                                                        {getDisplayField(option)}
                                                    </option>
                                                ))}
                                            </select>
                                        </div>
                                    </div>
                                )}
                            </div>

                            <div className="d-flex gap-2 mt-3">
                                <button type="submit" className="btn btn-success">
                                    Update Discount
                                </button>
                                <button
                                    type="button"
                                    className="btn btn-danger"
                                    onClick={handleDeleteDiscount}
                                >
                                    Delete Discount
                                </button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>

            {/* Confirmation Modal */}
            <ConfirmationModal
                show={showDeleteModal}
                onClose={cancelDelete}
                onConfirm={confirmDelete}
                message="Are you sure you want to delete this discount? This action cannot be undone."
            />
        </div>
    );
};

export default ProductDiscountUpdate;