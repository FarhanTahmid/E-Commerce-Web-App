import React, { useEffect, useState } from 'react'
import { BsPatchCheckFill } from 'react-icons/bs'
import { FiEdit, FiMail, FiMapPin, FiPhone, FiTrash2 } from 'react-icons/fi'
import Cookies from 'js-cookie';
import axios from 'axios';

const Profile = () => {
    const [userData, setUserData] = useState(null);
    const API_BASE_URL = 'http://127.0.0.1:8000/server_api/business-admin/admin';
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

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const username = `${Cookies.get("username")}`; // Retrieve username from cookies
                if (!username) {
                    console.error("Username not found in cookies");
                    return;
                }

                const response = await fetch(`${API_BASE_URL}/fetch-all/?admin_user_name=${username}`,
                    {
                        method: "GET",
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${Cookies.get("accessToken")}`, // Adjust as per auth mechanism
                        }
                    }
                );

                const data = await response.json();
                console.log("API Response:", data); // Console log the API response

                if (response.ok) {
                    setUserData(data.admin_users);
                } else {
                    console.error("Error fetching user data:", data.error);
                }
            } catch (error) {
                console.error("Fetch error:", error);
            }
        };

        fetchUserData();
    }, []);


    return (

        <div className="card stretch stretch-full">
            <div className="card-body">
                <div className="mb-4 text-center">
                    <div className="wd-150 ht-150 mx-auto mb-3 position-relative">
                        <div className="avatar-image wd-150 ht-150 border border-5 border-gray-3">
                            <img src={avatar} alt="img" className="img-fluid" />
                        </div>
                        <div className="wd-10 ht-10 text-success rounded-circle position-absolute translate-middle" style={{ top: "76%", right: "10px" }}>
                            <BsPatchCheckFill size={16} />
                        </div>
                    </div>
                    <div className="mb-4">
                        <a href="#" className="fs-14 fw-bold d-block">{userData?.admin_full_name || "Full Name"}</a>
                        <a href="#" className="fs-12 fw-normal text-muted d-block">{userData?.admin_email || "Email Addres"}</a>
                    </div>
                    {/* <div className="fs-12 fw-normal text-muted text-center d-flex flex-wrap gap-3 mb-4">
                        <div className="flex-fill py-3 px-4 rounded-1 d-none d-sm-block border border-dashed border-gray-5">
                            <h6 className="fs-15 fw-bolder">28.65K</h6>
                            <p className="fs-12 text-muted mb-0">Followers</p>
                        </div>
                        <div className="flex-fill py-3 px-4 rounded-1 d-none d-sm-block border border-dashed border-gray-5">
                            <h6 className="fs-15 fw-bolder">38.85K</h6>
                            <p className="fs-12 text-muted mb-0">Following</p>
                        </div>
                        <div className="flex-fill py-3 px-4 rounded-1 d-none d-sm-block border border-dashed border-gray-5">
                            <h6 className="fs-15 fw-bolder">43.67K</h6>
                            <p className="fs-12 text-muted mb-0">Engagement</p>
                        </div>
                    </div> */}
                </div>
                <ul className="list-unstyled mb-4">
                    {/* <li className="hstack justify-content-between mb-4">
                        <span className="text-muted fw-medium hstack gap-3"><FiMapPin size={16} />Location</span>
                        <a href="#" className="float-end">California, USA</a>
                    </li> */}
                    <li className="hstack justify-content-between mb-4">
                        <span className="text-muted fw-medium hstack gap-3"><FiPhone size={16} />Phone</span>
                        <a href="#" className="float-end">{userData?.admin_contact_no || "Contact No."}</a>
                    </li>
                    <li className="hstack justify-content-between mb-0">
                        <span className="text-muted fw-medium hstack gap-3"><FiMail size={16} />Email</span>
                        <a href="#" className="float-end">{userData?.admin_email || "Email Address"}</a>
                    </li>
                </ul>

            </div>
        </div>


    )
}

export default Profile