import Cookies from 'js-cookie';
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const TabProfilePicture = () => {
    const navigate = useNavigate();
    const [adminAvatar, setAdminAvatar] = useState(null);
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState('');

    const API_BASE_URL = 'http://127.0.0.1:8000/server_api/business-admin/';
    const userName = Cookies.get('username');

    const closeMessage = () => {
        setMessage('');
        setMessageType('');
    };

    const handleChange = (e) => {
        const { files } = e.target;
        if (files && files[0]) {
            setAdminAvatar(files[0]);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!adminAvatar) {
            setMessage('Please select an image file.');
            setMessageType('error');
            return;
        }

        const formData = new FormData();
        formData.append('admin_avatar', adminAvatar);

        try {
            const response = await fetch(`${API_BASE_URL}update/${userName}/`, {
                method: 'PUT',
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                },
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Error updating Avatar. Please try again later.');
            }

            setMessage('Avatar updated successfully');
            setMessageType('success');
            setAdminAvatar(null);
            e.target.reset(); // Reset file input
            window.location.reload(); // Reload the page to reflect changes
        } catch (error) {
            setMessage(error.message);
            setMessageType('error');
            console.error('Error changing password:', error);
        }
    };

    return (
        <div className="tab-pane fade p-4" id="profilePictureTab" role="tabpanel">
            {message && (
                <div className={`alert alert-${messageType === 'success' ? 'success' : 'danger'} alert-dismissible fade show`} role="alert">
                    {message}
                    <button type="button" className="btn-close" onClick={closeMessage}></button>
                </div>
            )}
            <form className="mt-4" onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>New Profile Avatar</label>
                    <input
                        type="file"
                        name="admin_avatar"
                        accept="image/png, image/jpg, image/jpeg"
                        onChange={handleChange}
                        className="form-control"
                        required
                    />
                </div>

                <button type="submit" className="btn btn-primary mt-4">Update Profile Avatar</button>
            </form>
        </div>
    );
};

export default TabProfilePicture;
