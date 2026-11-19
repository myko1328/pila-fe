import type { Metadata } from "next";
import Link from "next/link";
import { roadmap } from "@/data/roadmap.generated";
import {
  type FeatureStatus,
  currentSprintNumber,
  getFeatureStatus,
  statusLabels,
} from "@/data/roadmap-progress";
import styles from "./roadmap.module.css";

export const metadata: Metadata = {
  title: "Product roadmap",
  description:
    "Follow the Pila build sprint by sprint and see what is done, in progress, and planned next.",
};

function StatusMark({ status }: { status: FeatureStatus }) {
  return (
    <span className={styles.statusMark} data-status={status} aria-hidden="true">
      {status === "done" ? "✓" : status === "in-progress" ? "•" : ""}
    </span>
  );
}

export default function RoadmapPage() {
  const features = roadmap.flatMap((phase) => phase.sprints.flatMap((sprint) => sprint.features));
  const done = features.filter((feature) => getFeatureStatus(feature.id) === "done").length;
  const inProgress = features.filter(
    (feature) => getFeatureStatus(feature.id) === "in-progress",
  ).length;
  const totalPoints = roadmap.reduce(
    (phaseTotal, phase) =>
      phaseTotal +
      phase.sprints.reduce((sprintTotal, sprint) => sprintTotal + sprint.totalPoints, 0),
    0,
  );
  const completion = Math.round((done / features.length) * 100);

  return (
    <main className={styles.page}>
      <nav className={styles.nav} aria-label="Primary navigation">
        <Link className={styles.brand} href="/" aria-label="Pila home">
          Pila
        </Link>
        <Link className={styles.backLink} href="/">
          ← Back to product
        </Link>
      </nav>

      <header className={styles.hero}>
        <div>
          <p className={styles.eyebrow}>Building Pila in public</p>
          <h1>Product roadmap</h1>
          <p className={styles.intro}>
            This is the live implementation checklist. It shows what has been completed, what is
            moving now, and what the team plans to build next.
          </p>
        </div>
        <aside className={styles.legend} aria-label="Feature status legend">
          {(["done", "in-progress", "planned"] as const).map((status) => (
            <span key={status}>
              <StatusMark status={status} />
              {statusLabels[status]}
            </span>
          ))}
        </aside>
      </header>

      <section className={styles.summary} aria-labelledby="roadmap-summary">
        <div className={styles.summaryLead}>
          <p className={styles.summaryLabel}>Overall delivery</p>
          <h2 id="roadmap-summary">
            Sprint 1 of {roadmap.flatMap((phase) => phase.sprints).length}
          </h2>
          <p>
            The foundation is in progress. The proof-of-concept UI reproduction begins after the
            boilerplate is stable.
          </p>
        </div>
        <div className={styles.progressBlock}>
          <div className={styles.progressMeta}>
            <span>{completion}% complete</span>
            <span>{done + inProgress} active / finished</span>
          </div>
          <div
            className={styles.progressTrack}
            role="progressbar"
            aria-label="Overall roadmap completion"
            aria-valuemin={0}
            aria-valuemax={features.length}
            aria-valuenow={done}
          >
            <span style={{ width: `${Math.max(completion, 0.65)}%` }} />
          </div>
        </div>
        <dl className={styles.metrics}>
          <div>
            <dt>{features.length}</dt>
            <dd>features</dd>
          </div>
          <div>
            <dt>{totalPoints}</dt>
            <dd>planned points</dd>
          </div>
          <div>
            <dt>35</dt>
            <dd>points / week max</dd>
          </div>
        </dl>
      </section>

      <section className={styles.phases} aria-label="Roadmap phases">
        {roadmap.map((phase) => {
          const phaseFeatures = phase.sprints.flatMap((sprint) => sprint.features);
          const phaseDone = phaseFeatures.filter(
            (feature) => getFeatureStatus(feature.id) === "done",
          ).length;
          const phaseActive = phase.sprints.some((sprint) => sprint.number === currentSprintNumber);

          return (
            <details className={styles.phase} key={phase.number} open={phase.number === 1}>
              <summary>
                <span className={styles.phaseNumber}>{String(phase.number).padStart(2, "0")}</span>
                <span className={styles.phaseTitle}>
                  <strong>{phase.title}</strong>
                  <small>
                    {phase.sprints.length} sprint
                    {phase.sprints.length === 1 ? "" : "s"} · {phaseDone}/{phaseFeatures.length}{" "}
                    done
                  </small>
                </span>
                <span className={styles.phaseState} data-active={phaseActive || undefined}>
                  {phaseActive ? "Current phase" : "Planned"}
                </span>
                <span className={styles.chevron} aria-hidden="true">
                  ↓
                </span>
              </summary>

              <div className={styles.sprintList}>
                {phase.sprints.map((sprint) => {
                  const sprintDone = sprint.features.filter(
                    (feature) => getFeatureStatus(feature.id) === "done",
                  ).length;
                  const sprintActive = sprint.number === currentSprintNumber;

                  return (
                    <article className={styles.sprint} key={sprint.number}>
                      <header className={styles.sprintHeader}>
                        <div>
                          <p>
                            Sprint {sprint.number}
                            {sprintActive && <span className={styles.currentBadge}>Current</span>}
                          </p>
                          <h2>{sprint.title}</h2>
                          <span>{sprint.objective}</span>
                        </div>
                        <div className={styles.sprintScore}>
                          <strong>{sprint.totalPoints}</strong>
                          <span>points</span>
                        </div>
                      </header>

                      <ul className={styles.featureList}>
                        {sprint.features.map((feature) => {
                          const status = getFeatureStatus(feature.id);
                          return (
                            <li key={feature.id} data-status={status}>
                              <StatusMark status={status} />
                              <div className={styles.featureCopy}>
                                <div>
                                  <code>{feature.id}</code>
                                  <strong>{feature.title}</strong>
                                </div>
                                <p>{feature.acceptanceCriteria}</p>
                              </div>
                              <span className={styles.points}>{feature.points} pts</span>
                            </li>
                          );
                        })}
                      </ul>

                      <footer className={styles.sprintFooter}>
                        <span>
                          {sprintDone}/{sprint.features.length} complete
                        </span>
                        <p>
                          <strong>Deliverable:</strong> {sprint.deliverable}
                        </p>
                      </footer>
                    </article>
                  );
                })}
              </div>
            </details>
          );
        })}
      </section>

      <footer className={styles.footer}>
        <p>The roadmap is maintained from the source-controlled sprint blueprint.</p>
        <Link href="/">Return to Pila</Link>
      </footer>
    </main>
  );
}
