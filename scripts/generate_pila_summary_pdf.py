from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output" / "pdf"
OUTPUT_PATH = OUTPUT_DIR / "pila-full-product-summary.pdf"

PAGE_W, PAGE_H = A4
NAVY = colors.HexColor("#102A2A")
INK = colors.HexColor("#193536")
TEAL = colors.HexColor("#20A7B5")
CYAN = colors.HexColor("#5ED0DF")
MINT = colors.HexColor("#DFF7F4")
PALE = colors.HexColor("#F3F8F7")
GOLD = colors.HexColor("#E6A93D")
MUTED = colors.HexColor("#5F7777")
LINE = colors.HexColor("#CADBDA")
WHITE = colors.white


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(18 * mm, 15 * mm, PAGE_W - 18 * mm, 15 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(18 * mm, 10 * mm, "PILA - Product Concept and Proof-of-Concept Summary")
    canvas.drawRightString(PAGE_W - 18 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


class PilaDocTemplate(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(
            filename,
            pagesize=A4,
            rightMargin=18 * mm,
            leftMargin=18 * mm,
            topMargin=18 * mm,
            bottomMargin=22 * mm,
            title="Pila - Full Product Summary",
            author="Pila Product Team",
            subject="Product concept, proof-of-concept assessment, MVP, and rollout plan",
        )
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
        )
        self.addPageTemplates([PageTemplate(id="content", frames=[frame], onPage=footer)])


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="CoverTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=34,
        leading=38,
        textColor=WHITE,
        alignment=TA_LEFT,
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(
        name="CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=15,
        leading=21,
        textColor=colors.HexColor("#C8F2F0"),
        alignment=TA_LEFT,
    )
)
styles.add(
    ParagraphStyle(
        name="Section",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=NAVY,
        spaceBefore=6,
        spaceAfter=9,
        keepWithNext=True,
    )
)
styles.add(
    ParagraphStyle(
        name="Subsection",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12.5,
        leading=16,
        textColor=TEAL,
        spaceBefore=8,
        spaceAfter=5,
        keepWithNext=True,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyPila",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.6,
        leading=14.2,
        textColor=INK,
        spaceAfter=7,
    )
)
styles.add(
    ParagraphStyle(
        name="BulletPila",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.3,
        leading=13.5,
        textColor=INK,
        leftIndent=12,
        firstLineIndent=-8,
        bulletIndent=0,
        spaceAfter=3.5,
    )
)
styles.add(
    ParagraphStyle(
        name="Callout",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=18,
        textColor=NAVY,
        alignment=TA_CENTER,
        spaceAfter=0,
    )
)
styles.add(
    ParagraphStyle(
        name="Small",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.2,
        leading=11.5,
        textColor=MUTED,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="TableHead",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=8.4,
        leading=10.5,
        textColor=WHITE,
    )
)
styles.add(
    ParagraphStyle(
        name="TableBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.2,
        leading=11.2,
        textColor=INK,
    )
)


def p(text, style="BodyPila"):
    return Paragraph(text, styles[style])


def bullet(text):
    return Paragraph(f"- {text}", styles["BulletPila"])


def section(number, title):
    return Paragraph(f"{number}. {title}", styles["Section"])


def subsection(title):
    return Paragraph(title, styles["Subsection"])


def callout(text):
    box = Table([[Paragraph(text, styles["Callout"])]], colWidths=[PAGE_W - 44 * mm])
    box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), MINT),
                ("BOX", (0, 0), (-1, -1), 1, CYAN),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )
    return box


