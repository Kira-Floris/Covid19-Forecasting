import React from 'react';

let url = "faocs.onrender.com";

const Documentation = () => {
    const dataUrl = url+'/api/data';
    const lineUrl = url+'/api/predictions/line'
    const predictionsUrl = url+'/api/predictions'

    const bearer = "{'Authorization':'Bearer '+<Token>}"
    return (
        <div className="container pt-4">
            <h1>Documentation</h1>
            <hr/>
            <div className="py-2">
                <h3>Accessing the FAOCS api</h3>
                <p>To access the FAOCS predictions and data, the FAOCS needs your Token. You can get the token by registering and going to your account information.
                    <br/><br/>
                    In your account, you can also regenerate your token or update your account information.    
                </p>
                
            </div>
            <hr/>
            <div className="py-2">
                <h3>Getting Covid 19 Information</h3>
                <p>This endpoint returns data used in this project. This data was collected from <a href="ourworldindata.org">OurWorldInData</a> website. 
                The data contains Covid 19 information from all over the world from the first case in 2019 till now.</p>
                <div>
                    <pre className="bg-light border p-3">
                        <code>
                            <span>import requests</span><br/>
                            <span>response = requests.get("{dataUrl}","headers":{bearer})</span><br/>
                            <span>data_json = response.json()</span><br/>
                            <span>data = data_json.data</span><br/>
                        </code>
                    </pre>
                </div>
            </div>
            <hr/>
            <div className="py-2">
                <h3>Getting Forecasting Line</h3>
                <p>This endpoint returns predictions line data from the winning model, Facebook Prophet, 
                    starting from the first date in the dataset till the current date the request is sent plus 18 days.</p>
                <div>
                    <pre className="bg-light border p-3">
                        <code>
                            <span>import requests</span><br/>
                            <span>response = requests.get("{lineUrl}","headers":{bearer})</span><br/>
                            <span>data_json = response.json()</span><br/>
                            <span>data = data_json.data</span><br/>
                        </code>
                    </pre>
                </div>
            </div>
            <hr/>
            <div className="py-2">
                <h2>Getting Predictions Models.</h2>
                <h5>The winning model is Facebook Prophet</h5>
                <p>This endpoint returns predictions starting from the date the request is made and 18 days in the future. 
                    The endpoint requires a token that you can get in your account after registering.</p>
                <div>
                    <pre className="bg-light border p-3">
                        <code>
                            <span>import requests</span><br/>
                            <span>response = requests.get("{predictionsUrl}","headers":{bearer})</span><br/>
                            <span>data_json = response.json()</span><br/>
                            <span>data = data_json.data</span><br/>
                        </code>
                    </pre>
                </div>
            </div>
        </div>
    )
}

export default Documentation;