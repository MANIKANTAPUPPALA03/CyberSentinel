<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://github.com/user-attachments/assets/0aa67016-6eaf-458a-adb2-6e31a0763ed6" />
</div>

# CyberSentinel - URL Trust Analyzer

A security-focused web application that analyzes URLs for trustworthiness using ML-powered backend analysis.

## Run Locally

**Prerequisites:** Node.js

1. Install dependencies:
   `npm install`
2. (Optional) Set the backend API URL in [.env.local](.env.local):
   `VITE_API_BASE_URL=http://localhost:8000`
   If not set, defaults to `http://localhost:8000`
3. Run the app:
   `npm run dev`

## Architecture

- **Frontend**: React + TypeScript + Vite (presentation layer)
- **Backend**: Handles all ML analysis at `/analyze-url` endpoint

