import { Navbar } from "@/components/navbar";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Star, ArrowLeft } from "lucide-react";
import Link from "next/link";

interface ProductDetail {
    id: string;
    title: string;
    price: number;
    imUrl?: string | null;
    description?: string | null;
    brand?: string | null;
    categories?: string[];
    also_bought?: string[];
    also_viewed?: string[];
    num_reviews?: number;
    avg_stars?: number;
}

export async function getProduct(asin: string): Promise<ProductDetail | null> {
    try {
        const res = await fetch(`http://localhost:8081/products-microservice/product/${asin}`, { cache: 'no-store' });
        if (!res.ok) return null;
        const data = await res.json();
        return data;
    } catch (e) {
        console.error(e);
        return null;
    }
}

export default async function ProductDetailPage({ params }: { params: Promise<{ asin: string }> }) {
    const { asin } = await params;
    const product = await getProduct(asin);

    if (!product) {
        return (
            <div className="flex min-h-screen flex-col">
                <Navbar />
                <main className="container py-8 flex-1">
                    <div className="text-center py-20">
                        <h1 className="text-2xl font-bold mb-4">Product Not Found</h1>
                        <p className="text-muted-foreground mb-6">The product you're looking for doesn't exist or has been removed.</p>
                        <Link href="/">
                            <Button>Back to Home</Button>
                        </Link>
                    </div>
                </main>
            </div>
        );
    }

    const imageUrl = product.imUrl || '';
    const avgStars = product.avg_stars || 0;
    const numReviews = product.num_reviews || 0;
    const categories = product.categories || [];

    return (
        <div className="flex min-h-screen flex-col">
            <Navbar />
            <main className="container py-8 flex-1">
                <Link href="/" className="inline-flex items-center text-muted-foreground hover:text-primary mb-6">
                    <ArrowLeft className="w-4 h-4 mr-2" />
                    Back to Shopping
                </Link>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div className="aspect-square overflow-hidden rounded-xl bg-secondary">
                        {imageUrl ? (
                            <img
                                src={imageUrl}
                                alt={product.title}
                                className="object-cover w-full h-full"
                            />
                        ) : (
                            <div className="w-full h-full flex items-center justify-center text-muted-foreground">
                                No image available
                            </div>
                        )}
                    </div>

                    <div className="space-y-6">
                        {product.brand && (
                            <p className="text-muted-foreground">{product.brand}</p>
                        )}

                        <h1 className="text-3xl font-bold tracking-tight">{product.title}</h1>

                        <div className="flex items-center gap-4">
                            <div className="flex items-center text-primary">
                                <Star className="w-5 h-5 fill-current" />
                                <span className="ml-1 font-semibold">{avgStars.toFixed(1)}</span>
                            </div>
                            <span className="text-muted-foreground">({numReviews} reviews)</span>
                        </div>

                        {categories.length > 0 && (
                            <div className="flex flex-wrap gap-2">
                                {categories.map((category, index) => (
                                    <Badge key={index} variant="secondary">{category}</Badge>
                                ))}
                            </div>
                        )}

                        <div className="text-4xl font-extrabold text-primary">
                            ${product.price.toFixed(2)}
                        </div>

                        {product.description && (
                            <Card>
                                <CardContent className="pt-6">
                                    <h2 className="font-semibold mb-2">Description</h2>
                                    <p className="text-muted-foreground">{product.description}</p>
                                </CardContent>
                            </Card>
                        )}

                        <Button size="lg" className="w-full font-bold">
                            Add to Cart
                        </Button>
                    </div>
                </div>
            </main>
        </div>
    );
}
