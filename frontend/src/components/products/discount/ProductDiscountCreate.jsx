import React, { useState, useEffect } from "react";
import axios from "axios";
import Cookies from "js-cookie";

const ProductDiscountCreate = () => {
    const [discountName, setDiscountName] = useState("");
    const [discountAmount, setDiscountAmount] = useState("");
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");
    const [selectedType, setSelectedType] = useState(""); // "product", "brand", "category", "sub_category"
    const [selectedId, setSelectedId] = useState(""); // ID of selected type
    const [categories, setCategories] = useState([]); // List of categories
    const [subCategories, setSubCategories] = useState([]); // Subcategories for selected category
    const [options, setOptions] = useState([]); // Dynamic dropdown values
    const [selectedCategory, setSelectedCategory] = useState(""); // Selected category for subcategories
    const [message, setMessage] = useState("");
    const [messageType, setMessageType] = useState("");

    const API_BASE_URL = "http://127.0.0.1:8000/server_api/product";

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
                setCategories(fetchedCategories); // Store categories separately

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
                            return []; // Handle errors gracefully
                        })
                );

                // Resolve all subcategory requests and flatten into one array
                const allSubcategories = (await Promise.all(subcategoryPromises)).flat();
                setSubCategories(allSubcategories); // Store subcategories separately
            })
            .catch((error) => console.error("Error fetching categories:", error));
    }, []);


    // Fetch data dynamically based on selected type
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
                    setOptions(categories); // Use already fetched categories
                    return;
                case "sub_category":
                    setOptions(subCategories); // Use subcategories based on selected category
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
                    setOptions(response.data.product_data || response.data.product_brands);
                })
                .catch((error) => console.error("Error fetching options:", error));
        }
    }, [selectedType, categories, subCategories]);

    const handleSubmit = (e) => {
        e.preventDefault();

        if (!discountName || !discountAmount || !startDate || !endDate || !selectedType || !selectedId) {
            setMessage("All fields are required!");
            setMessageType("danger");
            return;
        }

        // Validate discountAmount (must be between 1 and 100)
        const discountValue = parseFloat(discountAmount);
        if (isNaN(discountValue) || discountValue < 1 || discountValue > 100) {
            setMessage("Discount amount must be between 1% and 100%.");
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

        const payload = {
            discount_name: discountName,
            discount_amount: discountValue,
            start_date: formattedStartDate,
            end_date: formattedEndDate,
        };

        // Assign selected type dynamically
        payload[`${selectedType}_id`] = selectedId;

        console.log("Payload:", payload);

        axios
            .post(`${API_BASE_URL}/product-discounts/create/`, payload, {
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                    "Content-Type": "application/json",
                },
            })
            .then((response) => {
                setMessage(response.data.message);
                setMessageType("success");
                setDiscountName("");
                setDiscountAmount("");
                setStartDate("");
                setEndDate("");
                setSelectedType("");
                setSelectedId("");
                setSelectedCategory("");
            })
            .catch((error) => {
                setMessage(error.response?.data?.error || "Error creating discount");
                setMessageType("danger");
            });
    };



    return (
        <div className="col-lg-12">
            <div className="card stretch stretch-full function-table">
                <div className="card-body p-0">
                    <div className="container">
                        <h3>Create Product Discount</h3>

                        {message && (
                            <div className={`alert alert-${messageType}`}>
                                {message}
                            </div>
                        )}

                        <form onSubmit={handleSubmit}>
                            <div className="mb-3">
                                <label className="form-label">Discount Name</label>
                                <input
                                    type="text"
                                    className="form-control"
                                    value={discountName}
                                    onChange={(e) => setDiscountName(e.target.value)}
                                    required
                                />
                            </div>

                            <div className="mb-3">
                                <label className="form-label">Discount Amount (%)</label>
                                <input
                                    type="number"
                                    className="form-control"
                                    value={discountAmount}
                                    onChange={(e) => setDiscountAmount(e.target.value)}
                                    min="1"
                                    max="100"
                                    required
                                />

                            </div>

                            <div className="mb-3">
                                <label className="form-label">Start Date</label>
                                <input
                                    type="datetime-local"
                                    className="form-control"
                                    value={startDate}
                                    onChange={(e) => setStartDate(e.target.value)}
                                    required
                                />
                            </div>

                            <div className="mb-3">
                                <label className="form-label">End Date</label>
                                <input
                                    type="datetime-local"
                                    className="form-control"
                                    value={endDate}
                                    onChange={(e) => setEndDate(e.target.value)}
                                    required
                                />
                            </div>

                            <div className="mb-3">
                                <label className="form-label">Apply Discount To</label>
                                <select
                                    className="form-control"
                                    value={selectedType}
                                    onChange={(e) => {
                                        setSelectedType(e.target.value);
                                        setSelectedId(""); // Reset selection
                                    }}
                                    required
                                >
                                    <option value="">Select One</option>
                                    <option value="product">Product</option>
                                    <option value="brand">Brand</option>
                                    <option value="category">Category</option>
                                    <option value="sub_category">Sub Category</option>
                                </select>
                            </div>

                            {selectedType && (
                                <div className="mb-3">
                                    <label className="form-label">Select {selectedType.replace("_", " ")}</label>
                                    <select
                                        className="form-control"
                                        value={selectedId}
                                        onChange={(e) => setSelectedId(e.target.value)}
                                        required
                                    >
                                        <option value="">Select {selectedType.replace("_", " ")}</option>
                                        {options.map((item) => (
                                            <option key={item.id} value={item.id}>
                                                {item.category_name || item.sub_category_name || item.product_name || item.brand_name}
                                            </option>
                                        ))}
                                    </select>
                                </div>
                            )}

                            <button type="submit" className="btn btn-success">
                                Create Discount
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ProductDiscountCreate;
