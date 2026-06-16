import express from 'express';

const app = express();

app.get('/', (req, res) => {
    res.send('Hello and welcome to stockflow API')
});

app.get('/api', (req, res) => {
    res.status(200).json({message: 'Stockflow API is working'})
});

export default app;