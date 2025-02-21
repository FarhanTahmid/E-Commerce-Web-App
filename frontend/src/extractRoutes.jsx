import { router } from "./router"; // Import your router config

const extractRoutes = (routes) => {
    let allRoutes = [];

    const traverseRoutes = (routes) => {
        routes.forEach((route) => {
            if (route.element?.props?.pageName) {
                allRoutes.push({ path: route.path, pageName: route.element.props.pageName });
            }
            if (route.children) {
                traverseRoutes(route.children);
            }
        });
    };

    traverseRoutes(routes.routes); // Access `routes` inside the router

    return allRoutes;
};

const allRoutes = extractRoutes(router);

export default allRoutes;
