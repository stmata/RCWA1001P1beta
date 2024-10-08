import sys, os
# Add the root directory to the syspath
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.templating import Jinja2Templates
import uvicorn
from dash_app import app as app_dash
import requests

# Create FastAPI app object
app = FastAPI()

# Get the absolute path to the templates directory
templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "templates"))
# Get the absolute path to the static directory
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "static"))
# Serve static files
app.mount("/static", StaticFiles(directory=static_dir))
# Set up Jinja2 template for rendering HTML files
templates = Jinja2Templates(directory=templates_dir)
# External API URL (replace with the actual URL)
EXTERNAL_API_URL = "https://weather1003.azurewebsites.net/info"
 
def get_external_info():
    try:
        response = requests.get(EXTERNAL_API_URL)
        return response.json()  # Convert response to JSON
    except Exception as e:
        return {"date": "N/A", "time": "N/A", "weather": {"city": "Unknown", "temperature": "N/A", "description": "N/A"}}
 
# In-memory user storage for login
users = {"admin": "password"}

# Define routes
@app.get("/")
async def home_page(request: Request):
    info = get_external_info()
    return templates.TemplateResponse("home.html", {"request": request, "info":info})

@app.get("/login")
async def login_page(request: Request):
    info = get_external_info()
    return templates.TemplateResponse("login.html", {"request": request, "info":info})

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username in users and users[username] == password:
        # Redirect to the dashboard generated with dash upon success
        response = RedirectResponse(url='/dashboard', status_code=302)
        response.set_cookie(key="Authorization", value="Bearer Token", httponly=True)
        return response
    info = get_external_info()
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials", "info":info})

@app.get("/logout")
async def logout():
    response = RedirectResponse(url='/login')
    response.delete_cookie('Authorization')
    return response



# Mount the Dash App under the /dashboard path
app.mount("/dashboard", WSGIMiddleware(app_dash.server))
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8021, workers=1)