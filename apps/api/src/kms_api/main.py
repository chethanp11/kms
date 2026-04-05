from __future__ import annotations

import os

from kms_config import load_runtime_config
from kms_api.app_factory import create_app

app = create_app(seed_demo_data=False, runtime_config=load_runtime_config())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "kms_api.main:app",
        host=os.getenv("KMS_API_HOST", "127.0.0.1"),
        port=int(os.getenv("KMS_API_PORT", "8010")),
        reload=False,
    )
