import { Navbar } from "@/components/navbar";
import { ProductCard } from "@/components/product-card";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { ArrowRight } from "lucide-react";

async function getProducts(category: string) {
  // SSR Fetch
  try {
    // Use Docker internal URL if running in Docker, else localhost
    // Since specific instructions said "Run services locally (Docker)", we might be outside docker now calling localhost
    const res = await fetch(`http://localhost:8081/products-microservice/products/category/${category}?page=0&size=4`, { cache: 'no-store' });
    if (!res.ok) return [];
    const data = await res.json();
    return data.content || [];
  } catch (e) {
    console.error(e);
    return [];
  }
}

export default async function Home() {
  const books = await getProducts("Books");
  const music = await getProducts("Music");
  const electronics = await getProducts("Electronics");

  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1">
        {/* Hero Section */}
        <section className="bg-muted py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center space-y-4 text-center">
              <div className="space-y-2">
                <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none">
                  Your Favorite Bookstore, <span className="text-primary">Reimagined.</span>
                </h1>
                <p className="mx-auto max-w-[700px] text-muted-foreground md:text-xl">
                  Discover the best books, music, and electronics. Secure, fast, and built for you.
                </p>
              </div>
              <div className="space-x-4">
                <Link href="/products/Books">
                  <Button size="lg">Shop Books</Button>
                </Link>
                <Link href="/register">
                  <Button variant="outline" size="lg">Join Now</Button>
                </Link>
              </div>
            </div>
          </div>
        </section>

        {/* Bestsellers Section */}
        <section className="container py-12 space-y-12">
          {books.length > 0 && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold tracking-tight">Best Sellers in Books</h2>
                <Link href="/products/Books" className="flex items-center text-primary hover:underline">
                  View all <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                {books.map((p: any) => <ProductCard key={p.id.asin || p.id} product={p} />)}
              </div>
            </div>
          )}

          {music.length > 0 && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold tracking-tight">Top Music</h2>
                <Link href="/products/Music" className="flex items-center text-primary hover:underline">
                  View all <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                {music.map((p: any) => <ProductCard key={p.id.asin || p.id} product={p} />)}
              </div>
            </div>
          )}

          {electronics.length > 0 && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold tracking-tight">Electronics & Gadgets</h2>
                <Link href="/products/Electronics" className="flex items-center text-primary hover:underline">
                  View all <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                {electronics.map((p: any) => <ProductCard key={p.id.asin || p.id} product={p} />)}
              </div>
            </div>
          )}
        </section>
      </main>
      <footer className="py-6 md:px-8 md:py-0">
        <div className="container flex flex-col items-center justify-between gap-4 md:h-24 md:flex-row">
          <p className="text-balance text-center text-sm leading-loose text-muted-foreground md:text-left">
            Built by Antigravity. Source code available on GitHub.
          </p>
        </div>
      </footer>
    </div>
  );
}
