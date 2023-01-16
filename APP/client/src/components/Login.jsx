import React, { useState, useContext } from "react";
import {useHistory} from 'react-router-dom';

import ErrorMessage from "./ErrorMessage";
import { UserContext } from "../context/UserContext";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [, setToken] = useContext(UserContext);
  const history = useHistory();

  const submitLogin = async () => {
    var formData = new FormData();
    formData.append("username", email);
    formData.append("password", password);
    const requestOptions = {
      method: "POST",
      body: formData
    };

    const response = await fetch("/auth/token", requestOptions);
    const data = await response.json();

    if (!response.ok) {
      setErrorMessage(data.message);
    } else {
      setToken(data.token);
      history.push('/dashboard');
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    submitLogin();
  };

  return (
    <div className="container d-flex justify-content-center align-items-center w-md-50 w-50">
      <form className="container px-5 pt-3" onSubmit={handleSubmit}>
        <h1 className="pb-3 text-center">Login</h1>
        <div className="form-group">
          <label className="label">Email Address</label>
          <div className="control">
            <input
              type="email"
              placeholder="Enter email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
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
              value={password}
              onChange={(e) => setPassword(e.target.value)}
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