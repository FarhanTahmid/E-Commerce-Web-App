import React from 'react'
import PageHeader from '@/components/shared/pageHeader/PageHeader'
import Footer from '@/components/shared/Footer'
import AdminManagementPositionsTable from '@/components/admin-management/AdminManagementPositionsTable'
import AdminManagementPositionsHeader from '@/components/admin-management/AdminManagementPositionsHeader'

const AdminManagementPositions = () => {
    return (
        <>
            <PageHeader>
                <AdminManagementPositionsHeader />
            </PageHeader>
            <div className='main-content'>
                <div className='row'>
                    <AdminManagementPositionsTable />
                </div>
            </div>
            <Footer />
        </>
    )
}

export default AdminManagementPositions