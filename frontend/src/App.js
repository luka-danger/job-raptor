import React, { useState } from 'react';
import axios from 'axios';
import { truncateDescription } from './truncate';

function App() {
  const [jobData, setJobData] = useState(null); // State to hold job data
  const [loading, setLoading] = useState(false); // State for loading status

  // Function to fetch a random job from the backend
  const fetchRandomJob = async () => {
    setLoading(true);
    try {
        // Get job posting from Node backend server
        const response = await axios.get('http://localhost:5002/random_job'); 
        setJobData(response.data);
    } catch (error) {
        console.error('Error fetching random job:', error);
    } finally {
        setLoading(false);
    }
};


  return (
    <div>
      <h1>Job Classification</h1>

      {/* Button to fetch new random job */}
      <button onClick={fetchRandomJob} disabled={loading}>
        {loading ? 'Loading...' : 'Get Random Job'}
      </button>

      {/* Display job data if available */}
      {jobData && (
        <div>
          <h2>Job Title: {jobData.job.title}</h2>
          <h3>Function: {jobData.job.function}</h3>
          <p>Description: {truncateDescription(jobData.job.description, 250)}</p>
          <h4>Prediction: {jobData.prediction}</h4>
        </div>
      )}

      {/* Display a message when no job data is available */}
      {!jobData && !loading && (
        <p>Click "Get Random Job" to fetch a job posting!</p>
      )}
    </div>
  );
}

export default App;
