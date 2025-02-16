import { createBrowserRouter, Navigate } from "react-router-dom";
import RootLayout from "../layout/root";
import Home from "../pages/home";
import Analytics from "../pages/analytics";
import ReportsSales from "../pages/reports-sales";
import ReportsLeads from "../pages/reports-leads";
import ReportsProject from "../pages/reports-project";
import AppsChat from "../pages/apps-chat";
import LayoutApplications from "../layout/layoutApplications";
import AppsEmail from "../pages/apps-email";
import ReportsTimesheets from "../pages/reports-timesheets";
import LoginCover from "../pages/login-cover";
import AppsTasks from "../pages/apps-tasks";
import AppsNotes from "../pages/apps-notes";
import AppsCalender from "../pages/apps-calender";
import AppsStorage from "../pages/apps-storage";
import Proposalist from "../pages/proposal-list";
import CustomersList from "../pages/customers-list";
import ProposalView from "../pages/proposal-view";
import ProposalEdit from "../pages/proposal-edit";
import LeadsList from "../pages/leadsList";
import CustomersView from "../pages/customers-view";
import CustomersCreate from "../pages/customers-create";
import ProposalCreate from "../pages/proposal-create";
import LeadsView from "../pages/leads-view";
import LeadsCreate from "../pages/leads-create";
import PaymentList from "../pages/payment-list";
import PaymentView from "../pages/payment-view/";
import PaymentCreate from "../pages/payment-create";
import ProjectsList from "../pages/projects-list";
import ProjectsView from "../pages/projects-view";
import ProjectsCreate from "../pages/projects-create";
import SettingsGaneral from "../pages/settings-ganeral";
import LayoutSetting from "../layout/layoutSetting";
import SettingsSeo from "../pages/settings-seo";
import SettingsTags from "../pages/settings-tags";
import SettingsEmail from "../pages/settings-email";
import SettingsTasks from "../pages/settings-tasks";
import SettingsLeads from "../pages/settings-leads";
import SettingsMiscellaneous from "../pages/settings-miscellaneous";
import SettingsRecaptcha from "../pages/settings-recaptcha";
import SettingsLocalization from "../pages/settings-localization";
import SettingsCustomers from "../pages/settings-customers";
import SettingsGateways from "../pages/settings-gateways";
import SettingsFinance from "../pages/settings-finance";
import SettingsSupport from "../pages/settings-support";
import LayoutAuth from "../layout/layoutAuth";
import LoginMinimal from "../pages/login-minimal";
import LoginCreative from "../pages/login-creative";
import RegisterCover from "../pages/register-cover";
import RegisterMinimal from "../pages/register-minimal";
import RegisterCreative from "../pages/register-creative";
import ResetCover from "../pages/reset-cover";
import ResetMinimal from "../pages/reset-minimal";
import ResetCreative from "../pages/reset-creative";
import ErrorCover from "../pages/error-cover";
import ErrorCreative from "../pages/error-creative";
import ErrorMinimal from "../pages/error-minimal";
import OtpCover from "../pages/otp-cover";
import OtpMinimal from "../pages/otp-minimal";
import OtpCreative from "../pages/otp-creative";
import MaintenanceCover from "../pages/maintenance-cover";
import MaintenanceMinimal from "../pages/maintenance-minimal";
import MaintenanceCreative from "../pages/maintenance-creative";
import HelpKnowledgebase from "../pages/help-knowledgebase";
import WidgetsLists from "../pages/widgets-lists";
import WidgetsTables from "../pages/widgets-tables";
import WidgetsCharts from "../pages/widgets-charts";
import WidgetsStatistics from "../pages/widgets-statistics";
import WidgetsMiscellaneous from "../pages/widgets-miscellaneous";
import RequireAuth from '../components/RequireAuth';
import Cookies from 'js-cookie';
import ProductCategory from "../pages/product-category";
import ProductCategoryCreate from "@/components/products/category/ProductCategoryCreate";
import ProductCategoryUpdate from "@/components/products/category/ProductCategoryUpdate";
import AdminManagementPositions from "../pages/admin-management-positions";
import AdminManagementPositionsCreate from "@/components/admin-management/positions/AdminManagementPositionsCreate";
import AdminManagementPositionsUpdate from "@/components/admin-management/positions/AdminManagementPositionsUpdate";
import AdminManagementAdmins from "../pages/admin-management-admins";
import AdminManagementAdminsOperation from "@/components/admin-management/admins/AdminManagementAdminsOperation";
import AccessError from "../pages/access-error";
import ProductBrandCreate from "@/components/products/brand/ProductBrandCreate";
import ProductBrandUpdate from "@/components/products/brand/ProductBrandUpdate";
import ProductBrand from "../pages/product-brand";
import ProductFlavour from "../pages/product-flavour";
import ProductFlavourCreate from "@/components/products/flavour/ProductFlavourCreate";
import ProductFlavourUpdate from "@/components/products/flavour/ProductFlavourUpdate";
import ProductSKU from "../pages/product-sku";
import Product from "../pages/product";
import ProductCreate from "@/components/products/product/ProductCreate";
import ProductUpdate from "@/components/products/product/ProductUpdate";
import ProductSKUCreate from "@/components/products/sku/ProductSKUCreate";
import ProductSKUUpdate from "@/components/products/sku/ProductSKUUpdate";
import ProductSKUTable from "@/components/products/sku/ProductSKUTable";
import ProductImageCreate from "@/components/products/image/ProductImageCreate";
import ProductImage from "../pages/product-image";
import ProductImageUpdate from "@/components/products/image/ProductImageUpdate";
import AdminManagementPermissions from "../pages/admin-management-permissions";
import AdminManagementPermissionsUpdate from "@/components/admin-management/permissions/AdminManagementPermissionsUpdate";


