import React from 'react';

const ConfirmationModal = ({ show, onClose, onConfirm, message, option }) => {
    if (!show) return null;

    return (
        <div className="modal" style={{ display: 'block', position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.5)' }}>
            <div className="modal-content" style={{ margin: '15% auto', backgroundColor: 'white', padding: '20px', borderRadius: '5px', width: '300px' }}>
                <h5>{message}</h5>
                <div className="d-flex justify-content-between mt-4">
                    <button className="btn btn-secondary" onClick={onClose}>Cancel</button>
                    {option ? <button className="btn btn-primary" onClick={onConfirm}>{option}</button> : <button className="btn btn-danger" onClick={onConfirm}>Delete</button>}
                </div>
            </div>
        </div>
    );
};

export default ConfirmationModal;
