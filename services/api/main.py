import os
from fastapi import FastAPI
from pydantic import BaseModel
import asyncpg
from fastapi.middleware.cors import CORSMiddleware


DATABASE_URL = "postgresql://postgres:example@db:5432/noqueue"

app = FastAPI(title="NoQueue AI API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class IssueTokenPayload(BaseModel):
    location_id: str


@app.on_event("startup")
async def startup():
    app.state.db = await asyncpg.create_pool(DATABASE_URL)


@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()


@app.get("/")
async def root():
    return {"status": "API running"}


@app.post("/api/tokens/issue")
async def issue_token(body: IssueTokenPayload):
    async with app.state.db.acquire() as conn:

        # next token number
        row = await conn.fetchrow(
            """
            SELECT COALESCE(MAX(token_number), 0) + 1
            FROM tokens
            WHERE location_id = $1::uuid
            """,
            body.location_id,
        )
        token_number = row[0]

        # simple wait time (2 min per person)
        predicted_wait = 0

        token_id = await conn.fetchval(
            """
            INSERT INTO tokens (location_id, token_number, predicted_wait_seconds)
            VALUES ($1::uuid, $2, $3)
            RETURNING id
            """,
            body.location_id,
            token_number,
            predicted_wait,
        )

    return {
        "token_id": token_id,
        "token_number": token_number,
        "predicted_wait_seconds": predicted_wait,
    }
