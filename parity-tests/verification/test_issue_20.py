"""
Verification tests for Issue #20: Tailwind v4 CSS-first configuration compatibility

Bug Summary:
The Next.js frontend fails to build or run due to Tailwind CSS v4 compatibility issues.
The error "Cannot apply unknown utility class 'border-border'" occurs because Tailwind v4
uses CSS-first configuration and doesn't read JS config the same way v3 did.

Acceptance Criteria:
- [ ] Frontend builds successfully without CSS errors
- [ ] Frontend runs in development mode without errors
- [ ] All existing unit tests continue to pass
- [ ] Tailwind CSS v4 @theme directive properly defines colors
- [ ] No "Cannot apply unknown utility class" errors
"""

import pytest
import requests
import subprocess
import time
import signal
import os
import re


class TestIssue20Build:
    """Verify that the build completes successfully with Tailwind v4"""

    def test_build_succeeds_without_css_errors(self):
        """
        Verify: npm run build completes without Tailwind CSS errors

        This was the core bug - the build would fail with:
        "Cannot apply unknown utility class `border-border`"
        """
        frontend_dir = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "nextjs-frontend"
        )

        result = subprocess.run(
            ["npm", "run", "build"],
            cwd=frontend_dir,
            capture_output=True,
            text=True,
            timeout=300
        )

        # Check the build succeeded
        assert result.returncode == 0, (
            f"Build failed (expected to succeed with Tailwind v4 fix):\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )

        # Check no Tailwind CSS errors in output
        combined_output = result.stdout + result.stderr
        assert "Cannot apply unknown utility class" not in combined_output, (
            "Build output contains Tailwind CSS error - fix not working"
        )

    def test_no_border_border_error(self):
        """
        Verify: No 'border-border' utility class error

        The specific error from the bug report was:
        "Cannot apply unknown utility class `border-border`"
        """
        frontend_dir = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "nextjs-frontend"
        )

        result = subprocess.run(
            ["npm", "run", "build"],
            cwd=frontend_dir,
            capture_output=True,
            text=True,
            timeout=300
        )

        combined_output = result.stdout + result.stderr
        assert "border-border" not in combined_output.lower() or result.returncode == 0, (
            "Build still has 'border-border' utility class error"
        )


class TestIssue20UnitTests:
    """Verify that unit tests pass after the Tailwind v4 migration"""

    def test_all_unit_tests_pass(self):
        """Verify: All 48 unit tests pass after the fix"""
        frontend_dir = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "nextjs-frontend"
        )

        result = subprocess.run(
            ["npm", "test"],
            cwd=frontend_dir,
            capture_output=True,
            text=True,
            timeout=120
        )

        assert result.returncode == 0, (
            f"Unit tests failed after Tailwind v4 fix:\n{result.stdout}\n{result.stderr}"
        )


class TestIssue20CSSConfiguration:
    """Verify the CSS-first configuration is properly set up"""

    def test_globals_css_uses_import_directive(self):
        """
        Verify: globals.css uses @import 'tailwindcss' (v4 style)
        instead of @tailwind directives (v3 style)
        """
        globals_css_path = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "nextjs-frontend", "src", "app", "globals.css"
        )

        with open(globals_css_path, "r") as f:
            content = f.read()

        # Should use v4 @import syntax
        assert '@import "tailwindcss"' in content or "@import 'tailwindcss'" in content, (
            "globals.css should use @import 'tailwindcss' for Tailwind v4"
        )

        # Should NOT use v3 @tailwind directives
        assert "@tailwind base" not in content, (
            "globals.css should not use @tailwind base (v3 syntax)"
        )
        assert "@tailwind components" not in content, (
            "globals.css should not use @tailwind components (v3 syntax)"
        )
        assert "@tailwind utilities" not in content, (
            "globals.css should not use @tailwind utilities (v3 syntax)"
        )

    def test_globals_css_has_theme_directive(self):
        """
        Verify: globals.css uses @theme directive for CSS-first config

        Tailwind v4 requires theme configuration via @theme in CSS
        """
        globals_css_path = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "nextjs-frontend", "src", "app", "globals.css"
        )

        with open(globals_css_path, "r") as f:
            content = f.read()

        assert "@theme" in content, (
            "globals.css should have @theme directive for Tailwind v4 configuration"
        )

    def test_border_color_defined_in_theme(self):
        """
        Verify: Border color is defined in @theme directive

        The original bug was that border-border couldn't resolve because
        the border color wasn't available in the CSS-first config
        """
        globals_css_path = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "nextjs-frontend", "src", "app", "globals.css"
        )

        with open(globals_css_path, "r") as f:
            content = f.read()

        # Check that --color-border is defined in the @theme section
        assert "--color-border" in content, (
            "globals.css should define --color-border in @theme for Tailwind v4"
        )

    def test_no_apply_border_border(self):
        """
        Verify: No @apply border-border directive exists

        The fix should remove or replace @apply border-border
        """
        globals_css_path = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "nextjs-frontend", "src", "app", "globals.css"
        )

        with open(globals_css_path, "r") as f:
            content = f.read()

        assert "@apply border-border" not in content, (
            "globals.css should not use @apply border-border - "
            "this causes the v4 compatibility error"
        )


