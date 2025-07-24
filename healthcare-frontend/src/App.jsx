
import { useState, useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';
import './App.css';

function App() {
  const [diagnoses, setDiagnoses] = useState([]);
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    fetch('http://localhost:3001/api/analytics/spark/top-diagnoses')
      .then((response) => response.json())
      .then((data) => setDiagnoses(data))
      .catch((error) => console.error('Error fetching data:', error));
  }, []);

  useEffect(() => {
    if (diagnoses.length > 0 && chartRef.current) {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
      const ctx = chartRef.current.getContext('2d');
      chartInstance.current = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: diagnoses.map((d) => d.diagnosis),
          datasets: [{
            label: 'Diagnosis Count',
            data: diagnoses.map((d) => d.count),
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
            borderColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
            borderWidth: 1,
          }],
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
              title: { display: true, text: 'Count' },
            },
            x: {
              title: { display: true, text: 'Diagnosis' },
            },
          },
          plugins: {
            legend: { display: true, position: 'top' },
            title: { display: true, text: 'Top 5 Diagnoses' },
          },
        },
      });
    }
    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
  }, [diagnoses]);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Smart Healthcare Analytics</h1>
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-2">Top 5 Diagnoses</h2>
        <div>
          {diagnoses.length > 0 ? (
            <div>
              <ul className="list-disc pl-5">
                {diagnoses.map((item, index) => (
                  <li key={index} className="mb-2">
                    {item.diagnosis}: {item.count}
                  </li>
                ))}
              </ul>
              <canvas ref={chartRef} className="mt-4" />
            </div>
          ) : (
            <p>Loading...</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
