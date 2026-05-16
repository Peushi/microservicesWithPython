## YOU NEED TO COMMIT THIS FILE BEFORE MOVING ON TO THE NEXT MODULE ! 🚨

**feel free to delete this comment**

# Module 1 — Reflection

**Team name**: **\*\***\_\_\_**\*\***
**Branch**: `module-01/<team-name>`
**Submitted**: before Module 2 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

You started from a painful monolith. Now you're splitting it into separate services.

**What concrete problem does that split solve: and for whom?**

Think about it from three angles: the developer who has to change code, the team that has to deploy it, and the user who has to live with its failures. You don't need to cover all three, pick the one that felt most real to you today.

> _Your answer:_
In a monolith, if you break something, everything breaks. Here, if notification-service goes down, users can still log in, browse games, and track their activity. The failure stays contained. That's the main thing the split gets you, one service's problem doesn't become everyone's problem.

---

## 2. Your choice

Look at your service map. Every arrow between two services is a decision someone made.

**Pick one boundary, one place where you decided service A should not be part of service B. Explain why that line exists.**

What would break, slow down, or become harder to manage if you merged those two services back together?

> _Your answer:_
I kept logging-service separate from activity-service. Logging is not the main job, it's a side effect. If they were the same service, a slow GDPR check could make adding a game to your library feel slow. Keeping them apart means logging happens in the background and nobody waits for it.

---

## 3. The tradeoff

Microservices solve the monolith's problems. But they create new ones.

**Name one thing that was simpler in the monolith and is now harder in your distributed design.**

No need to solve it: just name it honestly. This is exactly the tension the rest of the course is about.

> _Your answer:_
Debugging. In a monolith you have one place to look. Here, if something breaks, you don't know if it was the gateway, the service, or RabbitMQ. You have to check logs in multiple places just to understand what happened. It's a lot more painful to trace a bug across five services than one.

---

_Keep this file. You will refer back to it during the oral presentation._
