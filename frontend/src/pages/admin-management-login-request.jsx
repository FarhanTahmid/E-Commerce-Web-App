import React from 'react'
import PageHeader from '@/components/shared/pageHeader/PageHeader'
import Footer from '@/components/shared/Footer'
import AdminManagementLoginRequestsTable from '@/components/admin-management/login-requests/AdminManagementLoginRequestsTable'

const AdminManagementLoginRequest = () => {
    return (
        <>
            <PageHeader>
            </PageHeader>
            <div className='main-content'>
                <div className='row'>
                    <AdminManagementLoginRequestsTable />
                </div>
            </div>
            <Footer />
        </>
    )
}

export default AdminManagementLoginRequest