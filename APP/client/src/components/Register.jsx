import React, { useContext, useState } from "react";

import AuthContext from "../context/AuthContext";
import ErrorMessage from "./ErrorMessage";

const Register = () => {
  let {registerUser} = useContext(AuthContext);
  const [errorMessage, setErrorMessage] = useState("");

  return (
    <div className="container d-flex justify-content-center align-items-center w-md-50 w-50">
      <form className="container px-5 pt-3" onSubmit={registerUser}>
        <h1 className="pb-3 text-center">Register</h1>
        <div className="form-group">
          <label className="">Email Address</label>
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
        <div className="form-group">
          <label className="">Company</label>
          <div className="control">
            <input
              type="text"
              placeholder="Enter Company Name"
              name="company"
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
            Register
            </button>
        </div>
      </form>
    </div>
  );
};

export default Register;