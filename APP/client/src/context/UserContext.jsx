import React, {useState, useEffect,createContext} from 'react';

export const UserContext = createContext();

export const UserProvider = (props) =>{
    const [token, setToken] = useState(localStorage.getItem("auth-token"));
    const [loading, setLoading] = useState(true);

    useEffect(()=>{
        const fetchUser = async ()=>{
            const requestOptions = {
                method:"GET",
                headers:{
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token,
                },
            };
            const response = await fetch('/auth/me',requestOptions);
            if(!response.ok){
                setToken(null);
            }
            localStorage.setItem("auth-token",token);
            // if(loading){
            //     setLoading(false);
            // }
        };
        if(loading){
            fetchUser();
        }
    },[token, loading]);
    return (
        <UserContext.Provider value={[token, setToken]}>
            {props.children}
        </UserContext.Provider>
    )
}