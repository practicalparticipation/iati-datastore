import os
import sentry_sdk
from iatilib.frontend.app import create_app
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_dsn = os.getenv("SENTRY_DSN")
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        integrations=[FlaskIntegration()],
        traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0"))
    )

app = create_app()
