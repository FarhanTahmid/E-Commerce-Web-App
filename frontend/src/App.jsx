import React from 'react'
import { RouterProvider } from 'react-router-dom'
import { router } from './route/router'
import 'react-quill/dist/quill.snow.css';
import 'react-circular-progressbar/dist/styles.css';
import "react-perfect-scrollbar/dist/css/styles.css";
import "react-datepicker/dist/react-datepicker.css";
import "react-datetime/css/react-datetime.css";
import NavigationProvider from './contentApi/navigationProvider';
import SideBarToggleProvider from './contentApi/sideBarToggleProvider';
import SendRoutes from './SendRoutes';

const App = () => {
  return (
    <>
      <SendRoutes />
      <NavigationProvider>
        <SideBarToggleProvider>
          <RouterProvider router={router} />
        </SideBarToggleProvider>
      </NavigationProvider>
    </>
  )
}

export default App