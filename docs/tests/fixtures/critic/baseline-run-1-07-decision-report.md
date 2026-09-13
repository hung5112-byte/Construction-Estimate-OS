---
type: decision_report
stop: 1
---
## 📌 Bottom line (30-second read)

- The chip inside our two mobile internet tablets (CY-80L at $389 and CY-80R at $169) is being discontinued — we have 30 weeks to buy remaining stock or we lose both revenue streams.
- We recommend approving a bulk "last chance" purchase order now, but holding the actual signing until Week 4 when we have real sales numbers, supplier pricing, and refurbishment demand confirmed.
- Engineering believes a chip swap is a dead end and prefers a full redesign; every other department disagrees — this conflict must be resolved in writing by Week 1 before any engineering money is spent.
- A full product redesign takes up to 30 months and is ruled out as an immediate fix; the bulk purchase is the only option that guarantees no gap in product supply.
- Any purchase order over $50,000 needs VP sign-off, and if total committed spend exceeds $1.02M, it must be escalated before the order is placed.

---

# Decision Report: Main Processing Chip Discontinued — What We Do Next

## 📌 Summary (30-second read)

The main processing chip inside our **CY-80L** tablet has been discontinued by its maker. The CY-80L is our only tablet with mobile internet capability. It sells for $389 and earns a 39% profit margin.

We have **30 weeks** to place a bulk purchase order before the chip supply disappears completely.

Here is what we recommend:

- **Place a bulk "last chance" purchase order by Week 4.** This is the only option that guarantees we never run out of stock. Start collecting real sales data and supplier pricing *this week*, because the size of that order is the whole financial decision — and right now we have no confirmed volume number to base it on.
- **At the same time, begin finding a replacement chip** as our long-term solution. However, do not spend money on engineering or certifications until at least two suitable replacement chips have been identified and we have a real cost estimate. That decision point is Week 6.
- **Do not redesign the product from scratch as an immediate fix.** A full redesign takes 18 to 30+ months. We would be deliberately abandoning an active, profitable product with nothing ready to replace it.
- **This affects two products, not one.** The same chip also powers our **CY-80R** refurbished tablet ($169, 24% margin). Failing to act puts income from both products at risk simultaneously.

---

## Recommendation

**Proceed — with conditions.** Approve the bulk purchase plan in principle today. Hold the actual purchase order until Week 4, when three essential pieces of information will be ready.

---

## What Changed from the Original Brief

| Item | Original brief | This recommendation | Why |
|---|---|---|---|
| Which option to prioritise | Compare all three options equally | Bulk purchase first; replacement-chip search in parallel; full redesign rejected | All six departments agreed; the 30-week deadline makes the bulk purchase unavoidable regardless of what we do long-term |
| Timing of the purchase order | Not specified | Issue the order in Week 4 — not Week 3, not Week 5 | Week 3 relies on guessed numbers; Week 5 wastes precious time; Week 4 is achievable if data collection starts in Week 1 |
| How much to order | Not specified | Order enough to cover the **worst-case timeline for finding a replacement chip (44 weeks), plus a 15% safety cushion** | Ordering too little still creates a supply gap; ordering too much ties up cash but at least keeps products on shelves |
| When to commit engineering money to the replacement-chip search | Not specified | Not before Week 6, and only after at least 2 replacement chips are confirmed and costs are itemised | The current cost estimate has a 2× range ($150,000–$300,000); engineering spend that cannot be recovered should not be approved on a rough estimate |
| Full redesign | Listed as a comparable option | Formally ruled out as an immediate solution; flagged as a possible future successor programme | Getting a redesigned product into full production takes 18 to 30+ months; the product on sale today cannot wait that long |
| Engineering team's preference | Not addressed | Must be confirmed in writing by Week 1 | Different departments have read Engineering's preference differently; this determines whether the replacement-chip route is worth funding at all |

---

## Detailed Analysis

### What Each Department Said

**Hardware Engineering:** Lock in the bulk purchase immediately as a short-term bridge. For the long term, pursue a full redesign — not a chip swap. Engineering explicitly called the chip-swap route "the trap." Their reasoning: swapping the main chip almost certainly triggers costly government safety re-approvals, plus hidden software rewrite costs. Realistic total for the chip-swap route: 20–30 weeks and $100,000–$140,000 *before* any safety certification begins. Engineering recommends abandoning the chip-swap path.

