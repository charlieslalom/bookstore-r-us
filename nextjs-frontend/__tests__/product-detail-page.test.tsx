import { render, screen } from "@testing-library/react";

// Mock fetch
global.fetch = jest.fn();

// Mock next/navigation
jest.mock("next/navigation", () => ({
  useRouter: () => ({
    push: jest.fn(),
  }),
}));

// Mock AuthContext
jest.mock("@/context/AuthContext", () => ({
  useAuth: () => ({
    user: null,
    logout: jest.fn(),
  }),
}));

const mockProduct = {
  id: "B00TEST123",
  title: "Test Book Title",
  price: 19.99,
  imUrl: "https://example.com/book.jpg",
  description: "This is a test book description.",
  brand: "Test Publisher",
  categories: ["Books", "Fiction"],
  also_bought: ["B00OTHER1", "B00OTHER2"],
  also_viewed: ["B00VIEW1"],
  num_reviews: 42,
  avg_stars: 4.5,
};

const mockEmptyProduct = {
  id: "B00EMPTY",
  title: "Minimal Product",
  price: 9.99,
  imUrl: null,
  description: null,
  brand: null,
  categories: [],
  also_bought: [],
  also_viewed: [],
  num_reviews: 0,
  avg_stars: 0,
};

// Import after mocking
import ProductDetailPage, { getProduct } from "@/app/product/[asin]/page";

describe("Product Detail Page", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe("getProduct function", () => {
    it("fetches product data successfully", async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockProduct,
      });

      const product = await getProduct("B00TEST123");

      expect(global.fetch).toHaveBeenCalledWith(
        "http://localhost:8081/products-microservice/product/B00TEST123",
        { cache: "no-store" }
      );
      expect(product).toEqual(mockProduct);
    });

    it("returns null when fetch fails", async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 404,
      });

      const product = await getProduct("NONEXISTENT");

      expect(product).toBeNull();
    });

    it("returns null when fetch throws an error", async () => {
      (global.fetch as jest.Mock).mockRejectedValueOnce(new Error("Network error"));

      const product = await getProduct("B00ERROR");

      expect(product).toBeNull();
    });
  });

  describe("ProductDetailPage component", () => {
    it("renders product title", async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockProduct,
      });

      const page = await ProductDetailPage({ params: Promise.resolve({ asin: "B00TEST123" }) });
      render(page);

      expect(screen.getByText("Test Book Title")).toBeInTheDocument();
    });

    it("renders product price formatted correctly", async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockProduct,
      });

      const page = await ProductDetailPage({ params: Promise.resolve({ asin: "B00TEST123" }) });
      render(page);

      expect(screen.getByText("$19.99")).toBeInTheDocument();
    });

    it("renders product description", async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockProduct,
      });

      const page = await ProductDetailPage({ params: Promise.resolve({ asin: "B00TEST123" }) });
      render(page);

      expect(screen.getByText("This is a test book description.")).toBeInTheDocument();
    });

    it("renders product image with alt text", async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockProduct,
      });

      const page = await ProductDetailPage({ params: Promise.resolve({ asin: "B00TEST123" }) });
      render(page);

      const img = screen.getByAltText("Test Book Title");
      expect(img).toBeInTheDocument();
      expect(img).toHaveAttribute("src", "https://example.com/book.jpg");
    });

    it("renders Add to Cart button", async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockProduct,
      });

      const page = await ProductDetailPage({ params: Promise.resolve({ asin: "B00TEST123" }) });
      render(page);

      expect(screen.getByRole("button", { name: /add to cart/i })).toBeInTheDocument();
    });

    it("renders star rating and review count", async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockProduct,
      });

      const page = await ProductDetailPage({ params: Promise.resolve({ asin: "B00TEST123" }) });
      render(page);

      expect(screen.getByText("4.5")).toBeInTheDocument();
      expect(screen.getByText(/42 reviews/i)).toBeInTheDocument();
    });

    it("renders categories as badges", async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockProduct,
      });

      const page = await ProductDetailPage({ params: Promise.resolve({ asin: "B00TEST123" }) });
      render(page);

      expect(screen.getByText("Fiction")).toBeInTheDocument();
    });

    it("renders not found message when product does not exist", async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 404,
      });

      const page = await ProductDetailPage({ params: Promise.resolve({ asin: "NONEXISTENT" }) });
      render(page);

      expect(screen.getByText(/product not found/i)).toBeInTheDocument();
    });

    it("handles product with missing optional fields", async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockEmptyProduct,
      });

      const page = await ProductDetailPage({ params: Promise.resolve({ asin: "B00EMPTY" }) });
      render(page);

      expect(screen.getByText("Minimal Product")).toBeInTheDocument();
      expect(screen.getByText("$9.99")).toBeInTheDocument();
    });

    it("renders brand when available", async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockProduct,
      });

      const page = await ProductDetailPage({ params: Promise.resolve({ asin: "B00TEST123" }) });
      render(page);

      expect(screen.getByText("Test Publisher")).toBeInTheDocument();
    });

    it("renders back to shopping link", async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockProduct,
      });

      const page = await ProductDetailPage({ params: Promise.resolve({ asin: "B00TEST123" }) });
      render(page);

      const backLink = screen.getByRole("link", { name: /back/i });
      expect(backLink).toBeInTheDocument();
    });

    it("shows no image placeholder when imUrl is missing", async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockEmptyProduct,
      });

      const page = await ProductDetailPage({ params: Promise.resolve({ asin: "B00EMPTY" }) });
      render(page);

      expect(screen.getByText(/no image available/i)).toBeInTheDocument();
    });
  });
});
