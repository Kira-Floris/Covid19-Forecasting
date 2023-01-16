import React from 'react'
import {Redirect} from 'react-router-dom'

function Logout() {
    localStorage.setItem("auth-token",null)
    return <Redirect to="/login"/>
}

export default Logout