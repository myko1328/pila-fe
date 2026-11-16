import express, { type Express } from "express";

export type HealthResponse = {
  status: "ok";
  service: "pila-api";
  timestamp: string;
};

export function createApp(): Express {
  const app = express();

  app.disable("x-powered-by");
  app.use(express.json());

  app.get("/health", (_request, response) => {
    const body: HealthResponse = {
      status: "ok",
      service: "pila-api",
      timestamp: new Date().toISOString(),
    };

    response.status(200).json(body);
  });

  return app;
}
