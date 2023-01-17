import React from 'react';
import { useContext, useState } from 'react';
import {BrowserRouter as Router, Switch, Route, Link} from "react-router-dom";

import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Register from './components/Register';
import Login from './components/Login';
import { Dashboard } from './components/Dashboard';
import Documentation from './components/Documentation';
import Account from './components/Account';
import AuthContext, {AuthProvider} from './context/AuthContext';
import PrivateRoute from './utils/PrivateRoute';


function App() {
  const [message, setMessage] = useState("");
  return (
    <Router>
      <AuthProvider>
          <Navbar/>

          <Route path="/" exact>here</Route>
          <Route path="/register" exact><Register/></Route>
          <Route path="/login" exact><Login/></Route>
          <Route path="/documentation" exact><Documentation/></Route>
          <PrivateRoute component={Dashboard} path="/dashboard" exact/>
          <PrivateRoute component={Account} path="/account" exact/>
          <Footer/>
      </AuthProvider>
    </Router>
  );
}

export default App;
