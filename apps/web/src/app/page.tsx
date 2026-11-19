import Link from "next/link";
import styles from "./page.module.css";

export default function Home() {
  return (
    <main className={styles.page}>
      <nav className={styles.nav} aria-label="Primary navigation">
        <Link className={styles.brand} href="/" aria-label="Pila home">
          Pila
        </Link>
        <Link className={styles.navLink} href="/roadmap">
          View roadmap
        </Link>
      </nav>

      <section className={styles.hero}>
        <p className={styles.kicker}>A smarter way to wait</p>
        <h1>Find a service. Check the line. Take a number.</h1>
        <p className={styles.intro}>
          Pila is being built for walk-in businesses and the customers who would rather know the
          wait before leaving home.
        </p>
        <div className={styles.actions}>
          <Link className={styles.primaryAction} href="/roadmap">
            Follow the build
            <span aria-hidden="true">→</span>
          </Link>
          <a
            className={styles.secondaryAction}
            href="https://claude.ai/artifact/QzSmBKWsZF24QUdQvNm4VZ"
            target="_blank"
            rel="noreferrer"
          >
            View proof of concept
          </a>
        </div>
      </section>
    </main>
  );
}
