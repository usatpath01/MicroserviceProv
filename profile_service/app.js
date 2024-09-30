const express = require('express');
const ejs = require('ejs');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
    res.send('Profile service is running');
});

app.get('/profile', (req, res) => {
    const username = req.query.username || 'Guest';
    console.log(`Received request for username: ${username}`);
    
    let evaluatedUsername = username;
    let evaluationError = null;

    try {
        if (username.includes('<%=') && username.includes('%>')) {
            // If it's EJS syntax, render it
            evaluatedUsername = ejs.render(username, {
                process: {
                    env: {
                        NODE_ENV: process.env.NODE_ENV || 'development'
                        // Add other safe environment variables here
                    }
                }
                // Add other safe globals here
            });
        } else {
            // If it's not EJS syntax, eval it directly
            evaluatedUsername = eval(username);
        }
    } catch (error) {
        console.error('Evaluation error:', error);
        evaluationError = error.message;
    }

    const template = `
        <h1>Welcome, ${evaluatedUsername}!</h1>
        <p>This is your profile page.</p>
        <p>Original input: ${username}</p>
        <p>Evaluated result: ${evaluationError ? 'Error: ' + evaluationError : evaluatedUsername}</p>
    `;
    
    res.send(template);
});

app.listen(port, () => {
    console.log(`Profile service listening at http://localhost:${port}`);
});