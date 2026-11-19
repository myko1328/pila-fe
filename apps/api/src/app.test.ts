import request from "supertest";
import { describe, expect, it } from "vitest";

import { type HealthResponse, createApp } from "#api/app.js";

describe("GET /health", () => {
  it("reports that the API is healthy without requiring a database", async () => {
    const response = await request(createApp()).get("/health").expect(200);
    const body = response.body as HealthResponse;

    expect(body).toMatchObject({
      status: "ok",
      service: "pila-api",
    });
    expect(Number.isNaN(Date.parse(body.timestamp))).toBe(false);
    expect(response.headers["x-powered-by"]).toBeUndefined();
  });
});
