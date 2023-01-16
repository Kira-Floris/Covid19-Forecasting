import React, {useState, useContext, useEffect} from 'react'

import LineChart from './LineChart';
import { UserContext } from '../context/UserContext';

export const Dashboard = () => {
    const [data, setData] = useState([]);
    const [prediction, setPrediction] = useState([]);
    const [errorMessage, setErrorMessage] = useState("");
    const [token] = useContext(UserContext);
    const requestOptions = {
        method:"GET",
        headers: {"Authorization":"Bearer "+token}
    }

    const [chartData,setChartData] = useState({})

    let fetchData = async ()=>{
        const response_d = await fetch('/api/data', requestOptions);
        const response_data_d = await response_d.json();

        if(!response_d.ok){
            setErrorMessage(response_d.detail);
        }else{
            setData(response_data_d.data);
        }

        const response_p = await fetch('/api/predictions/line', requestOptions);
        const response_data_p = await response_p.json();

        if(!response_p.ok){
            setErrorMessage(response_p.detail);
        }else{
            setPrediction(response_data_p.data);
        }

        let dates = response_data_p.data.map((row)=>row.date);

        let data_ = response_data_d.data.map((row)=>row.new_cases);
        let lines = response_data_p.data.map((row)=>row.line);
        
        setChartData({  
            labels:dates,
            datasets:[
                {
                    label:"Covid 19 Cases",
                    data:data_,
                    backgroundColor: [
                        "#1c3030"
                    ],
                    borderColor: "black", 
                    borderWidth: 0.1,
                    pointRadius:1.5,
                },
                {
                    label:"Forecasting Line",
                    data:lines,
                    backgroundColor: [
                        "#63e3e7"
                    ],
                    tension:0.4,
                    borderWidth:1,
                    pointRadius:0.5,
                    pointHoverRadius:0,
                },
            ]
        });
    }

    useEffect(()=>{
        fetchData();
    },[]);

    return (
        <div className='d-flex justify-content-center'>
            <div>
                <h1 className='text-center'>Dashboard</h1>
                <div style={{width:700}} className="d-flex justify-content-center">
                    {
                        (Object.keys(chartData).length!==0)?
                            <LineChart chartData={chartData}/>:
                            "Loading"
                    }
                </div>
            </div>
            
        </div>
    )
}
