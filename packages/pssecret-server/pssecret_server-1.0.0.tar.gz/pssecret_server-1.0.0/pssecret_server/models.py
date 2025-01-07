from pydantic import BaseModel, Field


class Secret(BaseModel):
    data: str = Field(title="Secret", description="Some secret data", min_length=1)


class SecretSaveResult(BaseModel):
    key: str = Field(
        title="Retrieval key",
        description="Key that should be used for retrieval of submitted secret",
    )
