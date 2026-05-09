from fastapi import Header, HTTPException


API_SECRET = "talentlens_secure_api"


def verify_api_key(

    x_api_key: str = Header(None)

):

    if x_api_key != API_SECRET:

        raise HTTPException(

            status_code=401,

            detail="Unauthorized"
        )