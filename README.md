# word-guessr 🔠
This is the GitHub page for [WordGuessr](word-guessr-juules32s-projects.vercel.app), a word guessing game in the 'dle' genre, meaning you get a new puzzle every day!

# How to run locally
- Install python 😇
- Install dependencies: `pip install -r requirements.txt`
- Run the webserver: `uvicorn main:app --reload --port 80`

# Web Stack
Frontend: [htmx](https://htmx.org/) & [jinja](https://jinja.palletsprojects.com/en/3.1.x/) & [tailwind](https://tailwindcss.com/)
Backend: [FastAPI](https://fastapi.tiangolo.com/) & [redis](https://redis.io/)