> ⚠️ **Important conflict:** Engineering is the *only* department that prefers a full redesign over a chip swap as the long-term solution. Every other department treats the chip swap as the parallel track. This disagreement must be settled in Week 1. Spending engineering money on a route that Engineering believes is a dead end is money we cannot get back.

**New Product Introduction (NPI) Programme Management** *(the team that shepherds new products from concept to full production)*: The 30-week deadline is firm and non-negotiable. They recommend issuing the bulk purchase order within 2 weeks, running the chip-swap qualification in parallel, and treating the full redesign as a long-term option only. They also flagged that the chip-swap approval process and the bulk purchase window dangerously overlap if we delay. They confirmed that the **AMG-100** — another product currently in late-stage testing before production — is not yet in full production and *cannot* fill the gap left by a CY-80L shortage.

> **AMG-100** *(a product currently undergoing final pre-production testing — it is not yet available to sell or to substitute for the CY-80L)*

**Quality & Reliability:** Endorsed the bulk purchase as the lowest-risk bridge, but recommended sizing it conservatively — 12 to 18 months of supply, not 3 years. Three important additions:
1. Inspection standards for incoming bulk-purchase stock must be written *before the first delivery arrives* — those standards do not currently exist.
2. The first three deliveries of any replacement chip must be tested at the highest inspection level.
3. Chips made late in a product's life can carry subtle faults that cause "no fault found" returns in the field — the hardest kind of problem to diagnose. They also confirmed that a quality escape on the CY-80L would damage the CY-80R refurbished unit supply as well. **Two products are at risk, not one.**

> **"No fault found" return** *(a product sent back by a customer that appears to work fine when tested — caused by subtle chip behaviour that is hard to reproduce in a lab)*

**Manufacturing & Supplier Quality:** Agreed on bulk purchase plus parallel chip-swap search. Critical addition: **lock reference ("golden") samples and production test limits this week**, before any bulk-purchase stock ships. Without frozen test limits, chip variation across a large order could create two subtly different versions of the CY-80L in the field. On a payment device, a testing failure is a **PCI** *(Payment Card Industry — the security standard that governs any device that handles card payments)* compliance risk, not just a production waste problem. Also: no stock from third-party brokers — the bulk purchase must come with a **Certificate of Conformance (COC)** *(a document from the manufacturer confirming the parts meet the agreed specification)* and date stamps showing when the chips were made. Finding and qualifying a replacement chip takes a minimum of 12 to 16 weeks from a standing start.

**Service Operations:** Raised the "double exposure" point most clearly — both the CY-80L production line and the CY-80R refurbishment pool depend on the same chip. There is no substitute product that provides mobile internet; the CY-80R cannot simply be swapped in for the CY-80L without a formally approved product configuration change. They also costed the shipping difference: bulk ocean freight for the purchase order runs approximately $8–$12 per kg; expedited air freight during the chip-swap phase adds two to three extra air shipments at $18–$25 per kg; a delayed full redesign could add $40,000–$80,000 in unplanned freight costs — against a budget that currently has no freight line item.

**Finance:** Approved in principle — but with conditions. Key points:
1. Bulk-purchase stock is recorded as an asset on the balance sheet the moment the order is placed — it is illiquid and exposed to write-off if the product is discontinued before stock sells out.
2. Engineering spend on the chip-swap route is a direct operating expense — it is gone whether the route succeeds or not.
3. The $6.8M annual budget has no departmental breakdown on record; spending cannot be formally approved without a named budget owner.
4. Any purchase order above $50,000 requires **VP** *(Vice President — a senior executive one level above Department Head)* approval. Any draw on contingency funds above $25,000 must go to the **Change Control Board (CCB)** *(a small committee that reviews and approves significant unplanned spending or project changes)* with a written decision log entry. Finance will support the bulk purchase if the break-even volume calculation works — but no order will be signed without a completed financial model.

---

### The Case For and Against

