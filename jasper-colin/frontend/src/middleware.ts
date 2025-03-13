import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// Add paths that require authentication
const protectedPaths = ['/products'];

// Add paths that should redirect to /products if user is already authenticated
const authPaths = ['/login', '/register'];

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token');
  const { pathname } = request.nextUrl;

  // Check if the path requires authentication
  if (protectedPaths.some(path => pathname.startsWith(path))) {
    if (!token) {
      const response = NextResponse.redirect(new URL('/login', request.url));
      return response;
    }
  }

  // Redirect authenticated users away from auth pages
  if (authPaths.includes(pathname) && token) {
    const response = NextResponse.redirect(new URL('/products', request.url));
    return response;
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};
