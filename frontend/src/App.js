import React, { useState } from 'react';
import axios from 'axios';
import { truncateDescription } from './truncate';
import { companies } from './companyList';

function App() {
  const [jobData, setJobData] = useState(null); 
  const [loading, setLoading] = useState(false); 

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
      <h1>Introducing...netWork <i>DinoDetect</i></h1>
      <h2>A new way to job search</h2>

      {/* Button to fetch new random job */}
      <button onClick={fetchRandomJob} disabled={loading}>
        {loading ? 'Loading...' : 'Next Job Posting'}
      </button>

      {/* Display job data if available */}
      {jobData && (
        <div>
          <h2>Job Title: {jobData.job.title}</h2>
          <h3>Company: {companies[Math.floor(Math.random() * companies.length)]}</h3>
          <h4>Function: {jobData.job.function}</h4>
          <p><b>Description:</b> {truncateDescription(jobData.job.description, 250)}</p>
          <h4>Prediction: {jobData.prediction}</h4>
        </div>
      )}

      {/* Display a message when no job data is available */}
      {!jobData && !loading && (
        <p>Click "Next Job Posting" to run the <i>DinoDetect</i> job post classifier!</p>
      )}
    </div>
  );
}

export default App;
