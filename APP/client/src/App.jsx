import React from 'react';
import { useContext, useState } from 'react';
import {BrowserRouter as Router, Switch, Route, Link} from "react-router-dom";

import Navbar from './components/Navbar';
import Register from './components/Register';
import Login from './components/Login';
import { Dashboard } from './components/Dashboard';
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
          <PrivateRoute component={Dashboard} path="/dashboard" exact/>
          <PrivateRoute component={Account} path="/account" exact/>
      </AuthProvider>
    </Router>
  );
}

export default App;
