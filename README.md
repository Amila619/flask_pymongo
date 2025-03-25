# Flask PyMongo Vercel Deployment

This project demonstrates how to deploy a Flask application using PyMongo on Vercel.

## Project Structure

- `app.py`: The main Flask application file.
- `vercel.json`: Configuration file for deploying the application on Vercel.

## vercel.json Configuration

The `vercel.json` file is configured as follows:
```json
{
    "version": 2,
    "builds": [
        {
            "src": "app.py",
            "use": "@vercel/python"
        }
    ],
    "routes": [
        {
            "src": "/(.*)",
            "dest": "app.py"
        }
    ]
}
```