# Copyright 2026 - AI4I. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import os

import pytest
import requests


@pytest.mark.e2e
def test_auth_endpoint():
    """Smoke-test that the SecEv4LIA API auth endpoint returns a valid response."""
    api_key = os.environ.get("SECEV4LIA_API_KEY")
    base_url = os.environ.get("SECEV4LIA_API_BASE_URL")

    if not api_key or not base_url:
        pytest.skip(
            "SECEV4LIA_API_KEY and SECEV4LIA_API_BASE_URL must both be set — skipping auth smoke test"
        )

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    response = requests.get(f"{base_url}/api/v1/auth", headers=headers)
    assert response.status_code == 200
