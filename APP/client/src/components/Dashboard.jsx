import React, {useState, useContext, useEffect} from 'react'

import LineChart from './LineChart';
import AuthContext from '../context/AuthContext';

export const Dashboard = () => {
    const [data, setData] = useState([]);
    const [prediction, setPrediction] = useState([]);
    const [errorMessage, setErrorMessage] = useState("");
    const {authTokens} = useContext(AuthContext);
    const token = authTokens;
    const requestOptions = {
        method:"GET",
        headers: {"Authorization":"Bearer "+token}
    }

    const [chartData,setChartData] = useState({})
    const [allChartData, setAllChartData] = useState({});
    const [covidInfoData, setCovidInfoData] = useState({});

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
        let deaths = response_data_d.data.map((row)=>row.new_deaths);
        let lines = response_data_p.data.map((row)=>row.line);
        const slider_temp = 1025;
        
        setChartData({  
            labels:dates.slice(slider_temp),
            datasets:[
                {
                    label:"Covid 19 Cases",
                    data:data_.slice(slider_temp),
                    backgroundColor: [
                        "#1c3030"
                    ],
                    borderColor: "black", 
                    borderWidth: 2,
                    pointRadius:1.5,
                },
                {
                    label:"Forecasting Line",
                    data:lines.slice(slider_temp),
                    backgroundColor: [
                        "#63e3e7"
                    ],
                    tension:0.7,
                    borderWidth:3,
                    pointRadius:1.5,
                    pointHoverRadius:0,
                },
            ]
        });

        setAllChartData({
            labels:dates,
            datasets:[
                {
                    label:"Covid 19 Cases",
                    data:data_,
                    backgroundColor: [
                        "#1c3030"
                    ],
                    borderColor: "black", 
                    borderWidth: 0.4,
                    pointRadius:1.1,
                },
                {
                    label:"Forecasting Line",
                    data:lines,
                    backgroundColor: [
                        "#63e3e7"
                    ],
                    tension:0.7,
                    borderWidth:2,
                    pointRadius:1.1,
                    pointHoverRadius:0,
                },
            ]
        });

        setCovidInfoData({
            labels:dates,
            datasets:[
                {
                    label:"Cases",
                    data:data_,
                    backgroundColor: [
                        "#1c3030"
                    ],
                    borderColor: "black", 
                    borderWidth: 0.4,
                    pointRadius:1.1,
                },
                {
                    label:"Deaths",
                    data:deaths,
                    backgroundColor: [
                        "#f00f0f"
                    ],
                    tension:0.7,
                    borderWidth:2,
                    pointRadius:1.1,
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
                <h1 className="pb-3">Dashboard</h1>
                <hr/>
                <div className="py-4">
                    <h2 className="pb-3">Forecasting</h2>
                    <div style={{width:700}} className="d-flex justify-content-center">
                        {
                            (Object.keys(chartData).length!==0)?
                                <LineChart chartData={chartData}/>:
                                "Loading"
                        }
                    </div>
                </div>
                <div className="py-4">
                    <h2 className="pb-3">Forecasting Line</h2>
                    <div style={{width:700}} className="d-flex justify-content-center">
                        {
                            (Object.keys(allChartData).length!==0)?
                                <LineChart chartData={allChartData}/>:
                                "Loading"
                        }
                    </div>
                </div>
                <div className="py-4">
                    <h2 className="pb-3">Covid 19 Information</h2>
                    <div style={{width:700}} className="d-flex justify-content-center">
                        {
                            (Object.keys(covidInfoData).length!==0)?
                                <LineChart chartData={covidInfoData}/>:
                                "Loading"
                        }
                    </div>
                </div>
            </div>
            
        </div>
    )
}
