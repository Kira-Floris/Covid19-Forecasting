import React, {useEffect, useState, useContext} from 'react';
import AuthContext from '../context/AuthContext';
import ErrorMessage from "./ErrorMessage";

let object = {
    email:"",
    company:"",
}

const Account = () => {
    let {user, authTokens, loggedUser, generateNewToken} = useContext(AuthContext);
    let [person, setPerson] = useState({object});
    let [errorMessage, setErrorMessage] = useState("");

    let fetchUser = async () =>{
        let response = await fetch('/auth/me',{
            method:"GET",
            headers:{"Authorization":"Bearer "+String(authTokens)},
        });
        let data = await response.json()
        if (response.status===200){
            return data;
        }else{
            return null
        }
    }
    
    let getUser = async () =>{
        var temp = await fetchUser();
        setPerson({
            ...person,
            ["email"]:temp.email,
            ["company"]:temp.company,
        })
    }
    
    let handleChange=(e)=>{
        var name = e.target.name;
        var value = e.target.value;
        setPerson({
          ...person,
          [name]:value,
        });
    };

    let handleSubmit = async(e)=>{
        e.preventDefault();
        var temp = await fetchUser();
        let response = await fetch('/auth/users/'+temp.id,{
            method: "PUT",
            headers: {
                "Content-Type":"application/json",
                "Authorization":"Bearer "+String(authTokens)
            },
            body:JSON.stringify({"email":person.email,"company":person.company})
        });
        if(response.status===200){
            console.log('Success')
        }else{
            console.log("Something Went Wrong")
        }
    }

    let handlePassword = async(e)=>{
        e.preventDefault();
        let response = await fetch('/auth/reset',{
            method: "PUT",
            headers: {
                "Content-Type":"application/json",
                "Authorization":"Bearer "+String(authTokens)
            },
            body:JSON.stringify({"old_password":e.target.old_password.value,"new_password":e.target.new_password.value})
        });
        if(response.status===200){
            console.log('Updated Successfully');
        }else{
            console.log("Something Went Wrong")
        }
    }

    useEffect(()=>{
        getUser()
    },[])
    return (
        <div className='container py-5 w-75'>
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
                            name="email"
                            value={person.email}
                            onChange={handleChange}
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
                            name="company"
                            value={person.company}
                            onChange={handleChange}
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
                    <pre className='border p-2 rounded-1 bg-white'><code className="language-css">{authTokens}</code></pre>
                    <div className="w-100">
                        <button className="btn btn-md btn-primary rounded-0 px-5" type="button" onClick={()=>generateNewToken()}>
                        Generate New Token
                        </button>
                    </div>
                </div>
            </div>
            <div className="mx-3 my-4 p-5 border rounded-2 bg-light">
                <h3>Update Password</h3>
                <form className="container px-3 pt-1" onSubmit={handlePassword}>
                    <div className="form-group pb-1">
                        <label className="">Old Password</label>
                        <div className="control">
                            <input
                            type="password"
                            placeholder="Enter your old password"
                            name="old_password"
                            className="form-control"
                            required
                            />
                        </div>
                    </div>
                    <div className="form-group pb-2">
                        <label className="">New Password</label>
                        <div className="control">
                            <input
                            type="password"
                            placeholder="Enter new password"
                            name="new_password"
                            className="form-control"
                            required
                            />
                        </div>
                    </div>
                    <ErrorMessage message={errorMessage} />
                    <div className="w-100">
                        <button className="btn btn-md btn-primary rounded-0 px-5" type="submit">
                        Update Password
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}

export default Account