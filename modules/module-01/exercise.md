# Module 1 — Service Decomposition

**Duration**: 2h in class
**Branch to submit**: `module-01/<team-name>`

---

## Objective

Before writing a single line of code, you need to design the system on paper. Every decision you make here: where to draw service boundaries, who owns what data, how services talk to each other, is hard to reverse once you start coding.

This module is about slowing down and thinking like an architect, not a developer.

Read these two documents before doing anything else:

- `docs/domain.md` — what GameHub is and who uses it
- `docs/specs.md` — the tech stack and key architectural decisions

> The CTO has already laid out the `services/` folder structure. Use it as a starting point, but your job is to **justify** why each folder deserves to be its own service — not just accept it.

---

## Task 1 — Identify bounded contexts _(~40 min)_

A bounded context is a part of the system that has a clear responsibility and owns its data exclusively. No other service should reach into its database.

For each bounded context you identify, fill in the table:

| Bounded Context | Responsibilities                                                        | Owned Entities   | Team     |
| --------------- | ----------------------------------------------------------------------- | ---------------- | -------- |
| Identity        | Manages who users are, handles registration and profiles                | User, Session    | Platform |
| Game Library    | Tracks which games exist, their metadata, genres, and enables discovery | Game, Genre, Tag | content  |
 Notifications      | Reacts to events and delivers messages to users (in-app, email, push) | Notification, NotificationPreference | Platform |
|Auth & Security    | Issues and validates JWT tokens, manages credentials and access control | Token, Credential | Platform  |

There is no single correct answer: what matters is that you can justify each row.

---

## Task 2 — Define service contracts _(~30 min)_

For each pair of services that need to communicate, define:

- **Direction**: A → B
- **Trigger**: what causes the call
- **Protocol**: REST or event (async)
- **Payload**: key fields exchanged

Example:

```
activity-service → logging-service
Trigger: an activity is logged
Protocol: RabbitMQ message (async — why not REST here?)
Payload: { activity_id, user_id, action, game_id, timestamp }
```
gateway → auth-service
Trigger: any incoming client request with a Bearer token
Protocol: REST (sync — must validate before forwarding)
Payload: { token } → response: { user_id, roles, valid: true/false }

gateway → user-service / game-service / activity-service
Trigger: validated request is forwarded to the correct service
Protocol: REST (sync — path-based routing)
Payload: original request + injected { user_id } from decoded JWT

activity-service → RabbitMQ → logging-service
Trigger: a user performs a tracked action (play, add game, review)
Protocol: RabbitMQ message (async — logging must never block the action)
Payload: { activity_id, user_id, action, game_id, timestamp }

logging-service → (internal consent check)
Trigger: an activity event is received from RabbitMQ
Protocol: internal DB lookup (no inter-service call)
Payload: checks ConsentRecord for user_id before writing ActivityLog

Focus on the flows that feel non-obvious. You do not need to document every possible pair.

---

## Task 3 — Draw the service map _(~20 min)_

Draw the full GameHub service map:

- One box per service
- Arrows between services (solid line = synchronous REST, dashed line = async event)
- Label each arrow with its protocol
- One box at the top labelled **gateway** — all client requests enter here, no client ever calls a service directly

This can be a sketch on paper, a whiteboard photo, or ASCII art committed to your branch.

Answer to this can me found in serviceMap.md inside the module-01 folder

---

## Discussion _(~15 min)_

Three questions to discuss as a team before you leave:

1. Why does `notification-service` use Node.js instead of Python like the rest? What does that tell you about microservices and technology choices?
Answer:
Node.js handles real-time, event-driven tasks well (things like pushing notifications). But the real point is that microservices let each service pick the right tool for the job. Since notification service sits behind RabbitMQ, nothing else cares what language it uses

2. What is the risk of `activity-service` calling `logging-service` synchronously — why might you prefer an async event instead?
Answer:
If logging-service goes down or gets slow, the user's action fails too ,even though nothing actually went wrong on their end. Async means activity-service doesn't wait. The log gets written eventually, and a temporary outage in logging doesn't affect the user at all

3. Why does `logging-service` need a GDPR consent check before recording any activity?
Answer:
You legally can't record that without the user's permission. So logging-service checks consent before writing anything. No consent, no log 

You do not need to write these answers down — they are warm-up for your REFLECTION.md.

---

## Minimum to submit this branch

- [ ] Bounded context table filled in (at least 4 services justified)
- [ ] At least 3 service contracts defined
- [ ] Service map committed (sketch, photo, or ASCII)
- [ ] `REFLECTION.md` completed and committed

The map does not need to be perfect. It needs to be yours.
