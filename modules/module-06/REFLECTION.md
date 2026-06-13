# Module 6 — Reflection

**Team name**: _______________
**Branch**: `module-06/<team-name>`
**Submitted**: before Module 7 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

The gateway now validates every JWT before forwarding a request. Individual services no longer need to check identity themselves.

**What does centralising authentication at the gateway buy you?** What would the alternative look like — if every service validated tokens on its own?

Think about what happens when you need to rotate the secret key, or add a new service to the system.

> *Your answer:*
If every service validates tokens on its own, you have to update all of them every time the secret key changes or you add a new service. With the gateway doing it centrally, there's one place to change and everything else just works. It also means new services don't need to care about auth at all the gateway handles it before the request even reaches them.

---

## 2. Your choice

When activity-service calls user-service internally, it uses a Machine-to-Machine (M2M) token — not a user's token.

**Why can't it just reuse the user's token that arrived in the original request?**

What would break, or what door would you accidentally leave open, if services passed user tokens between themselves?

> *Your answer:*
If activity-service reuses the user's token, it's acting as that user internally which it shouldn't be. The user didn't ask activity-service to call user-service on their behalf. It also means if a user's token gets compromised, it could be used to make internal service calls. M2M tokens are scoped to the service, not the user, so the permissions stay separate.

---

## 3. The tradeoff

The gateway and the auth-service share the same `SECRET_KEY` to verify tokens without making a network call on every request.

**What is the security risk of sharing this key?** What happens if it leaks?

And what would the alternative look like — verifying tokens by calling auth-service on every request instead? What does that cost you?

> *Your answer:*
If the secret key leaks, anyone can forge valid tokens and get through the gateway. That's a big deal. But the alternative calling auth-service on every single request to verify tokens adds a network hop to every request, and if auth-service goes down, the whole system stops working. Sharing the key is faster and more resilient, but you have to keep it safe.

---

*Keep this file. You will refer back to it during the oral presentation.*
