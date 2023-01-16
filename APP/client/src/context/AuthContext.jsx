import { createContext, useState, useEffect} from 'react';
import {useHistory} from 'react-router-dom';

import jwt_decode from 'jwt-decode';

const AuthContext = createContext();

export default AuthContext;


export const AuthProvider = ({children}) =>{
    let authExists = localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null;
    let userExists = localStorage.getItem('authTokens') ? jwt_decode(localStorage.getItem('authTokens')) : null;
    let [authTokens, setAuthTokens] = useState(()=>authExists);
    let [user, setUser] = useState(()=>userExists);
    let [loggedUser, setLoggedUser] = useState(null);
    let [loading, setLoading] = useState(true);

    const history = useHistory();

    let loginUser = async(e) =>{
        e.preventDefault();
        const url = '/auth/token';
        var formData = new FormData();
        formData.append("username",e.target.email.value.toString());
        formData.append("password",e.target.password.value.toString());
        try{
            const response = await fetch(url,{
                method:'POST',
                body: formData,
            })
            let data = await response.json();

            if (response.status === 200){
                setAuthTokens(data.token);
                setUser(jwt_decode(data.token));
                localStorage.setItem('authTokens',JSON.stringify(data.token));
                // get the user role
                const urlUser = '/auth/me';
                let res = await fetch(urlUser,{
                    method: 'GET',
                    headers:{
                        'Content-type':'application/json',
                        'Authorization': 'Bearer '+String(data.token)
                    }
                });
                let dat = await res.json();
                if(res.status===200){
                    setLoggedUser(dat);
                    history.push('/dashboard');
                }else{
                    setLoggedUser(null);
                    console.log('Something Went Wrong')
                    history.push('/login')
                }
            }else{
                console.log('Something Went Wrong')
            }
        } catch(err){
            setAuthTokens(null);
            setUser(null);
            localStorage.removeItem('authTokens');
        }
        
    }

    let registerUser = async(e)=>{
        e.preventDefault();
        const url = '/auth/register';
        let response = await fetch(url,{
            method:"POST",
            headers: {
                "Content-type":"application/json"
            },
            body: JSON.stringify({
                "email":e.target.email.value,
                "company":e.target.company.value,
                "password":e.target.password.value
            }),
        });
        let data = await response.json();

        if(response.status===200){
            setAuthTokens(data.token);
            setUser(jwt_decode(data.token));
            localStorage.setItem('authTokens',JSON.stringify(data.token));
            // get the user role
            const urlUser = '/auth/me';
            let res = await fetch(urlUser,{
                method: 'GET',
                headers:{
                    'Content-type':'application/json',
                    'Authorization': 'Bearer '+String(data.token)
                }
            });
            let dat = await res.json();
            if(res.status === 200){
                setLoggedUser(dat);
                history.push("/dashboard")
            }else{
                setLoggedUser(null);
                console.log("Something went wrong");
                history.push('/login')
            }
        }else{
            console.log('Something Went Wrong, Please Try Again Later')
        }
    };

    let loggedInUser = async()=>{
        const url = '/auth/me';
        let response = await fetch(url,{
            method: 'GET',
            headers:{
                'Content-type':'application/json',
                'Authorization': 'Bearer '+String(authTokens)
            }
        });
        let data = await response.json();
        if(response.status === 200){
            setLoggedUser(data);
        }else{
            setLoggedUser(null)
        }
    }

    let logOut = () => {
        setAuthTokens(null);
        setUser(null);
        localStorage.removeItem('authTokens');
        history.push('/login')
    }

    let checkTokenValidation = async()=>{
        const tok = localStorage.getItem('authTokens');
        const decodedToken = jwt_decode(tok);
        
        if(!decodedToken.email){
            logOut();
        }
        if(loading){
            setLoading(false);
        }
    }


    useEffect(()=>{
        if(loading){
            checkTokenValidation();
        }
    },[authTokens, loading])

    let contextData = {
        user,
        authTokens,
        loginUser:loginUser,
        registerUser:registerUser,
        logOut:logOut,
        loggedInUser:loggedInUser,
        loggedUser:loggedUser,
    }

    return (
        <AuthContext.Provider value={contextData}>
            {children}
        </AuthContext.Provider>
    )
}