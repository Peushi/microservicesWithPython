import httpx
from fastapi import FastAPI, Request, Response

from app.config import settings

app = FastAPI(title="gateway", version="1.0.0")

# Routing table — maps the resource name in the URL path to the target service base URL.
# Path structure: /{version}/{resource}/...
#   e.g. GET /v1/users/123  →  resource = "users"  →  forward to user_service_url
#
# Add new entries here as each module introduces a new service.
# Module 4 will add: "notifications"
# Module 5 will add: "consent", "logs"
# Module 6 will add: "auth"
ROUTES: dict[str, str] = {
    "users": settings.user_service_url,
    "games": settings.game_service_url,
    "activities": settings.activity_service_url,
    "notifications": settings.notification_service_url,
}


@app.get("/health")
async def health():
    """
    Gateway liveness check. Handled here — never forwarded to a service.
    In Module 10 this endpoint will be upgraded to fan out to all services
    and return their individual status.
    """
    return {"status": "ok", "service": "gateway"}


@app.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"]
)
async def proxy(request: Request, path: str):
    """
    Catch-all reverse proxy — forwards every request
    to the correct downstream service.
    """

    # Step 1 — Parse path
    segments = path.split("/")

    # Path must contain at least version + resource
    # Example: /v1/users
    if len(segments) < 2:
        return Response(
            status_code=404,
            content="Invalid path"
        )

    # Step 2 — Find target service
    resource = segments[1]
    target_base = ROUTES.get(resource)

    # Unknown resource
    if not target_base:
        return Response(
            status_code=404,
            content=f"Unknown resource: {resource}"
        )

    # Step 3 — Build full target URL
    target_url = f"{target_base}/{path}"

    try:
        # Forward request to downstream service
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=request.headers.raw,
                content=await request.body(),
                params=request.query_params,
            )

        # Return downstream response
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.headers.get("content-type"),
        )

    # Step 4 — Handle unreachable service
    except httpx.RequestError:
        return Response(
            status_code=503,
            content="Service unavailable"
        )