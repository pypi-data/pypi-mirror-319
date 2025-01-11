# from fastapi import FastAPI

# def app():
#     _api = FastAPI()

#     @_api.get("/")
#     async def root():
#         return {"message": "Hello World"}

#     return _api

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app(), host="0.0.0.0", port=8000)

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}