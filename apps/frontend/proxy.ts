import { NextRequest, NextResponse } from "next/server";
import {
  unauthenticatedRoutes,
  authenticatedRoutes,
} from "@/core/constants/route";

export function proxy(request: NextRequest) {
  const path = request.nextUrl.pathname;
  const token = request.cookies.get("token")?.value;
  const isUnauthenticatedRoute = unauthenticatedRoutes.includes(path);
  const isAuthenticatedRoute = authenticatedRoutes.includes(path);

  if (isAuthenticatedRoute && !token) {
    return NextResponse.redirect(new URL("/login", request.nextUrl));
  }

  if (isUnauthenticatedRoute && token) {
    return NextResponse.redirect(new URL("/profile", request.nextUrl));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|.*\\.png$).*)"],
};proxy