"""Backend main application."""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Backend API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 