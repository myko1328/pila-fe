import { describe, expect, it, vi } from "vitest";

import { resolvePort, startApiServer } from "#api/server.js";

describe("API server lifecycle", () => {
  it("starts independently and shuts down cleanly", async () => {
    const logger = {
      error: vi.fn(),
      info: vi.fn(),
    };
    const runningApi = await startApiServer({
      host: "127.0.0.1",
      logger,
      port: 0,
      registerSignalHandlers: false,
    });

    expect(runningApi.server.listening).toBe(true);

    await runningApi.close();

    expect(runningApi.server.listening).toBe(false);
    expect(logger.error).not.toHaveBeenCalled();
  });

  it("rejects invalid port values", () => {
    expect(() => resolvePort("not-a-port")).toThrow(/PORT must be an integer/);
    expect(() => resolvePort("70000")).toThrow(/PORT must be an integer/);
  });
});