**Reasons to act now (bulk purchase + chip-swap search in parallel):**
- Every week without a purchase order is a week of the 30-week window gone, with zero stock secured.
- Each CY-80L unit earns $151.71 in gross profit (39% × $389). Every unit we cannot ship is profit lost.
- Bulk-purchase inventory is recorded as an asset, not an expense — it pays for itself as units sell.
- The chip-swap re-qualification realistically takes 24 to 44 weeks. The bulk purchase is the *only* option that guarantees no gap in supply.
- A full redesign takes 18 to 30+ months. Abandoning an active, profitable product with nothing ready to replace it is indefensible against our target of keeping 99.5% of our devices running by 2030.

**Reasons not to sign an order yet (wait for real data):**
- We have no confirmed monthly sales volume for the CY-80L. The "500 units per month" figure being discussed is illustrative — not verified from our business system.
- A 2× error in that assumed run-rate produces either 17.5 months of stock (too much cash tied up) or 4.4 months of stock (still a supply gap).
- The CY-80R refurbishment programme's chip usage has not been separated out from production demand — sizing the order against production only will leave the refurb programme short mid-window.
- Bulk-purchase unit pricing and the **minimum order quantity (MOQ)** *(the smallest number of units the supplier will sell in one order — buying less than this is not an option)* are unconfirmed. Suppliers commonly charge a premium for end-of-life stock.
- The chip-swap engineering cost estimate ($150,000–$300,000) has a 2× range. That range likely does not fully capture government re-certification lab fees and software labour costs.

**Conclusion:** Both sides are right in their own area. The bulk purchase is necessary. The data must be collected before the order is signed. The answer is **Week 4** — not Week 3, not Week 5.

---

### Three Ways to Look at It

**Growth-focused view:** Issue the purchase order by Week 3. Begin the replacement-chip supplier search immediately. The 30-week window is running now — every week of debate is a week consumed. Size the order generously. Running out of stock on a 39% margin product causes customers to leave, and winning them back is expensive. Rule out the full redesign for the CY-80L; formally scope it as a future new product programme for the successor device.

**Cautious view:** Do not sign a purchase order until three specific inputs are confirmed — verified monthly sales from our business system, CY-80R refurb chip usage, and firm supplier pricing. Set explicit spending limits: escalate to the VP if the committed spend exceeds $1.02M (15% of the $6.8M budget); cancel if it exceeds $1.36M (20%). Define a cancellation trigger for the chip-swap route (if no qualifying replacement chips are found, redirect to redesign). Week 5 at the earliest for the purchase order. Engineering's formal preference must be documented before any engineering money is committed.

