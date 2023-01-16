import React from 'react';
import { useContext, useState } from 'react';
import {BrowserRouter as Router, Switch, Route, Link} from "react-router-dom";

import Navbar from './components/Navbar';
import Register from './components/Register';
import Login from './components/Login';
import Logout from './components/Logout';
import { Dashboard } from './components/Dashboard';
import Account from './components/Account';
import { UserContext } from './context/UserContext';
import { PrivateRoute } from './utils/PrivateRoute';


function App() {
  const [message, setMessage] = useState("");
  const [token] = useContext(UserContext);
  return (
    <Router>
      <div>
        <Navbar/>
        <Switch>
          <Route path="/" exact>here</Route>
          <Route path="/register" exact><Register/></Route>
          <Route path="/login" exact><Login/></Route>
          <Route path="/logout" exact><Logout/></Route>
          <PrivateRoute component={Dashboard} path="/dashboard" exact/>
          <PrivateRoute component={Account} path="/account" exact/>
        </Switch>
      </div>
    </Router>
  );
}

export default App;
