from fastapi import Header, HTTPException, status

from app import config


def verify_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if not config.AGENT_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AGENT_API_KEY chÆ°a Ä‘Æ°á»£c cáº¥u hÃ¬nh",
        )

    if not x_api_key or x_api_key != config.AGENT_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-API-Key khÃ´ng há»£p lá»‡",
        )
