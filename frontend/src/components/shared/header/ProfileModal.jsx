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
    const [userInfo, setUserInfo] = useState({});
    const API_BASE_URL = 'http://127.0.0.1:8000/server_api/business-admin/'

    useEffect(() => {

        const accessToken = Cookies.get('accessToken'); // Ensure accessToken is available
        if (!accessToken || !admin_user_name) return; // Exit if no token or admin_user_name

        axios.get(`${API_BASE_URL}avatar/${admin_user_name}`, {
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
    useEffect(() => {
        fetchUserInfo();
    }, []);

    const fetchUserInfo = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}admin/fetch-all/?admin_user_name=${admin_user_name}`, {
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                },
            });

            const data = await response.json();

            if (data.admin_users) {
                setUserInfo(data.admin_users);  // Triggers useEffect to fetch position
            }
        } catch (error) {
            console.error('Error fetching user info:', error);
        }
    };

    const handleLogout = () => {
        const refreshToken = Cookies.get("refreshToken");
        console.log("Refresh token:", refreshToken);
        if (!refreshToken) {
            console.error("No refresh token found");
            return;
        }

        try {
            const response = fetch("http://127.0.0.1:8000/server_api/business-admin/logout/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                },
                body: JSON.stringify({ refresh: refreshToken }),
            });

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
                        <div>
                            <h6 className="text-dark mb-0 fw-small">
                                {userInfo.admin_full_name} {/* <span className="badge bg-soft-success text-success ms-1">PRO</span> */}
                            </h6>
                            <span className="fs-12 fw-medium text-muted">{userInfo.admin_email}</span>
                        </div>
                    </div>
                </div>
                <a href="/profile/details" className="dropdown-item">
                    <i><FiUser /></i>
                    <span>Profile Details</span>
                </a>
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
