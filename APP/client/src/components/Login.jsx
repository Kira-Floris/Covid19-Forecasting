import React, { useState, useContext } from "react";
import {useHistory} from 'react-router-dom';

import ErrorMessage from "./ErrorMessage";
import AuthContext from "../context/AuthContext";

const Login = () => {
  let {loginUser} = useContext(AuthContext);
  let {logoutUser, user, authTokens} = useContext(AuthContext);
  const [errorMessage, setErrorMessage] = useState("");

  return (
    <div className="container d-flex justify-content-center align-items-center w-md-50 w-50">
      <form className="container px-5 pt-3" onSubmit={loginUser}>
        <h1 className="pb-3 text-center">Login</h1>
        <div className="form-group">
          <label className="label">Email Address</label>
          <div className="control">
            <input
              type="email"
              placeholder="Enter email"
              name="email"
              className="form-control"
              required
            />
          </div>
        </div>
        <div className="field">
          <label className="label">Password</label>
          <div className="control">
            <input
              type="password"
              placeholder="Enter password"
              name="password"
              className="form-control"
              required
            />
          </div>
        </div>
        <ErrorMessage message={errorMessage} />
        <br />
        <div className="d-flex justify-content-center w-100">
            <button className="btn btn-lg btn-primary rounded-0 px-5" type="submit">
            Login
            </button>
        </div>
      </form>
    </div>
  );
};

export default Login;