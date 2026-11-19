export type FeatureStatus = "done" | "in-progress" | "planned";

export const currentSprintNumber = 1;

export const featureProgress: Record<string, FeatureStatus> = {
  "FND-001": "done",
  "FND-002": "done",
  "FND-003": "done",
  "FND-004": "done",
};

export const statusLabels: Record<FeatureStatus, string> = {
  done: "Done",
  "in-progress": "In progress",
  planned: "Planned",
};

export function getFeatureStatus(featureId: string): FeatureStatus {
  return featureProgress[featureId] ?? "planned";
}
