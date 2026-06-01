# Module 4 — Reflection

**Team name**: _______________
**Branch**: `module-04/<team-name>`
**Submitted**: before Module 5 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

In Module 3, services called each other directly over HTTP. Now activity-service drops a message into a broker and moves on — it never waits for a reply.

**What does the activity-service gain by not waiting? And what does the notification-service gain by consuming at its own pace?**

Think about what happens under load, or when notification-service is temporarily down.

> *Your answer:*
The activity-service doesn’t need to wait anymore, so it can respond faster and not get blocked if another service is slow.
The notification-service can process messages at its own speed, even if it is slow or temporarily down, because messages stay in the queue.

---

## 2. Your choice

In Module 3 you already knew how to call another service directly over HTTP — you did it for user validation and game enrichment.

**Why not use the same approach for notifications? What does introducing a broker give you that a direct HTTP call doesn't?**

Think about what happens if notification-service is slow, or crashes mid-message.

> *Your answer:*
We don’t use direct HTTP calls because it would tightly connect the services. If the notification-service crashes or is slow, it would affect the activity-service.
With a broker, the activity-service just sends a message and continues. This makes the system more stable and independent.

---

## 3. The tradeoff

With synchronous REST, you get an immediate answer: success or failure. With async messaging, the activity is saved and the message is sent — but you have no idea if the notification was ever delivered.

**How would a user know if their notification was never sent? How would you know as a developer?**

What visibility do you lose when you go async?

> *Your answer:*
With async messaging, we don’t know immediately if the notification was delivered or not. It might fail without us knowing right away.
To check this, we would need logs or monitoring on the consumer or message queue.

---

*Keep this file. You will refer back to it during the oral presentation.*
