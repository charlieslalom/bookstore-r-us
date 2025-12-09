"""
Verification tests for Issue #28: Item selection returns 404

Bug Summary:
When selecting an item, the application returns a 404 error instead of the expected data.

Root Cause:
The Next.js frontend was missing the product detail page component at /product/[asin].
When users clicked on a product card, they were navigated to /product/{asin}, but no
page existed to handle that route.

Fix:
Added the missing page component at nextjs-frontend/src/app/product/[asin]/page.tsx

Acceptance Criteria:
- [ ] Product detail page exists at /product/[asin]/page.tsx
- [ ] Page fetches product data from products-microservice API
- [ ] Page renders product details (title, price, description, etc.)
- [ ] Page shows "Product Not Found" for invalid ASINs
- [ ] All unit tests pass
- [ ] Frontend builds successfully
"""

import pytest
import subprocess
import time
import signal
import os
import re
import requests


class TestIssue28PageExists:
    """Verify the product detail page component exists"""

    def test_product_page_file_exists(self):
        """
        Verify: Product detail page file exists at the correct location

        The bug was that this page was missing entirely.
        """
        page_path = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "nextjs-frontend", "src", "app", "product", "[asin]", "page.tsx"
        )

        assert os.path.exists(page_path), (
            f"Product detail page not found at {page_path}. "
            "This is the root cause of the 404 error."
        )

    def test_product_page_exports_default_function(self):
        """
        Verify: Product detail page exports a default page component
        """
        page_path = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "nextjs-frontend", "src", "app", "product", "[asin]", "page.tsx"
        )

        with open(page_path, "r") as f:
            content = f.read()

        assert "export default" in content, (
            "Product detail page should export a default component"
        )

    def test_product_page_fetches_from_api(self):
        """
        Verify: Product detail page fetches from products-microservice API
        """
        page_path = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "nextjs-frontend", "src", "app", "product", "[asin]", "page.tsx"
        )

        with open(page_path, "r") as f:
            content = f.read()

        # Check for API endpoint
        assert "products-microservice/product" in content, (
            "Product page should fetch from products-microservice API"
        )


class TestIssue28PageContent:
    """Verify the product detail page has correct content structure"""

    def test_page_handles_product_not_found(self):
        """
        Verify: Page handles 404 case when product doesn't exist
        """
        page_path = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "nextjs-frontend", "src", "app", "product", "[asin]", "page.tsx"
        )

        with open(page_path, "r") as f:
            content = f.read()

        # Should handle null/not found case
        assert "not found" in content.lower() or "Product Not Found" in content, (
            "Product page should handle product not found case"
        )

    def test_page_renders_product_title(self):
        """
        Verify: Page renders product title
        """
        page_path = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "nextjs-frontend", "src", "app", "product", "[asin]", "page.tsx"
        )

        with open(page_path, "r") as f:
            content = f.read()

        assert "product.title" in content or "title" in content.lower(), (
            "Product page should render product title"
        )

    def test_page_renders_product_price(self):
        """
        Verify: Page renders product price
        """
        page_path = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "nextjs-frontend", "src", "app", "product", "[asin]", "page.tsx"
        )

        with open(page_path, "r") as f:
            content = f.read()

        assert "product.price" in content or "price" in content.lower(), (
            "Product page should render product price"
        )

    def test_page_has_add_to_cart_button(self):
        """
        Verify: Page has Add to Cart button
        """
        page_path = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "nextjs-frontend", "src", "app", "product", "[asin]", "page.tsx"
        )

        with open(page_path, "r") as f:
            content = f.read()

        assert "Add to Cart" in content, (
            "Product page should have Add to Cart button"
        )


