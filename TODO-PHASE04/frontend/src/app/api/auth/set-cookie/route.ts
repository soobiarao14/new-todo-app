/**
 * API route to set auth cookie on the frontend domain.
 * This solves the cross-origin cookie problem where the backend (hf.space)
 * sets a cookie that can't be read by the frontend middleware (vercel.app).
 */
import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    const { token } = await request.json();

    if (!token) {
      return NextResponse.json(
        { error: "Token is required" },
        { status: 400 }
      );
    }

    const response = NextResponse.json({ success: true });

    // Set the auth cookie on the frontend domain
    const isProduction = process.env.NODE_ENV === "production";

    response.cookies.set("auth_token", token, {
      httpOnly: true,
      secure: isProduction,
      sameSite: isProduction ? "strict" : "lax",
      maxAge: 3600, // 1 hour (matches backend)
      path: "/",
    });

    return response;
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to set cookie" },
      { status: 500 }
    );
  }
}
