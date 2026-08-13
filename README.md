# PJ-CORE Control Dashboard

Единый premium command center экосистемы PJ-COM.

## Текущий статус

Репозиторий содержит действующий визуальный прототип Control v1 и утверждённый implementation baseline для **PJ-CORE Control Dashboard v2**.

V2 объединяет:
- новый адаптивный интерфейс PJ-CORE Control;
- backend/data functionality legacy `pj-c0m/pj-core`;
- проекты, focus, priority, progress;
- идеи и их состояния;
- Global Inbox;
- tools;
- agents;
- Telegram intake;
- Activity Engine;
- Wiki/GitHub sync;
- premium Control Board / Expanded Card / Project Workspace.

`data/projects.json` является временным источником текущего прототипа и не является целевой primary storage архитектурой v2.

## Implementation documentation

Главная спецификация: [`docs/00-MASTER-SPECIFICATION.md`](docs/00-MASTER-SPECIFICATION.md)

Полный пакет:

1. [`docs/00-MASTER-SPECIFICATION.md`](docs/00-MASTER-SPECIFICATION.md) — продукт и scope.
2. [`docs/01-UX-UI-SPECIFICATION.md`](docs/01-UX-UI-SPECIFICATION.md) — premium UX/UI, cards, workspace, motion, mobile.
3. [`docs/02-SYSTEM-ARCHITECTURE.md`](docs/02-SYSTEM-ARCHITECTURE.md) — backend/frontend/integration architecture.
4. [`docs/03-DATA-MODEL.md`](docs/03-DATA-MODEL.md) — unified data model.
5. [`docs/04-API-CONTRACT.md`](docs/04-API-CONTRACT.md) — REST/SSE contract.
6. [`docs/05-SYNC-ACTIVITY-ENGINE.md`](docs/05-SYNC-ACTIVITY-ENGINE.md) — Activity Engine и sync.
7. [`docs/06-MIGRATION-PLAN.md`](docs/06-MIGRATION-PLAN.md) — перенос legacy PJ-CORE.
8. [`docs/07-SECURITY-TESTING-OPERATIONS.md`](docs/07-SECURITY-TESTING-OPERATIONS.md) — security, QA, operations.
9. [`docs/08-IMPLEMENTATION-ROADMAP.md`](docs/08-IMPLEMENTATION-ROADMAP.md) — roadmap/backlog.
10. [`docs/09-IMPLEMENTATION-HANDOFF.md`](docs/09-IMPLEMENTATION-HANDOFF.md) — точный handoff для coding-агента.

## Принцип v2

`PJ-CORE Wiki = canonical long-term knowledge`

`PJ-CORE Control DB = operational state`

`ActivityEvent = единая лента подтверждённой активности`

`Control Board → Expanded Card → Project Workspace`

## Legacy visual prototype

Текущий prototype можно запустить:

```bash
python3 -m http.server 8080
```

и открыть `http://localhost:8080`.

Он сохраняется как visual/reference prototype до достижения parity новым v2 frontend.

## Adaptive tiers

- 0–3 дня — Focus;
- 4–14 — Active;
- 15–30 — Cooling;
- 31–90 — Dormant;
- >90 — Archive-by-activity.

Activity tier не является lifecycle status проекта.
