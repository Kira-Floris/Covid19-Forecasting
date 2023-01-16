import React from 'react';
import {Line, Bar} from 'react-chartjs-2';
import {Chart as ChartJS} from 'chart.js/auto';
import * as zoom from 'chartjs-plugin-zoom';

function LineChart({chartData}) {
  return <Line 
            data={chartData}
            options={{
              responsive:true,
              title:{
                text:"Covid 19 Cases Forecasting", 
                display:true
              },
              options:{
                plugins:{
                  zoom:{
                    zoom:{
                      wheel:{
                        enabled:true,
                      },
                      pinch:{
                        enabled:true,
                      },
                      mode:'xy',
                    }
                  }
                }
              }
            }}
            />
}

export default LineChart