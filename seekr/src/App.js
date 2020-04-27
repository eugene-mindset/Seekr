import React, { useContext } from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";

import Search from "./components/pages/Search";
import UserInfo from "./components/pages/UserInfo";
import Logout from "./components/pages/Logout";
import Facebook from './components/Users/Facebook';
import Errorpage from './components/pages/Errorpage';
import ProtectedRoute from './ProtectedRoute'
import Navigation from './components/layout/Navigation';
import Add from './components/pages/Add';


import "./App.css";
import { AuthContext, AuthContextProvider } from "./components/helper/AuthContext";

const App = () => {
  return (
    <AuthContextProvider>
      <Router>
        <div className="App">
          <Navigation />
          <Route exact path="/" component={Search} />
          <div className="site-container">

            {/* <ProtectedRoute path="/add" user={false} component={Add} /> */}
            <Route path="/unauthorized" component={Errorpage}/>
            {/* Temporarily using Login component instead of Facebook Component */}
            <Route path="/login" component={Facebook}/>  
            
            {/* userinfo and logout should redirect if not logged in */}
            <Route path="/userinfo" component={UserInfo}/>  
            <Route path="/logout" component={Logout}/>  
            <Route path="/add" component={Add} />
          </div>
        </div>
      </Router>
    </AuthContextProvider>
  );
};

export default App;
