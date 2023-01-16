import React, { useContext, useState } from "react";

import { UserContext } from "../context/UserContext";
import ErrorMessage from "./ErrorMessage";

const Register = () => {
  const [email, setEmail] = useState("");
  const [company, setCompany] = useState("");
  const [password, setPassword] = useState("");
  const [confirmationPassword, setConfirmationPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [, setToken] = useContext(UserContext);

  const submitRegistration = async () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email, company:company, password: password }),
    };

    const response = await fetch("/auth/register", requestOptions);
    const data = await response.json();

    if (!response.ok) {
      setErrorMessage(data.message);
    } else {
      setToken(data.token);
      setEmail("");
      setCompany(""); 
      setPassword("");
      setConfirmationPassword("");
      setErrorMessage("")
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (password === confirmationPassword && password.length > 5) {
      submitRegistration();
    } else {
      setErrorMessage(
        "Ensure that the passwords match and greater than 5 characters"
      );
    }
  };

  return (
    <div className="container d-flex justify-content-center align-items-center w-md-50 w-50">
      <form className="container px-5 pt-3" onSubmit={handleSubmit}>
        <h1 className="pb-3 text-center">Register</h1>
        <div className="form-group">
          <label className="">Email Address</label>
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
        <div className="form-group">
          <label className="">Company</label>
          <div className="control">
            <input
              type="text"
              placeholder="Enter Company Name"
              value={company}
              onChange={(e) => setCompany(e.target.value)}
              className="form-control"
              required
            />
          </div>
        </div>
        <div className="form-group">
          <label className="">Password</label>
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
        <div className="form-group">
          <label className="">Confirm Password</label>
          <div className="control">
            <input
              type="password"
              placeholder="Enter password"
              value={confirmationPassword}
              onChange={(e) => setConfirmationPassword(e.target.value)}
              className="form-control"
              required
            />
          </div>
        </div>
        <ErrorMessage message={errorMessage} />
        <br />
        <div className="d-flex justify-content-center w-100">
            <button className="btn btn-lg btn-primary rounded-0 px-5" type="submit">
            Register
            </button>
        </div>
      </form>
    </div>
  );
};

export default Register;