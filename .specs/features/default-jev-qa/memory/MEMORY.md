# Shared build memory

- Browser Harness models IPC timeouts as `TimeoutError` subclasses. Jev initializes and observes its dedicated page during `Agent` construction; the action loop begins only when `Agent.run()` is called. See the official sources linked in `plan.md`.