def table(headers, rows, widths):
    data = [[Paragraph(h, styles["TableHead"]) for h in headers]]
    data.extend([[Paragraph(str(cell), styles["TableBody"]) for cell in row] for row in rows])
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE]),
                ("GRID", (0, 0), (-1, -1), 0.45, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return t


story = []

# Cover
cover = Table(
    [
        [
            Paragraph("PILA", styles["CoverTitle"]),
        ],
        [
            Paragraph(
                "Full Product Concept and<br/>Proof-of-Concept Summary",
                styles["CoverSubtitle"],
            )
        ],
        [Spacer(1, 20 * mm)],
        [
            Paragraph(
                "A real-time local service availability and virtual queue platform for walk-in businesses.",
                ParagraphStyle(
                    "CoverPromise",
                    parent=styles["BodyText"],
                    fontName="Helvetica-Bold",
                    fontSize=17,
                    leading=23,
                    textColor=WHITE,
                ),
            )
        ],
        [Spacer(1, 42 * mm)],
        [
            Paragraph(
                "Prepared from the product discussion and live proof-of-concept review<br/>November 2026",
                ParagraphStyle(
                    "CoverDate",
                    parent=styles["Small"],
                    fontSize=9,
                    leading=13,
                    textColor=colors.HexColor("#C8F2F0"),
                ),
            )
        ],
    ],
    colWidths=[PAGE_W - 36 * mm],
    rowHeights=[None, None, None, None, None, None],
)
cover.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, -1), NAVY),
            ("LEFTPADDING", (0, 0), (-1, -1), 18 * mm),
            ("RIGHTPADDING", (0, 0), (-1, -1), 18 * mm),
            ("TOPPADDING", (0, 0), (-1, 0), 30 * mm),
            ("BOTTOMPADDING", (0, -1), (-1, -1), 22 * mm),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]
    )
)
story.append(cover)
story.append(PageBreak())

