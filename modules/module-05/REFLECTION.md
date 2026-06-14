# Module 5 — Reflection

**Team name**: _______________
**Branch**: `module-05/<team-name>`
**Submitted**: before Module 6 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

The game-service now has two models for the same data: SQLite for writes, Redis for reads. They store the same games in two different shapes.

**Why go through the trouble of maintaining two representations of the same data?**

Think about what kind of queries each model is optimised for, and what would happen if you tried to use the write model for high-traffic read operations.

> *Your answer:*
SQLite is good for writes but if you hammer it with thousands of reads it gets slow. Redis is in-memory so reads are instant. Game summaries get read way more than they get created, so having a fast read model just makes sense.

---

## 2. Your choice

The logging-service checks GDPR consent before recording any activity. If a user has not opted in, the log is silently dropped.

**What does this consent check force you to accept about your data?** It is incomplete by design — some activities will never be recorded.

From a system design perspective: where is the right place to enforce this rule — in the logging-service, in the activity-service, or at the gateway? Why?

> *Your answer:*
It means your logs will always be incomplete and that's intentional. Some activities just never get recorded because the user said no.
It belongs in the logging-service. The gateway doesn't know or care about GDPR. The logging-service is the one writing personal data so it's the one that should decide if it's allowed to.

---

## 3. The tradeoff

With CQRS, your write model and read model can drift out of sync — a game is updated in SQLite but the Redis projection still shows the old data.

**In what scenario does this inconsistency matter to the user? In what scenario is it completely acceptable?**

Is there a class of applications where eventual consistency is never acceptable? What are they?

> *Your answer:*
It matters when someone updates a game and immediately checks the summary, they'll see the old data which feels wrong. It's fine for things like trending games or stats where being a few seconds behind doesn't matter.