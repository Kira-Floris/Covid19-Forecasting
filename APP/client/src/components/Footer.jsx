import React from 'react';
import {Link} from 'react-router-dom';

const Footer = () => {
  return (
    <div className="bg-light d-flex justify-content-center mt-4">
        <div className="row container px-5 py-3">
            <hr/>
            <div className="col-4">
                <p>
                    <b>© 2023 <span style={{color:"#70E7B5"}}>FAOCS</span>, Inc</b>
                </p>
            </div>
            <div className="col-8 text-end">
                <ul className="d-flex list-unstyled justify-content-end">
                    <li className="px-2">
                        <Link className="nav-link link-secondary" to="/">Home</Link>
                    </li>
                    <li className="px-2">
                        <Link className="nav-link link-secondary" to="/documentation">Documentation</Link>
                    </li>
                    <li className="px-2">
                        <Link className="nav-link link-secondary" to="/dashboard">Dashboard</Link>
                    </li>
                    <li className="pr-2">
                        <Link className="nav-link link-secondary" to="/register">Register</Link>
                    </li>
                </ul>
            </div>
        </div>
    </div>
  )
}

export default Footer