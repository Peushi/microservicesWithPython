```
                        +--------+
                        | Client |
                        +--------+
                             |
                           HTTP
                             |
                             v
          +------------------------------------------+          +----------------+
          |                Gateway                   | --REST--> |  auth-service  |
          |        port 8000 · JWT · routing         | <-verify- |   port 8005    |
          +------------------------------------------+          +----------------+
               |              |                |
             REST            REST             REST
               |              |                |
               v              v                v
      +--------------+  +-------------+  +----------------+
      | user-service |  | game-service|  |activity-service|
      |  port 8001   |  |  port 8002  |  |   port 8003    |
      +--------------+  +-------------+  +----------------+
                                                  |
                                              publish
                                            (async event)
                                                  |
                                                  v
                                         +----------------+
                                         |   RabbitMQ     |
                                         |   port 5672    |
                                         +----------------+
                                          /              \
                                      consume          consume
                                     (async)           (async)
                                        /                  \
                           +---------------------+   +-----------------+
                           | notification-service|   | logging-service |
                           |  port 8004 · Node.js|   | port 8006 · Flask|
                           +---------------------+   +-----------------+


Key:
  ------>   Synchronous REST
  - - ->    Async event (RabbitMQ)

```
