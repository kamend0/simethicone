# import marshal
# import pickle
# import types

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
async def healthy():
    return JSONResponse(content={"status": "ok"}, status_code=200)


# with open("model.pkl", "rb") as fh:
#     serialized_data = pickle.load(fh)
#     code_obj = marshal.loads(serialized_data["code"])
#     predict = types.FunctionType(
#         code_obj, globals(), serialized_data["name"], serialized_data["defaults"]
#     )


# TODO: create your API
@app.get("/economical")
async def get_economical():
    """
    TODO Memoized get on "economical" table. If record exists, get it. If not, compute
    it, then save it, and return it.
    """
    return 200
