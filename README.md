# Personal Portfolio Website

A modern, responsive personal portfolio website built with Flask, HTML, and CSS.

## Features

- Clean and modern design with light theme
- Responsive layout for all devices
- Smooth animations and transitions
- Interactive skill cards with progress bars
- Contact form with backend processing
- Social media integration

## Setup Instructions

1. Clone the repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```
5. Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
portfolio/
├── main.py              # Flask application
├── requirements.txt     # Python dependencies
├── static/
│   └── css/
│       └── style.css    # Stylesheet
└── templates/
    └── index.html      # Main template
```

## Customization

- Edit the content in `templates/index.html` to update your personal information
- Modify colors and styles in `static/css/style.css`
- Update contact form handling in `main.py`

## Technologies Used

- Flask (Backend)
- HTML5
- CSS3
- Font Awesome (Icons)
- Google Fonts (Typography) 