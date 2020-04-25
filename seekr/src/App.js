import React, { useContext } from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";

import Navigation from "./components/layout/Navigation";
import About from "./components/pages/About";
import Search from "./components/pages/Search";
import Add from "./components/pages/Add";
import UserInfo from "./components/pages/UserInfo";
import Login from "./components/pages/Login";
import Logout from "./components/pages/Logout";
import Facebook from './components/Users/Facebook';
import Errorpage from './components/pages/Errorpage';
import ProtectedRoute from './ProtectedRoute'


import "./App.css";
import { AuthContext, AuthContextProvider } from "./components/helper/AuthContext";
//<Facebook parentCallback={this.callbackFunction}/>

const App = () => {
  
  return (
    <AuthContextProvider>
      <Router>
        <div className="App">
          <Navigation />
          <Route exact path="/" component={Search} />
          <div className="site-container">
            <ProtectedRoute path="/add" user={false} component={Add} />
            <Route path="/about" component={About} />
            <Route path="/unauthorized" component={Errorpage}/>}
            {/* login should redirect if logged in */}
            <Route path="/login" component={Facebook}/>  
            
            {/* userinfo and logout should redirect if not logged in */}
            <Route path="/userinfo" component={UserInfo}/>  
            <Route path="/logout" component={Logout}/>  
          </div>
        </div>
      </Router>
    </AuthContextProvider>
  );
};

export default App;