const parseJwt = (token) => {
    try {
        const base64Url = token.split('.')[1]; // Get payload
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/'); // Fix URL-safe characters
        const jsonPayload = decodeURIComponent(atob(base64).split('').map((c) =>
            '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
        ).join(''));

        return JSON.parse(jsonPayload);
    } catch (error) {
        return null; // Invalid token
    }
};

const PublicRoute = ({ children }) => {
    const authToken = Cookies.get('accessToken');

    if (authToken) {
        const decodedToken = parseJwt(authToken);

        if (decodedToken && decodedToken.exp * 1000 > Date.now()) {
            // Token exists & is valid -> Redirect to home
            return <Navigate to="/" replace />;
        } else {
            // Token expired -> Remove it
            Cookies.remove('accessToken');
            Cookies.remove('refreshToken');
            Cookies.remove('username');
        }
    }
    return children;
};

// Error boundary component to catch 403 errors
const ErrorBoundary = ({ error }) => {
    if (error.status === 403) {
        return <Navigate to="/403" replace />;
    }
    return null;
};

export const router = createBrowserRouter([
    {
        path: "/",
        element: <RequireAuth><RootLayout /></RequireAuth>,
        children: [
            {
                path: "/",
                element: <Home />
            },
            {
                path: "/dashboards/analytics",
                element: <Analytics />
            },
            {
                path: "/reports/sales",
                element: <ReportsSales />
            },
            {
                path: "/reports/leads",
                element: <ReportsLeads />
            },
            {
                path: "/reports/project",
                element: <ReportsProject />
            },
            {
                path: "/reports/timesheets",
                element: <ReportsTimesheets />
            },
            {
                path: "/proposal/list",
                element: <Proposalist />
            },
            {
                path: "/proposal/view",
                element: <ProposalView />
            },
            {
                path: "/proposal/edit",
                element: <ProposalEdit />
            },
            {
                path: "/proposal/create",
                element: <ProposalCreate />
            },
            {
                path: "/payment/list",
                element: <PaymentList />
            },
            {
                path: "/payment/view",
                element: <PaymentView />
            },
            {
                path: "/payment/create",
                element: <PaymentCreate />
            },
            {
                path: "/customers/list",
                element: <CustomersList />
            },
            {
                path: "/profile/details",
                element: <CustomersView />
            },
            {
                path: "/customers/create",
                element: <CustomersCreate />
            },
            {
                path: "/leads/list",
                element: <LeadsList />
            },
            {
                path: "/leads/view",
                element: <LeadsView />
            },
            {
                path: "/leads/create",
                element: <LeadsCreate />
            },
            {
                path: "/projects/list",
                element: <ProjectsList />
            },
            {
                path: "/projects/view",
                element: <ProjectsView />
            },
            {
                path: "/projects/create",
                element: <ProjectsCreate />
            },
            {
                path: "/widgets/lists",
                element: <WidgetsLists />
            },
            {
                path: "/widgets/tables",
                element: <WidgetsTables />
            },
            {
                path: "/widgets/charts",
                element: <WidgetsCharts />
            },
            {
                path: "/widgets/statistics",
                element: <WidgetsStatistics />
            },
            {
                path: "/widgets/miscellaneous",
                element: <WidgetsMiscellaneous />
            },
            {
                path: "/help/knowledgebase",
                element: <HelpKnowledgebase />
            },
            {
                path: "/products",
                element: <Product />
            },
            {
                path: "/products/create",
                element: <ProductCreate />
            },
            {
                path: "/products/:id",
                element: <ProductUpdate />
            },
            {
                path: "/products/sku",
                element: <ProductSKUTable />
            },
            {
                path: "/products/sku/create/:product_id",
                element: <ProductSKUCreate />
            },
            {
                path: "/products/sku/:product_id",
                element: <ProductSKU />
            },
            {
                path: "/products/sku/:product_id/:id",
                element: <ProductSKUUpdate />
            },
            {
                path: "/products/image",
                element: <ProductImage />
            },
            {
                path: "/products/image/:id",
                element: <ProductImageUpdate />
            },
            {
                path: "/products/image/:id/create",
                element: <ProductImageCreate />
            },
            {
                path: "/products/category",
                element: <ProductCategory />
            },
            {
                path: "/products/category/create",
                element: <ProductCategoryCreate />
            },
            {
                path: "/products/category/:id",
                element: <ProductCategoryUpdate />
            },
            {
                path: "/products/brand",
                element: <ProductBrand />
            },
            {
                path: "/products/brand/create",
                element: <ProductBrandCreate />
            },
            {
                path: "/products/brand/:id",
                element: <ProductBrandUpdate />
            },
            {
                path: "/products/flavour",
                element: <ProductFlavour />
            },
            {
                path: "/products/flavour/create",
                element: <ProductFlavourCreate />
            },
            {
                path: "/products/flavour/:id",
                element: <ProductFlavourUpdate />
            },
            {
                path: "/admin-management/positions",
                element: <AdminManagementPositions />
            },
            {
                path: "/admin-management/positions/create",
                element: <AdminManagementPositionsCreate />
            },
            {
                path: "/admin-management/positions/:id",
                element: <AdminManagementPositionsUpdate />
            },
            {
                path: "/admin-management/role-permissions",
                element: <AdminManagementPermissions />
            },
            {
                path: "/admin-management/role-permissions/:id",
                element: <AdminManagementPermissionsUpdate />
            },
            {
                path: "/admin-management/admins",
                element: <AdminManagementAdmins />
            },
            {
                path: "/admin-management/admins/:admin_user_name",
                element: <AdminManagementAdminsOperation />
            },
            {
                path: "/403",
                element: <AccessError />
            }

        ],
        errorElement: <ErrorBoundary /> // Use error boundary for 403 handling
    },
    {
        path: "/",
        element: <RequireAuth><LayoutApplications /></RequireAuth>,
        children: [
            {
                path: "/applications/chat",
                element: <AppsChat />
            },
            {
                path: "/applications/email",
                element: <AppsEmail />
            },
            {
                path: "/applications/tasks",
                element: <AppsTasks />
            },
            {
                path: "/applications/notes",
                element: <AppsNotes />
            },
            {
                path: "/applications/calender",
                element: <AppsCalender />
            },
            {
                path: "/applications/storage",
                element: <AppsStorage />
            }
        ]
    },
    {
        path: "/",
        element: <RequireAuth><LayoutSetting /></RequireAuth>,
        children: [
            {
                path: "/settings/ganeral",
                element: <SettingsGaneral />
            },
            {
                path: "/settings/seo",
                element: <SettingsSeo />
            },
            {
                path: "/settings/tags",
                element: <SettingsTags />
            },
            {
                path: "/settings/email",
                element: <SettingsEmail />
            },
            {
                path: "/settings/tasks",
                element: <SettingsTasks />
            },
            {
                path: "/settings/leads",
                element: <SettingsLeads />
            },
            {
                path: "/settings/Support",
                element: <SettingsSupport />
            },
            {
                path: "/settings/finance",
                element: <SettingsFinance />
            },
            {
                path: "/settings/gateways",
                element: <SettingsGateways />
            },
            {
                path: "/settings/customers",
                element: <SettingsCustomers />
            },
            {
                path: "/settings/localization",
                element: <SettingsLocalization />
            },
            {
                path: "/settings/recaptcha",
                element: <SettingsRecaptcha />
            },
            {
                path: "/settings/miscellaneous",
                element: <SettingsMiscellaneous />
            },
        ]
    },
    {
        path: "/",
        element: <LayoutAuth />,
        children: [
            {
                path: "/authentication/login/minimal",
                element: <PublicRoute><LoginMinimal /></PublicRoute>
            },
            {
                path: "/authentication/register/minimal",
                element: <PublicRoute><RegisterMinimal /></PublicRoute>
            },
            {
                path: "/authentication/reset/minimal",
                element: <ResetMinimal />
            },
            {
                path: "/authentication/404/minimal",
                element: <ErrorMinimal />
            },
            {
                path: "/authentication/verify/minimal",
                element: <OtpMinimal />
            },
            {
                path: "/authentication/maintenance/minimal",
                element: <MaintenanceMinimal />
            },
        ]
    },
    // Catch-all route for 404
    {
        path: "*",
        element: <ErrorMinimal />, // This component should render your 404 page
    },
])