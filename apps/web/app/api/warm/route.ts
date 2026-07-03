import { NextResponse } from "next/server";

const apiBaseUrl = process.env.API_BASE_URL ?? process.env.NEXT_PUBLIC_API_BASE_URL ?? "https://voledge-ai-api.onrender.com";

export const dynamic = "force-dynamic";

export async function GET() {
  const started = Date.now();

  try {
    const response = await fetch(`${apiBaseUrl}/api/cache/warm`, {
      cache: "no-store",
      headers: { Accept: "application/json" }
    });
    const body = await response.json();

    return NextResponse.json({
      status: response.ok ? "warm" : "upstream_error",
      upstreamStatus: response.status,
      elapsedMs: Date.now() - started,
      api: body
    }, { status: response.ok ? 200 : 502 });
  } catch (error) {
    return NextResponse.json({
      status: "error",
      elapsedMs: Date.now() - started,
      message: error instanceof Error ? error.message : "Warm-up failed"
    }, { status: 500 });
  }
}
