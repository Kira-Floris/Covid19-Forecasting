import React, {useContext, useState, useEffect} from 'react';
import {Link} from 'react-router-dom';

import AuthContext from '../context/AuthContext';


export default function Navbar() {
    const {authTokens, loggedInUser, user, logOut} = useContext(AuthContext);
    const tokenExist = (localStorage.getItem('authTokens')!==null)?true:false;
    const [errorMessage, setErrorMessage] = useState("");
    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light shadow mb-4">
        <div className="container">
            <Link className="navbar-brand" href="#" style={{color:"#70E7B5", fontSize:"2rem", fontWeight:"bold"}}>FAOCS</Link>
            <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
                <span className="navbar-toggler-icon"></span>
            </button>
          <div className="collapse navbar-collapse mx-3" id="navbarText">
            <span className="me-auto"></span>
            <ul className="navbar-nav mb-2 mb-lg-0">
                <li className="nav-item h6">
                    <Link className="nav-link link-secondary" to="/">Home</Link>
                </li>
                <li className="nav-item h6">
                    <Link className="nav-link link-secondary" to="/">Documentation</Link>
                </li>
                <li className="nav-item h6">
                    <Link className="nav-link link-secondary" to="/dashboard">Dashboard</Link>
                </li>
                <li className="nav-item h6">
                    <Link className="nav-link link-secondary" to="/register">Register</Link>
                </li>
                {!(tokenExist)?
                    <li className="nav-item h6">
                        <Link className="nav-link link-secondary" to="/login">Login</Link>
                    </li>
                    :
                    <li className="nav-item dropdown h6">
                        <span className="nav-link dropdown-toggle border rounded-5 px-3" style={{backgroundColor:"#70E7B5", width:"fit-content"}} href="#" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            {user?user.email:'Profile'}
                        </span>
                        <ul className="dropdown-menu px-3" aria-labelledby="navbarDropdownMenuLink">
                            <li>
                                <Link className="nav-link link-secondary" to="/account">Account</Link>
                            </li>
                            <li>
                                <Link className="nav-link link-secondary" to="/login" onClick={()=>logOut()}>Logout</Link>
                            </li>
                        </ul>
                    </li>
                }
            </ul>
          </div>
        </div>
      </nav>
    )
  }
  