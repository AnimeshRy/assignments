import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";
import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Hero Section */}
      <section className="flex flex-col items-center justify-center px-4 py-32 text-center bg-gradient-to-b from-white to-gray-50">
        <h1 className="text-5xl font-bold tracking-tight text-gray-900 sm:text-6xl">
          Welcome to Jasper Colin
        </h1>
        <p className="mt-6 text-lg leading-8 text-gray-600 max-w-2xl">
          Discover our curated collection of premium products designed to elevate your lifestyle.
          Quality meets sophistication in every piece we offer.
        </p>
        <div className="mt-10 flex items-center justify-center gap-x-6">
          <Link href="/products">
            <Button size="lg" className="bg-gray-900 hover:bg-gray-800">
              Browse Collection
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </Link>
          <Link href="/register">
            <Button variant="outline" size="lg">
              Create Account
            </Button>
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 px-4 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 gap-12 sm:grid-cols-2 lg:grid-cols-3">
            {/* Feature 1 */}
            <div className="flex flex-col items-start">
              <div className="rounded-lg bg-gray-50 p-3">
                <svg
                  className="h-6 w-6 text-gray-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M5 13l4 4L19 7"
                  />
                </svg>
              </div>
              <h3 className="mt-4 text-lg font-semibold text-gray-900">Premium Quality</h3>
              <p className="mt-2 text-gray-600">
                Each product is carefully selected to ensure the highest quality standards.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="flex flex-col items-start">
              <div className="rounded-lg bg-gray-50 p-3">
                <svg
                  className="h-6 w-6 text-gray-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <h3 className="mt-4 text-lg font-semibold text-gray-900">Fast Delivery</h3>
              <p className="mt-2 text-gray-600">
                Quick and reliable shipping to get your products to you as soon as possible.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="flex flex-col items-start">
              <div className="rounded-lg bg-gray-50 p-3">
                <svg
                  className="h-6 w-6 text-gray-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"
                  />
                </svg>
              </div>
              <h3 className="mt-4 text-lg font-semibold text-gray-900">Secure Shopping</h3>
              <p className="mt-2 text-gray-600">
                Shop with confidence knowing your transactions are safe and secure.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
