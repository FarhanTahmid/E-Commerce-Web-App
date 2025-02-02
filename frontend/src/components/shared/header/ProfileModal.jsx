import React, { Fragment } from 'react';
import { FiActivity, FiBell, FiChevronRight, FiDollarSign, FiLogOut, FiSettings, FiUser } from "react-icons/fi";
import Cookies from 'js-cookie';

const activePosition = ["Active", "Always", "Bussy", "Inactive", "Disabled", "Cutomization"];
const subscriptionsList = ["Plan", "Billings", "Referrals", "Payments", "Statements", "Subscriptions"];

const ProfileModal = () => {
    const handleLogout = async () => {
        const refreshToken = Cookies.get('refreshToken');

        if (!refreshToken) {
            console.error('No refresh token found');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/server_api/business-admin/logout/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${Cookies.get('accessToken')}` // Include the access token in the Authorization header
                },
                body: JSON.stringify({ refresh: refreshToken })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Remove the authToken cookie
            Cookies.remove('accessToken');
            Cookies.remove('refreshToken');
            Cookies.remove('username');

            // Redirect to the login page
            window.location.href = '/';
        } catch (error) {
            console.error('Logout failed:', error);

            // Optionally, you can handle specific errors here
            if (error.message.includes('429')) {
                alert('Too many requests - try again in 1 minute');
            } else {
                alert('Logout failed. Please try again or contact support.');
            }
        }
    };

    return (
        <div className="dropdown nxl-h-item">
            <a href="#" data-bs-toggle="dropdown" role="button" data-bs-auto-close="outside">
                <img src="/images/avatar/1.png" alt="user-image" className="img-fluid user-avtar me-0" />
            </a>
            <div className="dropdown-menu dropdown-menu-end nxl-h-dropdown nxl-user-dropdown">
                <div className="dropdown-header">
                    <div className="d-flex align-items-center">
                        <img src="/images/avatar/1.png" alt="user-image" className="img-fluid user-avtar" />
                        <div>
                            <h6 className="text-dark mb-0">Alexandra Della <span className="badge bg-soft-success text-success ms-1">PRO</span></h6>
                            <span className="fs-12 fw-medium text-muted">alex.della@outlook.com</span>
                        </div>
                    </div>
                </div>
                <div className="dropdown">
                    <a href="#" className="dropdown-item" data-bs-toggle="dropdown">
                        <span className="hstack">
                            <i className="wd-10 ht-10 border border-2 border-gray-1 bg-success rounded-circle me-2"></i>
                            <span>Active</span>
                        </span>
                        <i className="ms-auto me-0"><FiChevronRight /></i>
                    </a>
                    <div className="dropdown-menu user-active">
                        {
                            activePosition.map((item, index) => (
                                <Fragment key={index}>
                                    {index === activePosition.length - 1 && <div className="dropdown-divider"></div>}
                                    <a href="#" className="dropdown-item">
                                        <span className="hstack">
                                            <i className={`wd-10 ht-10 border border-2 border-gray-1 rounded-circle me-2 ${getColor(item)}`}></i>
                                            <span>{item}</span>
                                        </span>
                                    </a>
                                </Fragment>
                            ))
                        }
                    </div>
                </div>
                <div className="dropdown-divider"></div>
                <div className="dropdown">
                    <a href="#" className="dropdown-item" data-bs-toggle="dropdown">
                        <span className="hstack">
                            <i className=" me-2"><FiDollarSign /></i>
                            <span>Subscriptions</span>
                        </span>
                        <i className="ms-auto me-0"><FiChevronRight /></i>
                    </a>
                    <div className="dropdown-menu">
                        {
                            subscriptionsList.map((item, index) => (
                                <Fragment key={index}>
                                    {index === subscriptionsList.length - 1 && <div className="dropdown-divider"></div>}
                                    <a href="#" className="dropdown-item">
                                        <span className="hstack">
                                            <i className="wd-5 ht-5 bg-gray-500 rounded-circle me-3"></i>
                                            <span>{item}</span>
                                        </span>
                                    </a>
                                </Fragment>
                            ))
                        }
                    </div>
                </div>
                <div className="dropdown-divider"></div>
                <a href="#" className="dropdown-item">
                    <i ><FiUser /></i>
                    <span>Profile Details</span>
                </a>
                <a href="#" className="dropdown-item">
                    <i ><FiActivity /></i>
                    <span>Activity Feed</span>
                </a>
                <a href="#" className="dropdown-item">
                    <i ><FiDollarSign /></i>
                    <span>Billing Details</span>
                </a>
                <a href="#" className="dropdown-item">
                    <i><FiBell /></i>
                    <span>Notifications</span>
                </a>
                <a href="#" className="dropdown-item">
                    <i><FiSettings /></i>
                    <span>Account Settings</span>
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
