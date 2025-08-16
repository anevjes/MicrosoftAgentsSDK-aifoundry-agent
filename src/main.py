# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

"""
Main entrypoint for the Weather Prediction Agent.

Adds an early SSL trust bootstrap to avoid SSL: CERTIFICATE_VERIFY_FAILED
errors when fetching JWKS/OIDC metadata during JWT validation.
"""

# Ensure system trust roots are available to all HTTPS clients before other imports
try:
    # Prefer using system trust store (works great on macOS)
    import truststore  # type: ignore

    truststore.inject_into_ssl()
except Exception:
    # Fallback to certifi and set common env vars; also patch urllib as a safety net
    try:
        import certifi  # type: ignore
        import os
        import ssl
        import urllib.request

        cafile = certifi.where()
        os.environ.setdefault("SSL_CERT_FILE", cafile)
        os.environ.setdefault("REQUESTS_CA_BUNDLE", cafile)

        try:
            _ssl_ctx = ssl.create_default_context(cafile=cafile)
            _opener = urllib.request.build_opener(
                urllib.request.HTTPSHandler(context=_ssl_ctx)
            )
            urllib.request.install_opener(_opener)
        except Exception:
            # If this fails, default SSL context still benefits from env vars above
            pass
    except Exception:
        # As a last resort, proceed without modifications
        pass

# enable logging for Microsoft Agents library
# for more information, see README.md for Quickstart Agent
import logging
ms_agents_logger = logging.getLogger("microsoft.agents")
ms_agents_logger.addHandler(logging.StreamHandler())
ms_agents_logger.setLevel(logging.INFO)

from .app import AGENT_APP, CONNECTION_MANAGER
from .start_server import start_server

start_server(
    agent_application=AGENT_APP,
    auth_configuration=CONNECTION_MANAGER.get_default_connection_configuration(),
)
