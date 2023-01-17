import React from 'react';

let url = "faocs.onrender.com";

const Documentation = () => {
    const dataUrl = url+'/api/data';
    const lineUrl = url+'/api/predictions/line'
    const predictionsUrl = url+'/api/predictions'

    const bearer = "{'Authorization':'Bearer '+<Token>}"
    return (
        <div className="container">
            <h1>Documentation</h1>
            <hr/>
            <div className="py-2">
                <h3>Getting Covid 19 Information</h3>
                <p></p>
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
                <h3>Getting Covid 19 Information</h3>
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