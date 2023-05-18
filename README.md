# Architecture Patterns with Python

Implementation of common architecture patterns. Inspired by the book [Architecture Patterns with Python](https://www.cosmicpython.com/).

This repository is just a playground.
Implemented solutions can serve as an inspiration for production-grade solutions, but author does not guarantee the full correctness.

## Implemented

1. Domain Model with Aggregate
2. Repository pattern
3. Unit of Work pattern
4. Ports layer - Abstraction
5. Adapters layer - Implementation
6. Dependency Injection
7. Event Driven Architecture
8. Command Bus
9. Command handlers - Service layer
10. Event Bus
11. Event Listeners
12. Event Publisher
13. Event Consumers - workers
14. CQRS pattern
15. Postgres backed Command responsibility
16. Redis backed Cache Query responsibility
17. Event based Cache Query updates
18. REST API - Presentation layer

## Visualization

![https://miro.com/app/board/uXjVPlqi-70=/?share_link_id=17264820398](/visualization/2023-02-28-architecture-patterns-with-python.jpg)

To see more details go to the [Miro board](https://miro.com/app/board/uXjVPlqi-70=/?share_link_id=17264820398).

## Work in progress

1. Robust logging system
2. Unit, Intergration and E2E tests

## Dev Notes

1. Naming conventions
   1. If you want to keep all models/repositories/whatever in one module, use the plural name.
   2. If you want to keep models/repositories/whatever in more than one module within a package, use the plural name for the package and the singular name for each module.
   3. Thanks to this approach you can make the package from one module with all repositories without updating imports in the entire codebase.
2. Database layer
   1. With the current setup database layer should not go beyond the adapters layer.
   2. Models should be stored in the database layer. One module or package for one logical part of the app.
   3. Mapping of models to domain models should be done in the adapters layer.
   4. Alternative approach would be to implement a kind of "entity framework" that would map models to domain models automatically.
   5. One of solutions, as described in the book, would be to invert the dependency by using SQLAlchemy classical mapping. ORM would depend on the domain model then.
3. Adapters
   1. Implementation specific.
   2. The goal is to have it easily replaceable once you decide to integrate with a new external service.
   3. Adapters have to be based on abstractions to make it possible to configure dependency injection on ports level.
4. Pydantic models
   1. There is a problem with parsing sets when parsing the object to json/dict or the other way around. Use lists instead.
