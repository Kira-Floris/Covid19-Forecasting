import React, {useContext, useState} from 'react';
import {Route, Redirect} from 'react-router-dom';

import { UserContext } from '../context/UserContext';

export const PrivateRoute = ({children, ...rest}) => {
    const [token] = useContext(UserContext); 
    return (
        <Route {...rest}>
            {!token?<Redirect to="/login"/>:children}
        </Route>
    )
}
