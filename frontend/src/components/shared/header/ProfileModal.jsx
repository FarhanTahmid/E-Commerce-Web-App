import React, { useEffect, useState, Fragment } from "react";
import {
    FiActivity, FiBell, FiChevronRight, FiDollarSign, FiLogOut, FiSettings, FiUser,
} from "react-icons/fi";
import Cookies from "js-cookie";
import axios from 'axios';

const activePosition = ["Active", "Always", "Bussy", "Inactive", "Disabled", "Cutomization"];
const subscriptionsList = ["Plan", "Billings", "Referrals", "Payments", "Statements", "Subscriptions"];

const ProfileModal = () => {
    const [avatar, setAvatar] = useState("/images/avatar/default.jpg"); // Default avatar
    const admin_user_name = Cookies.get("username");

    useEffect(() => {
        const accessToken = Cookies.get('accessToken'); // Ensure accessToken is available
        if (!accessToken || !admin_user_name) return; // Exit if no token or admin_user_name

        axios.get(`http://127.0.0.1:8000/server_api/business-admin/avatar/${admin_user_name}`, {
            headers: {
                Authorization: `Bearer ${accessToken}`,
            },
        })
            .then(response => {
                if (response.status === 200) {
                    setAvatar("http://" + response.data.admin_avatar);
                } else {
                    setAvatar('/images/avatar/default.jpg'); // Fallback to default avatar
                }
            })
            .catch(error => {
                console.error('Error fetching avatar:', error);
                setAvatar('/images/avatar/default.jpg'); // Fallback to default avatar
            });

    }, [admin_user_name]);

    const handleLogout = async () => {
        const refreshToken = Cookies.get("refreshToken");
        if (!refreshToken) {
            console.error("No refresh token found");
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:8000/server_api/business-admin/logout/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                },
                body: JSON.stringify({ refresh: refreshToken }),
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

            // Clear cookies and redirect
            Cookies.remove("accessToken");
            Cookies.remove("refreshToken");
            Cookies.remove("username");
            window.location.href = "/";
        } catch (error) {
            console.error("Logout failed:", error);
            alert("Logout failed. Please try again.");
        }
    };

    return (
        <div className="dropdown nxl-h-item">
            <a href="#" data-bs-toggle="dropdown" role="button" data-bs-auto-close="outside">
                <div style={{ width: '40px', height: '40px' }} className="w-8 h-8 d-flex align-items-center justify-content-center rounded-circle bg-light me-3 overflow-hidden">
                    <img src={avatar} alt="user-image" className="rounded-circle border" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                </div>
            </a>
            <div className="dropdown-menu dropdown-menu-end nxl-h-dropdown nxl-user-dropdown">
                <div className="dropdown-header">
                    <div className="d-flex align-items-center">
                        <div style={{ width: '40px', height: '40px' }} className="w-8 h-8 d-flex align-items-center justify-content-center rounded-circle bg-light me-3 overflow-hidden">
                            <img src={avatar} alt="user-image" className="rounded-circle border" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                        </div>
                        <div>
                            <h6 className="text-dark mb-0">
                                Alexandra Della {/* <span className="badge bg-soft-success text-success ms-1">PRO</span> */}
                            </h6>
                            <span className="fs-12 fw-medium text-muted">alex.della@outlook.com</span>
                        </div>
                    </div>
                </div>
                {/* <div className="dropdown">
                    <a href="#" className="dropdown-item" data-bs-toggle="dropdown">
                        <span className="hstack">
                            <i className="wd-10 ht-10 border border-2 border-gray-1 bg-success rounded-circle me-2"></i>
                            <span>Active</span>
                        </span>
                        <i className="ms-auto me-0"><FiChevronRight /></i>
                    </a>
                    <div className="dropdown-menu user-active">
                        {activePosition.map((item, index) => (
                            <Fragment key={index}>
                                {index === activePosition.length - 1 && <div className="dropdown-divider"></div>}
                                <a href="#" className="dropdown-item">
                                    <span className="hstack">
                                        <i className={`wd-10 ht-10 border border-2 border-gray-1 rounded-circle me-2 ${getColor(item)}`}></i>
                                        <span>{item}</span>
                                    </span>
                                </a>
                            </Fragment>
                        ))}
                    </div>
                </div> */}
                {/* <div className="dropdown">
                    <a href="#" className="dropdown-item" data-bs-toggle="dropdown">
                        <span className="hstack">
                            <i className="me-2"><FiDollarSign /></i>
                            <span>Subscriptions</span>
                        </span>
                        <i className="ms-auto me-0"><FiChevronRight /></i>
                    </a>
                    <div className="dropdown-menu">
                        {subscriptionsList.map((item, index) => (
                            <Fragment key={index}>
                                {index === subscriptionsList.length - 1 && <div className="dropdown-divider"></div>}
                                <a href="#" className="dropdown-item">
                                    <span className="hstack">
                                        <i className="wd-5 ht-5 bg-gray-500 rounded-circle me-3"></i>
                                        <span>{item}</span>
                                    </span>
                                </a>
                            </Fragment>
                        ))}
                    </div>
                </div>
                <div className="dropdown-divider"></div> */}
                <a href="/profile/details" className="dropdown-item">
                    <i><FiUser /></i>
                    <span>Profile Details</span>
                </a>
                {/* <a href="#" className="dropdown-item">
                    <i><FiActivity /></i>
                    <span>Activity Feed</span>
                </a>
                <a href="#" className="dropdown-item">
                    <i><FiDollarSign /></i>
                    <span>Billing Details</span>
                </a>
                <a href="#" className="dropdown-item">
                    <i><FiBell /></i>
                    <span>Notifications</span>
                </a> */}
                {/* <a href="#" className="dropdown-item">
                    <i><FiSettings /></i>
                    <span>Account Settings</span>
                </a> */}
                <div className="dropdown-divider"></div>
                <a href="#" className="dropdown-item" onClick={handleLogout}>
                    <i><FiLogOut /></i>
                    <span>Logout</span>
                </a>
            </div>
        </div>
    );
};

export default ProfileModal;

const getColor = (item) => {
    switch (item) {
        case "Always":
            return "always_clr";
        case "Bussy":
            return "bussy_clr";
        case "Inactive":
            return "inactive_clr";
        case "Disabled":
            return "disabled_clr";
        case "Cutomization":
            return "cutomization_clr";
        default:
            return "active-clr";
    }
};