class TestIssue20DevServer:
    """Verify the development server starts and runs without errors"""

    FRONTEND_URL = "http://localhost:3000"
    frontend_process = None

    @pytest.fixture(scope="class", autouse=True)
    def setup_frontend(self, request):
        """Start the Next.js frontend for testing"""
        frontend_dir = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "nextjs-frontend"
        )

        # Start the dev server
        TestIssue20DevServer.frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid
        )

        # Wait for server to be ready
        max_retries = 30
        for i in range(max_retries):
            try:
                response = requests.get(self.FRONTEND_URL, timeout=2)
                break
            except requests.exceptions.RequestException:
                time.sleep(1)

        yield

        # Cleanup
        if TestIssue20DevServer.frontend_process:
            os.killpg(os.getpgid(TestIssue20DevServer.frontend_process.pid), signal.SIGTERM)

    def test_dev_server_starts_successfully(self):
        """
        Verify: Dev server starts without CSS errors

        Before the fix, the dev server would fail to start with:
        "CssSyntaxError: tailwindcss: Cannot apply unknown utility class"
        """
        response = requests.get(self.FRONTEND_URL, timeout=10)
        # Server should return 200, not 500 (which indicates CSS error)
        assert response.status_code == 200, (
            f"Dev server returned status {response.status_code}. "
            "This may indicate a CSS/Tailwind error if status is 500."
        )

    def test_dev_server_renders_html(self):
        """Verify: Dev server renders valid HTML content"""
        response = requests.get(self.FRONTEND_URL, timeout=10)
        assert response.status_code == 200, "Server should return 200 OK"
        assert "<!DOCTYPE html>" in response.text or "<html" in response.text, (
            "Response should contain valid HTML"
        )

    def test_tailwind_classes_are_applied(self):
        """
        Verify: Tailwind CSS classes are being applied

        Check that common Tailwind utility classes appear in the rendered HTML
        """
        response = requests.get(self.FRONTEND_URL, timeout=10)
        assert response.status_code == 200, "Server must return 200"

        html = response.text
        # Check for common Tailwind classes that should be present
        tailwind_indicators = [
            "bg-background",
            "text-primary",
            "min-h-screen",
            "flex",
        ]

        found_classes = [cls for cls in tailwind_indicators if cls in html]
        assert len(found_classes) >= 2, (
            f"Expected to find Tailwind utility classes in HTML. "
            f"Found: {found_classes}"
        )

    def test_no_css_syntax_error_in_response(self):
        """
        Verify: No CSS syntax errors visible in the response

        Before the fix, the error message would appear in the response
        """
        response = requests.get(self.FRONTEND_URL, timeout=10)

        # Check for specific error messages, not just class names
        # Note: "border-border" as a class name is valid - we're checking for error messages
        error_indicators = [
            "CssSyntaxError",
            "Cannot apply unknown utility class",
            "unknown utility class `border-border`",
        ]

        for indicator in error_indicators:
            assert indicator not in response.text, (
                f"Response contains CSS error indicator: {indicator}"
            )
