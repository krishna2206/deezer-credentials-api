import json

from fastapi import FastAPI, Request, Response

from arlupdater import update_deezer_arl

webserver = FastAPI()


@webserver.get("/")
async def hello_world():
    return {"message": "Hello World"}


@webserver.post("/update-arl")
async def get_page_screenshot(request: Request):
    if request.headers.get("Content-Type") == "application/json":
        json_payload = await request.json()
        login_mail = json_payload.get("login_mail")
        login_password = json_payload.get("login_password")

        if None not in (login_mail, login_password):
            success, data = await update_deezer_arl(
                login_mail, login_password)
            if not success:
                return Response(
                    status_code=500,
                    headers={"Content-Type": "application/json"},
                    content=json.dumps({"error": f"Internal Server Error. {data}"}))
            return Response(
                status_code=200,
                content=json.dumps({"status": "success", "cookies": data}))
        return Response(
            status_code=400,
            headers={"Content-Type": "application/json"},
            content=json.dumps(
                {
                    "error": "login_mail and login_password are required"
                }
            ))
    return Response(
        status_code=400,
        headers={"Content-Type": "application/json"},
        content=json.dumps({"error": "Invalid request"}))
