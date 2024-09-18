import os

import uvicorn
from fastapi import FastAPI

from .routers import files


app = FastAPI()

app.include_router(files.router)

if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv('HOST'), port=os.getenv('PORT'))