**Balanced view (this report's recommendation):** Week 4 purchase order, with data collection starting in Week 1 immediately. Size the order against the worst-case chip-swap timeline (44 weeks) plus a 15% safety cushion. Lock Engineering's formal preference in Week 1 — it determines whether the chip-swap or the full redesign is the real long-term solution. Write incoming inspection standards before the first delivery. Gate engineering spending at Week 6, only after at least 2 confirmed replacement chip candidates and an itemised cost estimate are in hand.

---

## What Must Happen Before We Can Proceed (Blockers)

> **Blockers** *(tasks that must be completed before the next step can proceed — if any one of these is missing, we cannot safely move forward)*

### Before the Purchase Order Is Signed

- [ ] **Pull actual CY-80L monthly sales figures from our business system** — minimum last 6 months. *Owner: NPI Programme Management. Deadline: Week 1.* No real order quantity is possible without this.
- [ ] **Pull CY-80R refurbishment chip usage separately** from production demand. *Owner: Service Operations. Deadline: Week 1.*
- [ ] **Get firm bulk-purchase unit pricing and minimum order quantity from the chip supplier** — no third-party broker stock; require a Certificate of Conformance and manufacture date stamps. *Owner: Manufacturing & Supplier Quality. Deadline: Weeks 1–2.*
- [ ] **Get Engineering's formal written position: chip swap or full redesign as the intended long-term solution.** *Owner: NPI Programme Management (coordinating with Hardware Engineering). Deadline: Week 1.* This determines whether chip-swap engineering spending is well-spent or a detour.
- [ ] **Write bulk-purchase incoming inspection standards** — first three deliveries of any replacement chip must be tested at the highest inspection level or 100% electrical screen. *Owner: Quality & Reliability. Deadline: Before the first delivery arrives.*
- [ ] **Freeze reference ("golden") samples and production test limits.** *Owner: Manufacturing & Supplier Quality + the contract manufacturer's quality team. Deadline: This week, before any stock ships.*
- [ ] **Model the required order quantity across three chip-swap timeline scenarios** (best case 28 weeks / mid case 34 weeks / worst case 44 weeks), including CY-80R refurb demand, using actual sales figures. *Owner: NPI Programme Management + Finance. Deadline: Week 2.*
- [ ] **Check the purchase order commitment against the Finance escalation limit** — if the total committed spend exceeds $1.02M (15% of the $6.8M annual budget), escalate to the VP before signing. *Owner: Finance. Deadline: Week 2.*
- [ ] **Produce a departmental budget breakdown** — the $6.8M annual budget has no departmental split on record; spending cannot be formally approved without a named budget owner. *Owner: Finance (Controller). Deadline: Before the purchase order is authorised.*

### Before Engineering Spend on the Chip-Swap Route Is Committed

- [ ] **Identify at least 2 replacement chip candidates** with confirmed technical compatibility (pin layout and communication protocol). *Owner: Manufacturing & Supplier Quality + Engineering. Deadline: Weeks 4–5.* A single replacement source is not supply-chain resilience.
- [ ] **Produce an itemised chip-swap engineering cost estimate** broken out by work area: chip integration, software update, payment security re-certification, government radio approval lab fees, product safety lab fees, software labour. *Owner: Engineering. Deadline: Week 5.* The current $150,000–$300,000 range is too wide to support a budget approval.
- [ ] **Confirm the import tariff classification** *(the official customs code that determines what import duty applies)* for any replacement chip before freight is booked. *Owner: Logistics / Service Operations. Deadline: Before any replacement chip material ships.*

---

## Progress Checkpoints

| Week | What we measure | Minimum acceptable result | What happens if the target is missed |
|---|---|---|---|
| Week 1 | Verified monthly sales figure pulled from our business system and in the financial model | Must exist | Escalate to Department Head; do not size the order on assumed numbers |
| Week 1 | Engineering's written position confirmed (chip swap vs. redesign) | Must exist | Block all engineering spending; Department Head decides the path before any money is committed |
| Week 2 | Firm supplier pricing and minimum order quantity confirmed | Must exist | Delay purchase order to Week 5; assess cancellation if the minimum order forces a commitment above $1.36M |
| Week 2 | CY-80R refurb chip usage separated from production demand | Must exist | Do not sign the purchase order — the order will be undersized |
| Week 4 | Purchase order signed, sized to worst-case chip-swap timeline + 15% cushion | Order placed | If not signed by Week 5, escalate — the window begins to meaningfully constrain how much stock we can secure |
| Week 6 | At least 2 replacement chip candidates confirmed with technical compatibility | 2 qualified candidates | If 0 or 1 found: pause chip-swap engineering spending; formally start a redesign programme |
| Week 6 | Itemised chip-swap engineering cost estimate produced | Must be line-by-line, not a range | Block engineering spend approval until scope is defined |
| Week 8 | Engineering spend on chip-swap route committed (if 2+ candidates confirmed) | Spending order issued | If delayed past Week 10, the chip-swap timeline shifts right and the bulk purchase may need topping up |
| Week 20 | Replacement chip technical integration complete; software update started | Milestone hit | If missed: assess whether the bulk-purchase quantity

---

## ⚠️ Warning: claims missing a source

The following sentences contain figures or legal references but no clear citation was found. The Department Head should verify them before proceeding:

- **[Line 7] Figure:** - The chip inside our two mobile internet tablets (CY-80L at $389 and CY-80R at $169) is being discontinued — we have 30 weeks to buy remaining stock or we lose both revenue streams.
- **[Line 9] Figure:** - Engineering believes a chip swap is a dead end and prefers a full redesign; every other department disagrees — this conflict must be resolved in writing by Week 1 before any engineering money is spe
- **[Line 10] Figure:** - A full product redesign takes up to 30 months and is ruled out as an immediate fix; the bulk purchase is the only option that guarantees no gap in product supply.
- **[Line 11] Figure:** - Any purchase order over $50,000 needs VP sign-off, and if total committed spend exceeds $1.02M, it must be escalated before the order is placed.
- **[Line 19] Figure:** It sells for $389 and earns a 39% profit margin.
- **[Line 21] Figure:** We have **30 weeks** to place a bulk purchase order before the chip supply disappears completely.
- **[Line 28] Figure:** - **This affects two products, not one.** The same chip also powers our **CY-80R** refurbished tablet ($169, 24% margin).
- **[Line 55] Figure:** Realistic total for the chip-swap route: 20–30 weeks and $100,000–$140,000 *before* any safety certification begins.
- **[Line 59] Figure:** They recommend issuing the bulk purchase order within 2 weeks, running the chip-swap qualification in parallel, and treating the full redesign as a long-term option only.
- **[Line 63] Figure:** **Quality & Reliability:** Endorsed the bulk purchase as the lowest-risk bridge, but recommended sizing it conservatively — 12 to 18 months of supply, not 3 years.
- **[Line 70] Figure:** Finding and qualifying a replacement chip takes a minimum of 12 to 16 weeks from a standing start.
- **[Line 72] Figure:** They also costed the shipping difference: bulk ocean freight for the purchase order runs approximately $8–$12 per kg; expedited air freight during the chip-swap phase adds two to three extra air shipm
- **[Line 77] Figure:** The $6.8M annual budget has no departmental breakdown on record; spending cannot be formally approved without a named budget owner.
- **[Line 78] Figure:** Any purchase order above $50,000 requires **VP** *(Vice President — a senior executive one level above Department Head)* approval.
- **[Line 78] Figure:** Any draw on contingency funds above $25,000 must go to the **Change Control Board (CCB)** *(a small committee that reviews and approves significant unplanned spending or project changes)* with a writt
- **[Line 86] Figure:** - Each CY-80L unit earns $151.71 in gross profit (39% × $389).
- **[Line 88] Figure:** - The chip-swap re-qualification realistically takes 24 to 44 weeks.
- **[Line 89] Figure:** Abandoning an active, profitable product with nothing ready to replace it is indefensible against our target of keeping 99.5% of our devices running by 2030.
- **[Line 93] Figure:** - A 2× error in that assumed run-rate produces either 17.5 months of stock (too much cash tied up) or 4.4 months of stock (still a supply gap).
- **[Line 96] Figure:** - The chip-swap engineering cost estimate ($150,000–$300,000) has a 2× range.
- **[Line 104] Figure:** Running out of stock on a 39% margin product causes customers to leave, and winning them back is expensive.
- **[Line 106] Figure:** Set explicit spending limits: escalate to the VP if the committed spend exceeds $1.02M (15% of the $6.8M budget); cancel if it exceeds $1.36M (20%).
- **[Line 108] Figure:** Size the order against the worst-case chip-swap timeline (44 weeks) plus a 15% safety cushion.
- **[Line 118] Figure:** - [ ] **Pull actual CY-80L monthly sales figures from our business system** — minimum last 6 months.
- **[Line 122] Figure:** - [ ] **Write bulk-purchase incoming inspection standards** — first three deliveries of any replacement chip must be tested at the highest inspection level or 100% electrical screen.
- **[Line 124] Figure:** - [ ] **Model the required order quantity across three chip-swap timeline scenarios** (best case 28 weeks / mid case 34 weeks / worst case 44 weeks), including CY-80R refurb demand, using actual sales
- **[Line 125] Figure:** - [ ] **Check the purchase order commitment against the Finance escalation limit** — if the total committed spend exceeds $1.02M (15% of the $6.8M annual budget), escalate to the VP before signing.
- **[Line 126] Figure:** - [ ] **Produce a departmental budget breakdown** — the $6.8M annual budget has no departmental split on record; spending cannot be formally approved without a named budget owner.
- **[Line 131] Figure:** Deadline: Week 5.* The current $150,000–$300,000 range is too wide to support a budget approval.
