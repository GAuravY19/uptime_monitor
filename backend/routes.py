from fastapi import APIRouter, Form, Request, Query
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from .database import get_connection
from .helper import generate_web_id
from .crud import get_recent_tracking, get_all_websites

from datetime import datetime

router = APIRouter()

# Location of index.html
templates = Jinja2Templates(directory="Frontend")


@router.get("/")
def dashboard(request: Request):

    # tracking_data = get_latest_tracking()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "tracking_data": tracking_data
        }
    )


@router.get("/website-list")
def website_list():

    websites = get_all_websites()

    return JSONResponse(content=websites)


@router.post("/add-website")
def add_website(
    website_name: str = Form(...),
    website_url: str = Form(...)
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        web_id = generate_web_id()

        cursor.execute(
            """
            INSERT INTO website_listing
            (web_id, web_name, web_url, under_track)
            VALUES (%s, %s, %s, %s)
            """,
            (
                web_id,
                website_name,
                website_url,
                True
            )
        )

        conn.commit()

    except Exception as e:

        conn.rollback()
        print(e)

    finally:

        cursor.close()
        conn.close()

    return RedirectResponse(
        url="/",
        status_code=303
    )


@router.get("/tracking-data")
def tracking_data(

    web_id: str | None = Query(default=None)

):

    records = get_recent_tracking(
        web_id=web_id,
        limit=30
    )

    for row in records:

        if row["hit_timestamp"]:

            row["hit_timestamp"] = row["hit_timestamp"].strftime("%H:%M:%S")

    return JSONResponse(content=records)