story += [
    section("1", "Executive overview"),
    p(
        "Pila is a Cebu-focused, mobile-friendly platform that helps customers find a business offering a needed service, check whether the service is currently available, understand the expected wait, and join a virtual queue before traveling to the shop. For merchants, it provides a lightweight operating system for store hours, services, prices, employees, capacity, and customer flow."
    ),
    callout("Find a nearby shop that can serve you soon, see the real wait, and reserve your place before traveling."),
    Spacer(1, 8),
    p(
        "The concept began as a queue tool for one shop and developed into a local service-discovery platform. It now combines real-time availability, queue management, staff assignment, location information, and potential future booking. The proof of concept demonstrates that the interaction model is understandable and technically plausible. The primary remaining risk is operational: merchants must keep the queue accurate enough for customers to trust it."
    ),
    subsection("Recommended initial market"),
    p(
        "Start with three to five barbershops in one compact area of Mandaue City. Barbershops have visible queues, repeat customers, predictable service durations, and relatively simple staffing. This makes them a stronger first pilot than clinics, which introduce medical privacy and scheduling complexity."
    ),
    section("2", "How the idea developed"),
    p(
        "The original discussion considered several Cebu-related opportunities: flood and traffic reporting, jeepney route guidance, public-market price tracking, queue management for small businesses, and habal-habal fare estimation. The queue idea became the priority because it provides direct customer value and has a clearer path to merchant revenue."
    ),
    table(
        ["Stage", "Product direction", "Result"],
        [
            ["Initial concept", "Simple queue tool for one business", "Customers receive a number; staff call the next person."],
            ["Expanded concept", "Service discovery across several shops", "Customers compare opening status, price, queue, staff, and waiting time."],
            ["Current direction", "Local availability and virtual queue platform", "A two-sided product for customers and walk-in service businesses."],
        ],
        [30 * mm, 61 * mm, 72 * mm],
    ),
    section("3", "Target users and core problem"),
    subsection("Customers"),
    p("Pila is designed for people who want to avoid traveling to a business only to discover that:"),
    bullet("the business is closed or the desired service is unavailable;"),
    bullet("all qualified employees are busy;"),
    bullet("the queue is too long;"),
    bullet("the shop cannot finish the service before closing; or"),
    bullet("the price or location is unsuitable."),
    p(
        "Likely customer groups include local residents, students, workers with limited time, people using public transportation, and visitors who do not already know which businesses are available nearby."
    ),
    subsection("Merchants"),
    p(
        "The merchant side is intended for small walk-in service businesses such as barbershops, salons, massage shops, car washes, repair shops, clinics, and service counters. These businesses often manage customers through physical lines, notebooks, text messages, Facebook, or word of mouth."
    ),
    section("4", "Customer experience"),
    p("The proof of concept demonstrates the following customer journey:"),
    table(
        ["Step", "Customer action", "Information provided"],
        [
            ["1", "Open Pila and choose a service", "Examples include haircut, shave, massage, car wash, or check-up."],
            ["2", "Compare participating shops", "Open status, closing time, price, duration, location, queue, staff, wait, and capacity."],
            ["3", "Select a shop", "The interface explains whether the customer can join and the final acceptance time."],
            ["4", "Enter a first name and take a number", "The prototype minimizes customer information at the point of entry."],
            ["5", "Track the ticket", "A production version should show position, estimated turn, arrival deadline, and notifications."],
        ],
        [14 * mm, 58 * mm, 91 * mm],
    ),
    Spacer(1, 8),
    subsection("Most important customer answer"),
    callout("Estimated wait: 25 minutes<br/>Available to join now"),
    Spacer(1, 7),
    p(
        "The prototype currently exposes several operational values at once: waiting, being served, staff free, estimated wait, and spots left. These are useful, but the estimated wait and ability to join should receive the strongest visual emphasis. Additional statistics can remain available as secondary details."
    ),
    section("5", "Merchant experience"),
    subsection("Queue desk"),
    bullet("View customers being served and those still waiting."),
    bullet("Call the next customer and assign a qualified employee."),
    bullet("Mark a service as completed or record a no-show."),
    bullet("Add walk-in customers who do not use the app."),
    bullet("Remove queue entries and begin a new business day."),
    bullet("View simple counts for customers served, waiting, and no-shows."),
    subsection("Store settings"),
    bullet("Shop name, location, and customer waiting capacity."),
    bullet("Opening and closing hours for each day."),
    bullet("Offered services, prices, and expected duration."),
    bullet("Employees, on-duty status, and service qualifications."),
    p(
        "The merchant configuration is comprehensive, but it is long on a mobile screen. A production interface should divide it into Business details, Hours, Services and prices, Staff, and Queue rules. The daily queue desk should remain separate and require very few actions."
    ),
    section("6", "Core product logic"),
    p(
        "Merchants should not manually maintain every status. Real-time values should be calculated from normal queue operations so that the system remains accurate during busy periods."
    ),
    table(
        ["Displayed value", "Recommended calculation"],
        [
            ["Waiting", "Active tickets that have not yet been called."],
            ["Being served", "Tickets with an active service session."],
            ["Available staff", "On-duty, qualified employees without an active assignment."],
            ["Spots left", "Configured waiting capacity minus active waiting tickets."],
            ["Estimated wait", "Workload ahead distributed across qualified staff, adjusted by service duration."],
            ["Final joining time", "The latest time the queue can accept a customer and still finish before closing."],
        ],
        [48 * mm, 115 * mm],
    ),
    section("7", "Proof-of-concept assessment"),
    subsection("What the prototype proves"),
    bullet("Customers can compare shops using real-time service information."),
    bullet("Services can be connected to employees qualified to perform them."),
    bullet("Queue and staff conditions can determine whether someone may join."),
    bullet("Walk-in and remote customers can share one queue."),
    bullet("Operating hours and service duration can produce a final acceptance time."),
    bullet("A merchant can manage the queue from a mobile interface."),
    bullet("English and Bisaya interfaces are feasible."),
    bullet("The interface can explain why an action is unavailable."),
    subsection("Strong design choices"),
    bullet("A clear promise: Find a service, check the line, take a number."),
    bullet("Large controls suitable for touch screens."),
    bullet("Visible price and expected service duration."),
    bullet("Separate waiting and currently served states."),
    bullet("Walk-in support and location links."),
    bullet("A privacy explanation before queue entry."),
    bullet("A sample clock for testing business-hour behavior."),
    subsection("Current limitations"),
    p("The Claude-hosted artifact is a demonstration, not a production service. Current constraints include:"),
    bullet("tab-local or contributor-restricted shared data;"),
    bullet("no public customer access independent of the artifact platform;"),
    bullet("no merchant-specific ownership and permissions;"),
    bullet("possible queue-number conflicts during simultaneous joins;"),
    bullet("no production backend, notifications, or future appointments;"),
    bullet("a long merchant settings screen; and"),
    bullet("sample businesses, services, prices, and queues rather than live operating data."),
    section("8", "Key usability improvements"),
    table(
        ["Issue", "Recommended improvement"],
        [
            ["Too many customer metrics", "Prioritize estimated wait and join availability; make operational details secondary."],
            ["Staff free: 0/2 may look unavailable", "Use clearer wording such as 2 staff working, both currently busy, next opening in 25 minutes."],
            ["Long merchant configuration", "Split settings into focused sections and preserve a fast daily queue desk."],
            ["Unclear post-join journey", "Add a dedicated ticket screen with position, arrival deadline, cancel, and notification status."],
            ["Manual status burden", "Derive availability and customer counts from ticket and employee state changes."],
        ],
        [55 * mm, 108 * mm],
    ),
    section("9", "Operational questions to resolve"),
    p("Trust depends on clear queue rules. Before production development, decide:"),
    bullet("How far away may a customer be when joining?"),
    bullet("How long does the customer have to arrive?"),
    bullet("What happens when a customer is absent when called?"),
    bullet("Can customers pause, cancel, or hold more than one ticket?"),
    bullet("May merchants reorder the queue or serve priority customers?"),
    bullet("Can customers request a specific employee?"),
    bullet("How are lunch breaks, split shifts, and temporary closures represented?"),
    bullet("How are fake entries, abuse, and inaccurate merchant information handled?"),
    bullet("Will future appointments and walk-in queues coexist?"),
    section("10", "Business model and market risk"),
    p(
        "Pila has a two-sided marketplace challenge: customers will not use it if too few shops participate, while merchants may not maintain it if too few customers use it. A broad Cebu launch across many service categories would therefore be risky."
    ),
    callout("Recommended launch: one service category, one compact area, three to five participating shops."),
    Spacer(1, 8),
    subsection("Potential revenue models"),
    bullet("Monthly merchant subscription."),
    bullet("Free basic plan with paid operational features."),
    bullet("Per-branch pricing for growing businesses."),
    bullet("Featured placement after the marketplace has meaningful demand."),
    bullet("Business analytics and customer-flow reporting."),
    p(
        "Merchant subscriptions are better aligned with the early value proposition than charging customers to enter a queue. Pricing should be validated through merchant interviews rather than assumed."
    ),
    section("11", "Validation research"),
    subsection("Questions for merchants"),
    bullet("How is the queue managed today, and when are the busiest periods?"),
    bullet("How often do customers leave because of the wait?"),
    bullet("Would staff consistently press start and done during busy periods?"),
    bullet("Would the business accept customers who join remotely?"),
    bullet("How long should customers have to arrive?"),
    bullet("Would the owner pay, and what monthly amount feels reasonable?"),
    subsection("Questions for customers"),
    bullet("Would they trust an estimated waiting time?"),
    bullet("Would they join remotely, and how far away would they be?"),
    bullet("Which information most strongly affects shop choice?"),
    bullet("Would they share a name or telephone number?"),
    bullet("Would they prefer browser, SMS, or Messenger notifications?"),
    p(
        "The most important validation question is whether merchants will operate the queue consistently during busy hours. The most important performance measure is the difference between the predicted wait and the customer's actual service start time."
    ),
    section("12", "Recommended minimum viable product"),
    table(
        ["Customer MVP", "Merchant MVP"],
        [
            ["Select a service and view nearby participating businesses.", "Secure merchant account and ownership of one shop."],
            ["See operating status, price, location, and estimated wait.", "Configure hours, temporary closures, services, prices, and duration."],
            ["Join the queue and receive a unique ticket.", "Manage employees, qualifications, and on-duty status."],
            ["See position, arrival deadline, and current status.", "Add walk-ins and perform call, start, complete, cancel, and no-show actions."],
            ["Confirm arrival, cancel, and receive a near-turn notification.", "Use automatic queue, staff, capacity, and waiting-time calculations."],
            ["Use English or Bisaya.", "Review basic daily operating statistics."],
        ],
        [81.5 * mm, 81.5 * mm],
    ),
    subsection("Postpone until after the pilot"),
    p(
        "Online payments, public reviews, advertising, loyalty programs, broad geographic coverage, multiple industries, advanced appointments, complex scheduling, promotions, and multi-branch management should wait until the core queue behavior is validated."
    ),
    section("13", "Production and technical requirements"),
    bullet("A public mobile-first web application or progressive web app."),
    bullet("A real-time database shared by customers and merchants."),
    bullet("Customer and merchant authentication with merchant-scoped permissions."),
    bullet("Transaction-safe queue-number allocation."),
    bullet("Live synchronization between customer and merchant screens."),
    bullet("Near-turn notifications and arrival confirmation."),
    bullet("Audit history, backups, monitoring, and error reporting."),
    bullet("Rate limiting and protection against repeated fake queue entries."),
    bullet("Fast performance on inexpensive Android phones and slow connections."),
    p(
        "Supabase or Firebase could support an early pilot. The final architecture should follow the confirmed operating rules rather than being selected before the workflows are settled."
    ),
    section("14", "Privacy and legal considerations"),
    p(
        "Pila may process names, telephone numbers, locations, and service history. A production service must follow the Philippine Data Privacy Act and apply data-minimization principles."
    ),
    bullet("Collect only information required to operate the queue."),
    bullet("Explain why data is collected and how long it is retained."),
    bullet("Do not expose customer names or contact details to other customers."),
    bullet("Limit each merchant to its own shop and queue records."),
    bullet("Protect customer and account data with appropriate access controls."),
    bullet("Obtain consent for SMS or other notification channels."),
    bullet("Provide a privacy notice and a process for data deletion requests."),
    p(
        "Clinics should not be part of the first pilot because medical-service information carries additional privacy and operational sensitivity."
    ),
    section("15", "Recommended development and rollout"),
    table(
        ["Phase", "Focus", "Evidence of success"],
        [
            ["1. Refine", "Simplify customer cards, define queue rules, and design the complete ticket journey.", "Customers understand whether to join without assistance."],
            ["2. Build", "Add merchant ownership, shared backend, automatic calculations, and notifications.", "Independent customers and merchants see synchronized queue state."],
            ["3. Pilot", "Onboard three to five barbershops in one Mandaue area.", "Shops operate the queue during real busy periods."],
            ["4. Measure", "Track joins, arrivals, no-shows, completion, and wait accuracy.", "Predicted and actual service-start times are acceptably close."],
            ["5. Expand", "Improve operations, then add shops, districts, or related service categories.", "Usage remains reliable as supply and customer demand grow."],
        ],
        [22 * mm, 76 * mm, 65 * mm],
    ),
    section("16", "Final assessment"),
    p(
        "Pila is a strong proof of concept for real-time service availability and virtual queue management. It solves a more immediate problem than a generic booking application by answering one practical question:"
    ),
    callout("If I go there now, can they serve me, and how long will I wait?"),
    Spacer(1, 9),
    p(
        "The prototype demonstrates that the concept can be translated into a usable product. The next challenge is not adding more features. It is proving that merchants will operate the queue consistently and that customers will trust the waiting-time estimate enough to act on it."
    ),
    p(
        "The most responsible next step is an independently hosted, narrowly scoped pilot with a small group of barbershops in one part of Mandaue. If merchants use the system consistently and customers rely on its estimates, Pila will have credible evidence for broader investment and expansion."
    ),
]


def build():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = PilaDocTemplate(str(OUTPUT_PATH))
    doc.build(story)
    print(OUTPUT_PATH)


if __name__ == "__main__":
    build()
