# Module 3 — Reflection

**Team name**: _______________
**Branch**: `module-03/<team-name>`
**Submitted**: before Module 4 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

All client requests now go through the gateway. No client ever calls a service directly.

**Why does that single entry point exist? What would the client's life look like without it?**

Think about what the client would need to know and manage if it talked to each service on its own port.

> *Your answer:*
The gateway gives the client one single entry point. Without it, the client would need to know different ports and URLs for every service. The gateway makes the system easier to manage and hides the internal service structure.

---

## 2. Your choice

The activity-service makes two outbound calls: one to validate the user (with retry logic), one to fetch game data (with a null fallback if it fails).

**Why are these two calls treated differently? Why does one retry and the other just give up gracefully?**

What is the consequence for the user in each case if the downstream service is unavailable?

> *Your answer:*
User validation is important because we should not create activities for users that do not exist. That is why it retries once before failing. Game data is only extra information, so if game-service is down, the activity can still be saved with `"game": null`.


---

## 3. The tradeoff

Every time a client creates an activity, three services are involved synchronously. They all have to be running, healthy, and fast.

**What is the systemic risk of chaining synchronous calls like this?**

What happens to the user experience if the slowest service in the chain takes 3 seconds to respond?

> *Your answer:*
The risk is that one slow service slows down the whole request. If one service takes 3 seconds, the user waits longer for the full response. If a service goes down, some requests may fail completely.
---

*Keep this file. You will refer back to it during the oral presentation.*
