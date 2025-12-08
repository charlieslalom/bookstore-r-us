import Link from "next/link"
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge" // Need to create Badge
import { Star } from "lucide-react"

export interface Product {
    id: string | { asin: string }
    title: string
    price: number
    imUrl: string
    category: string
    // add other fields as needed
}

export function ProductCard({ product }: { product: Product }) {
    const asin = typeof product.id === 'string' ? product.id : product.id.asin

    return (
        <Card className="flex flex-col h-full overflow-hidden transition-all hover:shadow-lg">
            <Link href={`/product/${asin}`} className="flex-1">
                <div className="aspect-[3/4] overflow-hidden relative group">
                    <img
                        src={product.imUrl}
                        alt={product.title}
                        className="object-cover w-full h-full transition-transform group-hover:scale-105"
                    />
                </div>
            </Link>
            <CardContent className="p-4">
                <div className="flex justify-between items-start mb-2">
                    <div className="text-sm text-muted-foreground">{product.category}</div>
                    <div className="flex items-center text-yellow-500">
                        <Star className="w-3 h-3 fill-current" />
                        <span className="text-xs ml-1">4.5</span>
                    </div>
                </div>
                <Link href={`/product/${asin}`}>
                    <h3 className="font-semibold text-lg leading-tight line-clamp-2 hover:underline">{product.title}</h3>
                </Link>
                <div className="mt-2 font-bold text-xl">${product.price.toFixed(2)}</div>
            </CardContent>
            <CardFooter className="p-4 pt-0 mt-auto">
                <Button className="w-full">Add to Cart</Button>
            </CardFooter>
        </Card>
    )
}
