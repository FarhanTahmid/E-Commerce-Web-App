import React, { Fragment, useEffect, useState } from "react";
import { FiChevronRight } from "react-icons/fi";
import { Link, useLocation } from "react-router-dom";
import getIcon from "@/utils/getIcon";

const Menus = () => {
    const [openDropdown, setOpenDropdown] = useState(null);
    const [openSubDropdown, setOpenSubDropdown] = useState(null);
    const [activeParent, setActiveParent] = useState("");
    const [activeChild, setActiveChild] = useState("");
    const pathName = useLocation().pathname;
    const menuList = [
        {
            id: 0,
            name: "dashboards",
            path: "#",
            icon: 'feather-airplay',
            dropdownMenu: [
                {
                    id: 1,
                    name: "CRM",
                    path: "/",
                    subdropdownMenu: false
                },
                {
                    id: 2,
                    name: "Analytics",
                    path: "/dashboards/analytics",
                    subdropdownMenu: false
                }
            ]
        },
        {
            id: 1,
            name: "products",
            path: "#",
            icon: 'feather-clipboard',
            dropdownMenu: [
                {
                    id: 1,
                    name: "Products",
                    path: "/products",
                    subdropdownMenu: false
                },
                {
                    id: 2,
                    name: "Categories",
                    path: "/products/category",
                    subdropdownMenu: false
                }
            ]
        },
        {
            id: 2,
            name: "Admin Management",
            path: "#",
            icon: 'feather-users',
            dropdownMenu: [
                {
                    id: 1,
                    name: "Positions",
                    path: "/admin-management/positions",
                    subdropdownMenu: false
                }
            ]
        }
    ]

    // const menuList = [
    //     {
    //         id: 0,
    //         name: "dashboards",
    //         path: "#",
    //         icon: 'feather-airplay',
    //         dropdownMenu: [
    //             {
    //                 id: 1,
    //                 name: "CRM",
    //                 path: "/",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 2,
    //                 name: "Analytics",
    //                 path: "/dashboards/analytics",
    //                 subdropdownMenu: false
    //             }
    //         ]
    //     },
    //     {
    //         id: 1,
    //         name: "reports",
    //         path: "#",
    //         icon: 'feather-cast',
    //         dropdownMenu: [
    //             {
    //                 id: 1,
    //                 name: "Sales Report",
    //                 path: "/reports/sales",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 2,
    //                 name: "Leads Report",
    //                 path: "/reports/leads",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 3,
    //                 name: "Project Report",
    //                 path: "/reports/project",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 4,
    //                 name: "Timesheets Report",
    //                 path: "/reports/timesheets",
    //                 subdropdownMenu: false
    //             },

    //         ]
    //     },
    //     {
    //         id: 2,
    //         name: "applications",
    //         path: '#',
    //         icon: 'feather-send',
    //         dropdownMenu: [
    //             {
    //                 id: 1,
    //                 name: "Chat",
    //                 path: "/applications/chat",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 2,
    //                 name: "Email",
    //                 path: "/applications/email",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 3,
    //                 name: "Tasks",
    //                 path: "/applications/tasks",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 4,
    //                 name: "Notes",
    //                 path: "/applications/notes",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 5,
    //                 name: "Storage",
    //                 path: "/applications/storage",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 6,
    //                 name: "Calender",
    //                 path: "/applications/calender",
    //                 subdropdownMenu: false
    //             },
    //         ]
    //     },
    //     {
    //         id: 3,
    //         name: "proposal",
    //         path: "#",
    //         icon: 'feather-sign',
    //         dropdownMenu: [
    //             {
    //                 id: 1,
    //                 name: "Proposal",
    //                 path: "/proposal/list",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 2,
    //                 name: "Proposal View",
    //                 path: "/proposal/view",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 3,
    //                 name: "Proposal Edit",
    //                 path: "/proposal/edit",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 4,
    //                 name: "Proposal Create",
    //                 path: "/proposal/create",
    //                 subdropdownMenu: false
    //             },

    //         ],
    //     },
    //     {
    //         id: 4,
    //         name: "payment",
    //         path: "#",
    //         icon: 'feather-dollar-sign',
    //         dropdownMenu: [
    //             {
    //                 id: 1,
    //                 name: "Payment",
    //                 path: "/payment/list",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 2,
    //                 name: "Invoice View",
    //                 path: "/payment/view",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 4,
    //                 name: "Invoice Create",
    //                 path: "/payment/create",
    //                 subdropdownMenu: false
    //             }
    //         ]
    //     },
    //     {
    //         id: 5,
    //         name: "customers",
    //         path: "#",
    //         icon: 'feather-users',
    //         dropdownMenu: [
    //             {
    //                 id: 1,
    //                 name: "Customers",
    //                 path: "/customers/list",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 2,
    //                 name: "Customers View",
    //                 path: "/customers/view",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 3,
    //                 name: "Customers Create",
    //                 path: "/customers/create",
    //                 subdropdownMenu: false
    //             }
    //         ]
    //     },
    //     {
    //         id: 6,
    //         name: "leads",
    //         path: "#",
    //         icon: 'feather-alert-circle',
    //         dropdownMenu: [
    //             {
    //                 id: 1,
    //                 name: "Leads",
    //                 path: "/leads/list",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 2,
    //                 name: "Leads View",
    //                 path: "/leads/view",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 3,
    //                 name: "Leads Create",
    //                 path: "/leads/create",
    //                 subdropdownMenu: false
    //             }
    //         ]
    //     },
    //     {
    //         id: 7,
    //         name: "projects",
    //         path: "#",
    //         icon: 'feather-briefcase',
    //         dropdownMenu: [
    //             {
    //                 id: 1,
    //                 name: "Projects",
    //                 path: "/projects/list",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 2,
    //                 name: "Projects View",
    //                 path: "/projects/view",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 3,
    //                 name: "Projects Create",
    //                 path: "/projects/create",
    //                 subdropdownMenu: false
    //             }
    //         ]
    //     },
    //     {
    //         id: 8,
    //         name: "widgets",
    //         path: "#",
    //         icon: 'feather-layout',
    //         dropdownMenu: [
    //             {
    //                 id: 1,
    //                 name: "Lists",
    //                 path: "/widgets/lists",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 2,
    //                 name: "Tables",
    //                 path: "/widgets/tables",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 3,
    //                 name: "Charts",
    //                 path: "/widgets/charts",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 4,
    //                 name: "Statistics",
    //                 path: "/widgets/statistics",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 5,
    //                 name: "Miscellaneous",
    //                 path: "/widgets/miscellaneous",
    //                 subdropdownMenu: false
    //             },
    //         ]
    //     },
    //     {
    //         id: 9,
    //         name: "settings",
    //         path: "#",
    //         icon: 'feather-settings',
    //         dropdownMenu: [
    //             {
    //                 id: 1,
    //                 name: "Ganeral",
    //                 path: "/settings/ganeral",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 2,
    //                 name: "SEO",
    //                 path: "/settings/seo",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 3,
    //                 name: "Tags",
    //                 path: "/settings/tags",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 4,
    //                 name: "Email",
    //                 path: "/settings/email",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 5,
    //                 name: "Tasks",
    //                 path: "/settings/tasks",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 6,
    //                 name: "Leads",
    //                 path: "/settings/leads",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 7,
    //                 name: "Support",
    //                 path: "/settings/Support",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 8,
    //                 name: "Finance",
    //                 path: "/settings/finance",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 9,
    //                 name: "Gateways",
    //                 path: "/settings/gateways",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 10,
    //                 name: "Customers",
    //                 path: "/settings/customers",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 11,
    //                 name: "Localization",
    //                 path: "/settings/localization",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 12,
    //                 name: "reCAPTCHA",
    //                 path: "/settings/recaptcha",
    //                 subdropdownMenu: false
    //             },
    //             {
    //                 id: 13,
    //                 name: "Miscellaneous",
    //                 path: "/settings/miscellaneous",
    //                 subdropdownMenu: false
    //             },
    //         ]
    //     }
    // ]



    const handleMainMenu = (e, name) => {
        if (openDropdown === name) {
            setOpenDropdown(null);
        } else {
            setOpenDropdown(name);
        }
    };

    const handleDropdownMenu = (e, name) => {
        e.stopPropagation();
        if (openSubDropdown === name) {
            setOpenSubDropdown(null);
        } else {
            setOpenSubDropdown(name);
        }
    };

    useEffect(() => {
        if (pathName !== "/") {
            const x = pathName.split("/");
            setActiveParent(x[1]);
            setActiveChild(x[2]);
            setOpenDropdown(x[1]);
            setOpenSubDropdown(x[2]);
        } else {
            setActiveParent("dashboards");
            setOpenDropdown("dashboards");
        }
    }, [pathName]);

    return (
        <>
            {menuList.map(({ dropdownMenu, id, name, path, icon }) => {
                return (
                    <li
                        key={id}
                        onClick={(e) => handleMainMenu(e, name)}
                        className={`nxl-item nxl-hasmenu ${activeParent === name ? "active nxl-trigger" : ""}`}
                    >
                        <Link to={path} className="nxl-link text-capitalize">
                            <span className="nxl-micon"> {getIcon(icon)} </span>
                            <span className="nxl-mtext" style={{ paddingLeft: "2.5px" }}>
                                {name}
                            </span>
                            <span className="nxl-arrow fs-16">
                                <FiChevronRight />
                            </span>
                        </Link>
                        <ul
                            className={`nxl-submenu ${openDropdown === name ? "nxl-menu-visible" : "nxl-menu-hidden"}`}
                        >
                            {dropdownMenu.map(({ id, name, path, subdropdownMenu }) => {
                                const x = name;
                                return (
                                    <Fragment key={id}>
                                        {subdropdownMenu.length ? (
                                            <li
                                                className={`nxl-item nxl-hasmenu ${activeChild === name ? "active" : ""
                                                    }`}
                                                onClick={(e) => handleDropdownMenu(e, x)}
                                            >
                                                <Link to={path} className={`nxl-link text-capitalize`}>
                                                    <span className="nxl-mtext">{name}</span>
                                                    <span className="nxl-arrow">
                                                        <i>
                                                            {" "}
                                                            <FiChevronRight />
                                                        </i>
                                                    </span>
                                                </Link>
                                                {subdropdownMenu.map(({ id, name, path }) => {
                                                    return (
                                                        <ul
                                                            key={id}
                                                            className={`nxl-submenu ${openSubDropdown === x
                                                                ? "nxl-menu-visible"
                                                                : "nxl-menu-hidden "
                                                                }`}
                                                        >
                                                            <li
                                                                className={`nxl-item ${pathName === path ? "active" : ""
                                                                    }`}
                                                            >
                                                                <Link
                                                                    className="nxl-link text-capitalize"
                                                                    to={path}
                                                                >
                                                                    {name}
                                                                </Link>
                                                            </li>
                                                        </ul>
                                                    );
                                                })}
                                            </li>
                                        ) : (
                                            <li
                                                className={`nxl-item ${pathName === path ? "active" : ""
                                                    }`}
                                            >
                                                <Link className="nxl-link" to={path}>
                                                    {name}
                                                </Link>
                                            </li>
                                        )}
                                    </Fragment>
                                );
                            })}
                        </ul>
                    </li>
                );
            })}
        </>
    );
};

export default Menus;
