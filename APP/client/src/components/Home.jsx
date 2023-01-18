import React from 'react';
import Forecast from '../static/covid-19.png';

const Home = () => {
    return (
      <div>
        <div className='px-5' style={{backgroundColor:"#218e9252"}}>
            <div className='row container' style={{height:"85vh"}}>
                <div className="col-9 d-flex align-items-center justify-content-center px-5">
                    <h1 className='text-center display-5'><b>Forecasting And Alerting On Covid 19 Cases Spikes</b></h1>
                </div>
                <div className="col-3 d-flex align-items-center justify-content-center">
                    <img className="text-center" src={Forecast} style={{width:"240px", color:"red"}}/>
                </div>
            </div>
        </div>
        <div className='container py-5'>
          <h1>Features</h1>
          <div class="row px-4">
            <div class="col-sm-6 col-lg-3">
              <div class="card p-3 my-2" style={{height:250}}>
                <div class="card-body">
                  <h3 class="card-title">Rwanda Covid 19 Information</h3>
                  <p class="card-text">
                    Provides Covid 19 information in Rwanda from <a href="https://ourworldindata.org/">OurWorldInData</a>
                  </p>
                </div>
              </div>
            </div>
            <div class="col-sm-6 col-lg-3">
              <div class="card p-3 my-2" style={{height:250}}>
                <div class="card-body">
                  <h3 class="card-title">Future Values</h3>
                  <p class="card-text">
                    Check what's ahead through forecasting Covid 19 cases using Facebook Prophet Tool.
                  </p>
                </div>
              </div>
            </div>
            <div class="col-sm-6 col-lg-3">
              <div class="card p-3 my-2" style={{height:250}}>
                <div class="card-body">
                  <h3 class="card-title">Notifications</h3>
                  <p class="card-text">
                    Get notified when the forecasting model detects future spikes in Covid 19 cases.
                  </p>
                </div>
              </div>
            </div>
            <div class="col-sm-6 col-lg-3">
              <div class="card p-3 my-2" style={{height:250}}>
                <div class="card-body">
                  <h3 class="card-title">API</h3>
                  <p class="card-text">
                    Free to use and integrate API for the forecasting model.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="bg-light py-5 d-flex justify-content-center">
          <Contact/>
        </div>
      </div>
    )
}

const Contact = ()=>{
  let handleEmail = async(e)=>{
    e.preventDefault();
    let response = await fetch('/api/contact',{
        method: "POST",
        headers: {
            "Content-Type":"application/json",
        },
        body:JSON.stringify({"email":e.target.email.value,"subject":e.target.subject.value,"message":e.target.message.value})
    });
    if(response.status===200){
        document.getElementById("id_contact").reset();
        console.log('Success');
    }else{
        console.log("Something Went Wrong");
    }
  }
  return (
    <div className="container">
            <h1>Contact Us</h1>
            <div className="row">
              <form className="py-4 px-4 col-md-12 col-lg-8" id="id_contact" onSubmit={handleEmail}>
                <div className="form-group">
                  <label className="label">Email Address</label>
                  <div className="control">
                    <input
                      type="email"
                      placeholder="Where can we contact you"
                      name="email"
                      className="form-control"
                      required
                    />
                  </div>
                </div>
                <div className="field">
                  <label className="label">Subject</label>
                  <div className="control">
                    <input
                      type="text"
                      placeholder="Enter a subject for your email"
                      name="subject"
                      className="form-control"
                      required
                    />
                  </div>
                </div>
                <div className="field">
                  <label className="label">Message</label>
                  <div className="control">
                    <textarea
                      className="form-control"
                      placeholder="What do you want to tell us"
                      name="message"
                      required
                      />
                  </div>
                </div>
                {/* <ErrorMessage message={errorMessage} /> */}
                <br />
                  <button className="btn btn-lg btn-primary rounded-0 px-5" type="submit">
                  Send
                  </button>
              </form>
              <div className="col-md-12 col-lg-4 py-md-4">
                <div>
                  <h2>Location</h2>
                  <p className='py-1 px-4'>Kigali, Rwanda</p>
                </div>
                <div>
                  <h2>Email</h2>
                  <p className='py-1 px-4'>For general inquiries, please reach us on: faocs@gmail.com</p>
                </div>                
              </div>
            </div>
          </div>
  )
}

export default Home;