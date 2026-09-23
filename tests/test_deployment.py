"""Regression tests for public-hosting safeguards."""
from __future__ import annotations

import unittest
from unittest.mock import patch

import app as server
import config


class DeploymentConfigTests(unittest.TestCase):
    def test_production_requires_a_fixed_secret(self):
        with patch.multiple(
            config,
            IS_PRODUCTION=True,
            SECRET_KEY_CONFIGURED=False,
            SESSION_COOKIE_SECURE=True,
        ):
            with self.assertRaisesRegex(RuntimeError, "TALKMATE_SECRET_KEY"):
                config.validate_runtime_config()

    def test_production_requires_secure_session_cookies(self):
        with patch.multiple(
            config,
            IS_PRODUCTION=True,
            SECRET_KEY_CONFIGURED=True,
            SESSION_COOKIE_SECURE=False,
        ):
            with self.assertRaisesRegex(RuntimeError, "TALKMATE_SESSION_SECURE=true"):
                config.validate_runtime_config()

    def test_health_has_browser_safety_headers(self):
        response = server.app.test_client().get("/api/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")
        self.assertEqual(response.headers["Referrer-Policy"], "strict-origin-when-cross-origin")

    def test_production_health_enables_hsts(self):
        with patch.object(config, "IS_PRODUCTION", True):
            response = server.app.test_client().get("/api/health")

        self.assertEqual(response.headers["Strict-Transport-Security"], "max-age=31536000")
