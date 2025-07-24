
const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');
const axios= require("axios")

const app = express();
app.use(cors({ origin: 'http://localhost:5173' })); // Allow React frontend (Vite default port)
app.use(express.json());

// PostgreSQL connection
const pool = new Pool({
    user: 'postgres', // Replace with your PostgreSQL username
    host: 'localhost',
    database: 'healthcare_db',
    password: 'your_password', // Replace with your PostgreSQL password
    port: 5432,
});

// Test database connection
pool.connect((err, client, release) => {
    if (err) {
        return console.error('Error connecting to PostgreSQL:', err.stack);
    }
    console.log('Connected to PostgreSQL database');
    release();
});

// Get all patients
app.get('/api/patients', async (req, res) => {
    console.log("request recieved from",req);
    try {
        const result = await pool.query('SELECT * FROM Patients LIMIT 100'); // Limit for performance
        res.json(result.rows);
    } catch (err) {
        console.error('Error fetching patients:', err.stack);
        res.status(500).send('Server Error');
    }
});

// Get top 5 diagnoses
app.get('/api/analytics/diagnoses', async (req, res) => {
    try {
        const result = await pool.query(`
            SELECT Diagnosis, COUNT(*) as Count
            FROM MedicalRecords
            GROUP BY Diagnosis
            ORDER BY Count DESC
            LIMIT 5
        `);
        res.json(result.rows);
    } catch (err) {
        console.error('Error fetching diagnoses:', err.stack);
        res.status(500).send('Server Error');
    }
});


app.get('/api/analytics/diagnoses', async (req, res) => {
    try {
        const result = await pool.query(`
            SELECT Diagnosis, COUNT(*) as Count
            FROM MedicalRecords
            GROUP BY Diagnosis
            ORDER BY Count DESC
            LIMIT 5
        `);
        res.json(result.rows);
    } catch (err) {
        console.error('Error fetching diagnoses:', err.stack);
        res.status(500).send('Server Error');
    }
});

// SQL-based endpoint (example)
app.get('/api/analytics/sql/top-diagnoses', async (req, res) => {
  try {
    const result = await pool.query(
      'SELECT Diagnosis, COUNT(*) as Count FROM MedicalRecords GROUP BY Diagnosis ORDER BY Count DESC LIMIT 5'
    );
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});


// New endpoint to proxy to Flask server
app.get('/api/analytics/spark/top-diagnoses', async (req, res) => {
  try {
    const response = await axios.get('http://localhost:5000/api/spark/top-diagnoses');
    res.json(response.data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});


// Start the server
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
