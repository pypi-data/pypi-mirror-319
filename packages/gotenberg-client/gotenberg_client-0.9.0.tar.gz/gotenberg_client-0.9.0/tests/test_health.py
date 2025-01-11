# SPDX-FileCopyrightText: 2023-present Trenton H <rda0128ou@mozmail.com>
#
# SPDX-License-Identifier: MPL-2.0
from gotenberg_client import GotenbergClient
from gotenberg_client._health import StatusOptions


class TestHealthStatus:
    def test_health_endpoint(
        self,
        client: GotenbergClient,
    ):
        status = client.health.health()
        assert status.overall == StatusOptions.Up
        assert status.chromium is not None
        assert status.chromium.status == StatusOptions.Up
        if "uno" in status.data:  # pragma: no cover
            assert status.uno is not None
            assert status.uno.status == StatusOptions.Up
