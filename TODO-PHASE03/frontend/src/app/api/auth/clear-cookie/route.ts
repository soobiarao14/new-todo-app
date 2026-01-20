/**
 * API route to clear auth cookie on signout.
 */
import { NextResponse } from "next/server";

export async function POST() {
  const response = NextResponse.json({ success: true });

  response.cookies.delete("auth_token");

  return response;
}
