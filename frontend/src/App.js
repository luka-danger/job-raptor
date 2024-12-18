import React, { useState } from 'react';
import axios from 'axios';
import { truncateDescription } from './truncate';
import logo from './velociraptor.gif';
// Import the custom animation hook
import { useAnimation } from './useAnimation'; 

function App() {
  const [jobData, setJobData] = useState(null);
  const [loading, setLoading] = useState(false);

  // Use the custom hook for animation
  const typedText = useAnimation(); 

  // Function to fetch a random job from the backend
  const fetchRandomJob = async () => {
    setLoading(true);
    try {
      // Get job posting from Node backend server
      const response = await axios.get('http://localhost:5001/api/random-posting');
      setJobData(response.data);

    } catch (error) {
      console.error('Error fetching random job:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className='container'>
      <div className='upper'>
        <div className='text'>
          <h1 className='title'><i>Job Raptor</i></h1>
          <h3 className='slogan'>A job posting classifier, powered by netWork</h3>
        </div>
      </div>

      <div className='lower'>
        {/* Button to fetch new random job */}
        <button onClick={fetchRandomJob} disabled={loading}>
          {loading ? 'Loading...' : 'Next Job Posting'}
        </button>

        {/* Display job data if available */}
        {jobData && (
          <div>
            <h2>Job Title: {jobData.posting.title}</h2>
            <h3>Company: {jobData.posting.company}</h3>
            <p className='description'><b>Description:</b> {truncateDescription(jobData.posting.description, 50)}</p>
            <h4 className={`prediction ${jobData.prediction === 'Real' ? 'real' : 'fake'}`}>
              Likely {jobData.prediction}
            </h4>
          </div>
        )}

        {/* Display a message when no job data is available */}
        {!jobData && !loading && (
          <h3>Click "Next Job Posting" to run the <i>Job Raptor</i> job post classifier!</h3>
        )}
      
        <div className='footer'>
          <div className='logo'>
            <img className='dino' src={logo} alt='loading...' />
            <div className='typing'>
              <span className='sentence'>{typedText}</span>
              <span className='cursor'></span>
            </div>
          </div>
        </div>
      </div>
      
    </div>
  );
}

export default App;
