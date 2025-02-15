import React from 'react'
import PageHeader from '@/components/shared/pageHeader/PageHeader'
import Footer from '@/components/shared/Footer'
import AdminManagementPermissionsTable from '@/components/admin-management/permissions/AdminManagementPermissionsTable'

const AdminManagementPermissions = () => {
    return (
        <>
            <PageHeader>
            </PageHeader>
            <div className='main-content'>
                <div className='row'>
                    <AdminManagementPermissionsTable />
                </div>
            </div>
            <Footer />
        </>
    )
}

export default AdminManagementPermissions