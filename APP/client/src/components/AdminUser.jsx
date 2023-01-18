import React,{useContext,useState,useEffect} from 'react';
import AuthContext from '../context/AuthContext';

let object = {
    id:null,
    email:"",
    role:"",
    company:"",
    password:""
};

const AdminUser = () => {
    let {user, authTokens, logOut} = useContext(AuthContext);
    let [list, setList] = useState([]);
    let [activeItem, setActiveItem] = useState(object);
    let [editing, setEditing] = useState(false);

    let getCookie = (name)=>{
        var cookieValue = null;
        if(document.cookie && document.cookie !== ''){
          var cookies = document.cookie.split(";");
          for(var i=0; i<cookies.length; i++){
            var cookie = cookies[i].trim();
            if(cookie.substring(0, name.length+1)===(name+'=')){
              cookieValue = decodeURIComponent(cookie.substring(name.length+1));
              break;
            }
          }
        }
        return cookieValue;
    };

    let fetchList =async (e)=>{
        console.log("fetching...");
        var link = '/auth/users';
        let response = await fetch(link,{
          method: "GET",
          headers:{
            "Content-Type": "application/json",
            "Authorization": "Bearer " + String(authTokens),
          }
        } 
        );
        let data = await response.json();
        if(response.status === 200){
          setList(data.data);
        }else if(response.status===401){
          console.log('Failed');
        }
    };

    let handleChange=(e)=>{
        var name = e.target.name;
        var value = e.target.value;
        setActiveItem({
          ...activeItem,
          [name]:value
        });
    };

    let handleSubmit = async (e) =>{
        e.preventDefault();
        var url = "";
        var method = "";
        var csrftoken = getCookie("csrftoken");
        if(editing===true){
            var pk = activeItem.id;
            method = "PUT";
            var temp = "/".concat(pk);
            url = '/auth/users'.concat(temp);
            setEditing(false);
        }else{
            method = "POST";
            url = '/auth/register';
        }
        console.log(url)

        let response = await fetch(url,{
            method:method,
            headers:{
                "Content-Type":"application/json",
                "Authorization": "Bearer " + String(authTokens),
                "X-CSRFToken": csrftoken,
            },
            body:JSON.stringify(activeItem),
        });
        console.log(response);
        if(response.status===200){
            fetchList();
            setActiveItem(object);
            document.querySelector("#form").reset();
        }else{
            // toast.error(response.statusText)
        }
    };

    let startEdit=(task)=>{
        setActiveItem(task);
        setEditing(true);
    };

    let deleteItem=(task)=>{
        var crsftoken = getCookie("csrftoken");
        var pk = task.id;
        var url = '/auth/users'.concat("/").concat(pk);
        fetch(url,{
          method:"DELETE",
          headers: {
            "Content-type": "application/json",
            "Authorization": "Bearer " + String(authTokens),
            "X-CSRFToken": crsftoken,
          }
        }).then(response=>{
          fetchList();
        }).catch((error)=>{
            console.log(error)
        });
      };

    useEffect(()=>{
        fetchList();
    },[]);

    return (
        <div className="container py-4">
            <h1>Users</h1>
            <hr/>
            <form method="POST" className="me-md-5 px-2" id="form" onSubmit={handleSubmit}>
                <h2>User Form</h2>
                <div className="d-md-flex">
                    <div className="w-50">
                        <label>Email</label>
                        <input type="text" className="form-control my-1" placeholder="Email" onChange={handleChange} id="email" name="email" value={activeItem.email}/>
                    </div>
                    
                    <div className="w-50">
                        <label>Company</label>
                        <input type="text" className="form-control my-1" placeholder="Company" onChange={handleChange} id="company" name="company" value={activeItem.company}/>
                    </div>
                </div>
                <div className="d-md-flex">
                    <div className='w-50'>
                        <label>Role</label>
                        <input type="text" className="form-control my-1" placeholder="admin or user" onChange={handleChange} id="role" name="role" value={activeItem.role}/>
                    </div>
                    <div className='w-50'>
                        <label>Password</label>
                        <input type="password" className="form-control my-1" placeholder="Password" onChange={handleChange} id="password" name="password" value={activeItem.password}/>
                    </div>
                </div>
                <div className='w-50'>
                    <input type="submit" className="form-control my-1 btn btn-lg rounded-0 btn-primary" id="submit" placeholder="Submit"/>
                </div>
            </form>
            <br/>
            <hr/>
            <div>
                <h2>Users:</h2>
                <table className="table">
                    <thead>
                        <tr>
                            <th scope="col">Email</th>
                            <th scope="col">Company</th>
                            <th scope="col">Role</th>
                            <th scope="col">Update</th>
                            <th scope="col">Delete</th>
                        </tr>
                    </thead>
                    <tbody>
                        {list.map((item, index)=>{
                            return (
                                <tr key={index}>
                                    <td>{item.email}</td>
                                    <td>{item.company}</td>
                                    <td>{item.role}</td>
                                    <td><button className="btn btn-primary" onClick={()=>startEdit(item)}>Update</button></td>
                                    <td><button className="btn btn-danger" onClick={()=>deleteItem(item)}>Delete</button></td>
                                </tr>
                            )
                        })}
                    </tbody>

                </table>
            </div>
        </div>
    )
}

export default AdminUser