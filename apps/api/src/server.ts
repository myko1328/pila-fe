import { type Server } from "node:http";
import { pathToFileURL } from "node:url";

import { createApp } from "#api/app.js";

const DEFAULT_PORT = 4000;
const DEFAULT_HOST = "0.0.0.0";

type Logger = Pick<Console, "error" | "info">;

export type ApiServerOptions = {
  host?: string;
  logger?: Logger;
  port?: number;
  registerSignalHandlers?: boolean;
};

export type RunningApiServer = {
  close: () => Promise<void>;
  server: Server;
};

export function resolvePort(value = process.env.PORT): number {
  if (value === undefined || value === "") {
    return DEFAULT_PORT;
  }

  const port = Number(value);

  if (!Number.isInteger(port) || port < 0 || port > 65_535) {
    throw new Error(`PORT must be an integer between 0 and 65535; received ${value}.`);
  }

  return port;
}

function closeHttpServer(server: Server): Promise<void> {
  return new Promise((resolve, reject) => {
    server.close((error) => {
      if (error) {
        reject(error);
        return;
      }

      resolve();
    });
  });
}

export async function startApiServer(
  options: ApiServerOptions = {},
): Promise<RunningApiServer> {
  const host = options.host ?? DEFAULT_HOST;
  const logger = options.logger ?? console;
  const port = options.port ?? resolvePort();
  const registerSignalHandlers = options.registerSignalHandlers ?? true;
  const app = createApp();

  const server = await new Promise<Server>((resolve, reject) => {
    const listeningServer = app.listen(port, host, () => resolve(listeningServer));
    listeningServer.once("error", reject);
  });

  const address = server.address();
  const activePort = typeof address === "object" && address ? address.port : port;
  logger.info(`Pila API listening on http://${host}:${activePort}`);

  let closing: Promise<void> | undefined;

  const close = (): Promise<void> => {
    if (closing) {
      return closing;
    }

    closing = closeHttpServer(server).finally(() => {
      process.off("SIGINT", onSigint);
      process.off("SIGTERM", onSigterm);
    });

    return closing;
  };

  const shutdown = (signal: NodeJS.Signals): void => {
    logger.info(`${signal} received; shutting down Pila API.`);
    void close().catch((error: unknown) => {
      logger.error("Pila API failed to shut down cleanly.", error);
      process.exitCode = 1;
    });
  };

  function onSigint(): void {
    shutdown("SIGINT");
  }

  function onSigterm(): void {
    shutdown("SIGTERM");
  }

  if (registerSignalHandlers) {
    process.once("SIGINT", onSigint);
    process.once("SIGTERM", onSigterm);
  }

  return { close, server };
}

const isEntryPoint =
  process.argv[1] !== undefined &&
  import.meta.url === pathToFileURL(process.argv[1]).href;

if (isEntryPoint) {
  void startApiServer().catch((error: unknown) => {
    console.error("Pila API failed to start.", error);
    process.exitCode = 1;
  });
}
