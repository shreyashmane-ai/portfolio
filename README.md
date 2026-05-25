# Thunder Command — Python Backend Portfolio

A premium cinematic Flask portfolio inspired by Asgardian technology aesthetics — futuristic AI dashboard, not a superhero fan page.

## Stack

- **Python 3** + **Flask**
- **HTML** + **Jinja2** templates
- **Bootstrap 5**
- **Vanilla JavaScript**
- **CSS** (glassmorphism, neon effects, custom animations)

No React, Tailwind, or Node.js. No database required (contact form uses server logging + flash messages).

## Quick Start

```bash
cd portfolio
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Project Structure

```
portfolio/
├── app.py                 # Routes & portfolio data
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── index.html
│   └── components/        # Reusable sections
└── static/
    ├── css/
    │   ├── variables.css  # Design tokens
    │   ├── main.css
    │   ├── animations.css
    │   └── themes.css
    └── js/
        ├── loader.js      # Thunder loading screen
        ├── particles.js   # Storm background
        ├── effects.js     # Mjolnir hover / cursor
        └── main.js        # Scrollspy, counters, modals
```

## Customize Content

Edit the data dictionaries at the top of `app.py`:

- `SITE` — name, title, email, social links
- `ABOUT`, `SKILLS`, `PROJECTS`, `EXPERIENCE`

## Features

- Cinematic thunder loading screen
- Bifrost gradient transitions
- Glassmorphism UI panels
- Particle storm background
- Dark / light theme toggle
- Sidebar + scrollspy navigation
- Animated counters & skill bars
- Project control-panel modals
- Contact form with validation
- `prefers-reduced-motion` support

## Production

Set environment variables:

```bash
export FLASK_ENV=production
export SECRET_KEY=your-secure-random-key
```

Use **gunicorn** or **waitress** behind nginx:

```bash
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:8000 app:app
```

## License

MIT — customize freely for your portfolio.
