import React, { useContext } from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";

import Navigation from "./components/layout/Navigation";
import About from "./components/pages/About";
import Search from "./components/pages/Search";
import Add from "./components/pages/Add";
import UserInfo from "./components/pages/UserInfo";

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
            <Route path="/add" component={Add} />
            <Route path="/about" component={About} /> 
            <Route path="/userinfo" component={UserInfo}/>           
          </div>
        </div>
      </Router>
    </AuthContextProvider>
  );
};

export default App;
