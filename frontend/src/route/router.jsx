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
import ProductCategoryCreate from "@/components/products/ProductCategoryCreate";
import ProductCategoryUpdate from "@/components/products/ProductCategoryUpdate";

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
                path: "/customers/view",
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
                path: "/products/category",
                element: <ProductCategory />
            },
            {
                path: "/products/category/create",
                element: <ProductCategoryCreate />
            },
            {
                path: "/product-category/:id",
                element: <ProductCategoryUpdate />
            }

        ]
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