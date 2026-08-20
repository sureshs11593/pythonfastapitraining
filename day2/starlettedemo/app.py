from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

async def homepage(request):
    return JSONResponse({"message": "Hello, Starlette!"})

app = Starlette(routes=[
    Route("/", homepage)
])
'''
uvicorn app:app --reload

Where:
•	app (before :) = the Python filename (app.py) 
•	app (after :) = the Starlette application object 
•	--reload = automatically restarts the server when files change 

4. Open in your browser
http://127.0.0.1:8000/

Expected response:
{
  "message": "Hello, Starlette!"
}

or 
Run with multiple workers (production):
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4


'''
