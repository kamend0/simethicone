import pickle
import marshal
import types

with open("model.pkl", "rb") as fh:
    serialized_data = pickle.load(fh)
    code_obj = marshal.loads(serialized_data["code"])
    predict = types.FunctionType(
        code_obj, globals(), serialized_data["name"], serialized_data["defaults"]
    )

# TODO: create your API
