import React from 'react'
import PageHeader from '@/components/shared/pageHeader/PageHeader'
import Footer from '@/components/shared/Footer'
import AdminManagementAdminsTable from '@/components/admin-management/admins/AdminManagementAdminsTable'

const AdminManagementAdmins = () => {
    return (
        <>
            <PageHeader>
            </PageHeader>
            <div className='main-content'>
                <div className='row'>
                    <AdminManagementAdminsTable />
                </div>
            </div>
            <Footer />
        </>
    )
}

export default AdminManagementAdmins