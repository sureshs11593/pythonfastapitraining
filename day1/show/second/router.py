from fastapi.routing import APIRoute


def hello() -> dict:
    return {"message": "hello API route"}

hello_route = APIRoute(
    path="/hello",
    endpoint=hello,
    methods=["GET"],
    name="hello",
)