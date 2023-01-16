import React, {useEffect, useState, useContext} from 'react';
import { UserContext } from '../context/UserContext';
import ErrorMessage from "./ErrorMessage";

const Account = () => {
    const [email, setEmail] = useState("");
    const [company, setCompany] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const [, setToken] = useContext(UserContext);
    const [token] = useContext(UserContext)
    const [user, setUser] = useState(null);

    let fetchUser = async () => {
        const requestOptions = {
            method:"GET",
            headers: {"Authorization":"Bearer "+token}
        }
        const response= await fetch('/auth/me', requestOptions);
        const response_data = await response.json();

        if(!response.ok){
            setErrorMessage(response.detail);
        }else{
            setUser(response_data);
        }
    };

    const submitUpdate = async () => {
        const requestOptions = {
          method: "PUT",
          headers: { 
            "Content-Type": "application/json",
            "Authorization": "Bearer "+token,
         },
          body: JSON.stringify({ email: email, company:company}),
        };
        // console.log(user)
    
        const response = await fetch("/auth/users/"+user.id, requestOptions);
        const data = await response.json();
    
        if (!response.ok) {
          setErrorMessage(data.message);
        } else {
          setToken(data.token);
          setEmail("");
          setCompany(""); 
          setErrorMessage("")
        }
      };
    
      const handleSubmit = (e) => {
        e.preventDefault();
        submitUpdate();
      };

    const generateNewToken = async () =>{
        const requestOptions = {
            method: "GET",
            headers: { 
              "Content-Type": "application/json",
              "Authorization": "Bearer "+token,
            }
        };
        const response = await fetch("/auth/token/update", requestOptions);
        const data = await response.json();
    
        if (!response.ok) {
          setErrorMessage(data.message);
        } else {
          setToken(data.token);
          setEmail("");
          setCompany(""); 
          setErrorMessage("")
        }
    }
    useEffect(()=>{
        fetchUser()
    },[user]);
    // window.onload(()=>fetchUser())
    return (
        <div className='container p-5'>
            <h2>Account</h2>
            <div className="mx-3 my-4 p-4 border rounded-2 bg-light">
                <h3>Personal Details</h3>
                <form className="container px-3 pt-1" onSubmit={handleSubmit}>
                    <div className="form-group pb-1">
                        <label className="">Email Address</label>
                        <div className="control">
                            <input
                            type="email"
                            placeholder="Enter email"
                            value={user?user.email:""}
                            onChange={(e) => setEmail(e.target.value)}
                            className="form-control"
                            required
                            />
                        </div>
                    </div>
                    <div className="form-group pb-2">
                        <label className="">Company</label>
                        <div className="control">
                            <input
                            type="text"
                            placeholder="Enter Company Name"
                            value={user?user.company:""}
                            onChange={(e) => setCompany(e.target.value)}
                            className="form-control"
                            required
                            />
                        </div>
                    </div>
                    <ErrorMessage message={errorMessage} />
                    <div className="w-100">
                        <button className="btn btn-md btn-primary rounded-0 px-5" type="submit">
                        Change Profile
                        </button>
                    </div>
                </form>
            </div>
            <div className="mx-3 my-4 p-4 border rounded-2 bg-light">
                <h3>Token</h3>
                <div className="px-3">
                    <pre className='border p-2 rounded-1 bg-white'><code className="language-css">{user?user.token:""}</code></pre>
                    <div className="w-100">
                        <button className="btn btn-md btn-primary rounded-0 px-5" type="button" onClick={()=>generateNewToken()}>
                        Generate New Token
                        </button>
                    </div>
                </div>
            </div>
            <div className="mx-3 my-4 p-5 border rounded-2 bg-light">
                hellpo
            </div>
        </div>
    )
}

export default Account