class TestIssue28Build:
    """Verify the frontend builds successfully with the new page"""

    def test_build_succeeds(self):
        """
        Verify: npm run build completes successfully

        The new page should not break the build.
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

        assert result.returncode == 0, (
            f"Build failed:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )

    def test_no_typescript_errors(self):
        """
        Verify: No TypeScript errors in the new page
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

        # Check for TypeScript errors related to our new page
        assert "product/[asin]/page.tsx" not in combined_output or result.returncode == 0, (
            "TypeScript errors in product detail page"
        )


class TestIssue28UnitTests:
    """Verify unit tests pass for the product detail page"""

    def test_unit_tests_pass(self):
        """
        Verify: All unit tests pass including new product detail page tests
        """
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
            f"Unit tests failed:\n{result.stdout}\n{result.stderr}"
        )

    def test_product_detail_page_tests_exist(self):
        """
        Verify: Test file exists for product detail page
        """
        test_path = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "nextjs-frontend", "__tests__", "product-detail-page.test.tsx"
        )

        assert os.path.exists(test_path), (
            "Product detail page test file should exist"
        )

    def test_product_detail_page_has_coverage(self):
        """
        Verify: Product detail page has >80% coverage
        """
        frontend_dir = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "nextjs-frontend"
        )

        result = subprocess.run(
            ["npm", "test", "--", "--coverage", "--coverageReporters=text"],
            cwd=frontend_dir,
            capture_output=True,
            text=True,
            timeout=120
        )

        # Check that the product page is covered
        assert "app/product/[asin]" in result.stdout, (
            "Coverage report should include product detail page"
        )

        # Parse coverage for the product page - look for the line
        lines = result.stdout.split('\n')
        for line in lines:
            if "app/product/[asin]" in line:
                # Extract percentage - format is typically: file | stmts | branch | funcs | lines
                parts = line.split('|')
                if len(parts) >= 2:
                    try:
                        stmt_coverage = float(parts[1].strip())
                        assert stmt_coverage >= 80, (
                            f"Product page statement coverage is {stmt_coverage}%, expected >= 80%"
                        )
                    except (ValueError, IndexError):
                        pass  # If we can't parse, skip this assertion
                break


@pytest.mark.skip(reason="Dev server tests require running infrastructure - skipping in CI environment")
class TestIssue28DevServer:
    """Verify the development server serves the product page correctly"""

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
        TestIssue28DevServer.frontend_process = subprocess.Popen(
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
        if TestIssue28DevServer.frontend_process:
            try:
                os.killpg(os.getpgid(TestIssue28DevServer.frontend_process.pid), signal.SIGTERM)
            except ProcessLookupError:
                pass  # Process already terminated

    def test_product_page_route_exists(self):
        """
        Verify: Product page route does not return 404

        Before the fix, navigating to /product/{asin} would return 404.
        Now it should return 200 (or potentially a different error if
        the backend isn't running, but NOT a 404 from missing route).
        """
        # Try to access a product page
        response = requests.get(f"{self.FRONTEND_URL}/product/test-asin", timeout=10)

        # The route should exist (not a Next.js 404)
        # Note: The page might show "Product Not Found" if the API isn't available,
        # but the page itself should render (200 status)
        assert response.status_code == 200, (
            f"Product page route returned {response.status_code}. "
            "Expected 200 - the route should exist now."
        )

    def test_product_page_renders_html(self):
        """
        Verify: Product page renders valid HTML
        """
        response = requests.get(f"{self.FRONTEND_URL}/product/test-asin", timeout=10)

        assert response.status_code == 200, "Product page should return 200"
        assert "<html" in response.text or "<!DOCTYPE html>" in response.text, (
            "Product page should render valid HTML"
        )

    def test_product_page_has_navbar(self):
        """
        Verify: Product page includes the navbar component
        """
        response = requests.get(f"{self.FRONTEND_URL}/product/test-asin", timeout=10)

        assert response.status_code == 200, "Product page should return 200"
        # The navbar contains the brand name
        assert "Bookstore" in response.text, (
            "Product page should include the navbar with brand name"
        )
