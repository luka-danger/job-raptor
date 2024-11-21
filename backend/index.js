const express = require('express');
const axios = require('axios');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const port = 5002;

// Enable CORS for all origins
app.use(cors());
app.use(bodyParser.json());

// Route to fetch random job
app.get('/random_job', async (req, res) => {
    try {
        const response = await axios.get('http://127.0.0.1:5001/random_job');
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching random job' });
    }
});

// Existing prediction route
app.post('/api/predict', async (req, res) => {
    const { title, description } = req.body;

    try {
        // Get job posting details from Flask API
        const response = await axios.post('http://127.0.0.1:5001/api/predict', {
            title,
            description,
        });

        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'Error in prediction API' });
    }
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});

