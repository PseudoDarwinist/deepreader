# DEEP READER

## Overview
A static HTML website that helps users master complex knowledge using the Feynman Technique. The application transforms technical articles into deep learning experiences with structured learning paths.

## Project Structure
- `index.html` - Single-page application containing all HTML, CSS, and JavaScript

## Tech Stack
- Pure HTML/CSS/JavaScript (no build system)
- Static file serving via Python's built-in http.server

## Running the App
The app is served using Python's http.server on port 5000:
```
python3 -m http.server 5000 --bind 0.0.0.0
```

## Deployment
Configured as a static site deployment serving from the root directory (`.`).
