# PJ-CORE Control Dashboard v2 — Implementation Roadmap

Статус: Approved for implementation
Дата: 2026-08-13

## 1. Стратегия разработки

Разработка идёт вертикальными срезами. Каждая фаза должна оставлять работающий продукт, а не набор несвязанных слоёв.

Главная последовательность:
1. фундамент и schema;
2. API + migration;
3. premium Control Board;
4. expanded card/workspace;
5. activity/sync;
6. inbox/bot/agents;
7. hardening/cutover.

## 2. Phase 0 — Repository restructuring

Цель: превратить текущий single-page prototype в maintainable application.

Задачи:
- создать `backend/`, `frontend/`, `docs/`;
- сохранить текущий `index.html` как visual reference до parity;
- выбрать frontend implementation baseline;
- перенести design tokens;
- подготовить Docker Compose;
- CI lint/test/build;
- env example без secrets;
- architecture boundaries.

Acceptance:
- frontend/backend запускаются локально одной командой/compose;
- existing prototype не потерян;
- build reproducible.

## 3. Phase 1 — Unified backend & data model

Задачи:
- FastAPI skeleton;
- DB/session/config;
- SQLAlchemy models;
- Alembic initial schema;
- Project service;
- Idea service;
- Inbox service;
- Tools/Agents compatibility;
- ActivityEvent model;
- SyncState model;
- API errors/auth foundation.

Tests:
- unit core domain;
- migration creation;
- API smoke.

Acceptance:
- projects CRUD/API;
- ideas state machine;
- inbox basic flow;
- activity events persist.

## 4. Phase 2 — Legacy migration tool

Задачи:
- legacy DB reader;
- dry-run mapping;
- project matching;
- migrate notes/ideas/inbox/tools/agents/telegram;
- preserve deliverables/artifacts;
- reconcile Control JSON;
- reports/counts;
- idempotency;
- backup/rollback docs.

Acceptance:
- dry-run produces complete report;
- repeated import has no duplicates;
- test copy legacy data reconciles.

## 5. Phase 3 — Premium Control Board

Задачи:
- global shell;
- operational strip;
- search;
- filters;
- adaptive grid;
- compact/normal/focus cards;
- signal strip;
- card sorting;
- premium design tokens;
- typography;
- background;
- hover/microinteraction;
- responsive desktop/tablet/mobile;
- reduced-motion.

Acceptance:
- board works from API, not JSON;
- 30+ projects visually manageable;
- all activity tiers render correctly;
- visual QA approved.

## 6. Phase 4 — Expanded Card & Workspace

Задачи:
- shared-element card expansion;
- Overview;
- Activity;
- Ideas;
- Tasks;
- Agents;
- Resources;
- inline edit patterns;
- project deep-link;
- browser back/forward state;
- mobile workspace.

Acceptance:
- expand does not lose grid context;
- core legacy project management available in new UI;
- ideas fully manageable;
- workspace direct URL works.

## 7. Phase 5 — Activity Engine + live updates

Задачи:
- ingestion endpoint;
- normalizer/dedupe;
- project resolver;
- tier recompute;
- SSE stream;
- live counters;
- timeline filters;
- unread activity;
- notification generation.

Acceptance:
- incoming event appears without reload;
- confirmed event changes last activity/tier;
- duplicates ignored;
- reconnect safe.

## 8. Phase 6 — Wiki/GitHub sync

Задачи:
- Wiki adapter;
- GitHub adapter;
- field ownership config;
- provenance;
- sync health;
- stale detection;
- conflict UI;
- manual conflict resolution;
- background schedule.

Acceptance:
- Wiki-owned fields refresh safely;
- GitHub activity creates events;
- outage is degraded, not fatal;
- conflicts never silently overwrite.

## 9. Phase 7 — Founder Inbox + Telegram

Задачи:
- Inbox drawer;
- counters;
- convert/attach/resolve flows;
- Telegram bot refactor to API client;
- `/idea`;
- `/inbox`;
- scoped service auth;
- source provenance.

Acceptance:
- Telegram never opens DB directly;
- bot idea immediately appears on project card;
- inbox triage works desktop/mobile.

## 10. Phase 8 — Agents + command palette

Задачи:
- agent cards;
- developer/lead display;
- last activity/current assignment;
- structured agent action request;
- command palette search/actions;
- `Cmd/Ctrl+K`;
- command preview/execute architecture;
- optional natural-language parser behind feature flag.

Acceptance:
- common project operations available from keyboard;
- agent actions audited;
- unsupported transport clearly represented as queued/not-connected, not fake success.

## 11. Phase 9 — System status & operations

Задачи:
- system popover;
- component health;
- backup status;
- sync status;
- observability;
- operational commands;
- restore drill;
- performance tuning.

## 12. Phase 10 — Cutover

Задачи:
- production backup;
- write freeze legacy;
- final migration;
- verification report;
- bot switch;
- proxy switch;
- smoke/E2E;
- monitor;
- legacy read-only;
- archive decision after stable period.

## 13. Work packages / issue groups

### CORE-001..010 Foundation
- repo structure;
- backend bootstrap;
- DB/Alembic;
- config;
- auth;
- error format;
- tests/CI;
- Docker;
- logging;
- health.

### DATA-001..012 Domain & migration
- Project;
- Ideas;
- Inbox;
- Tasks;
- Activity;
- Agents;
- Tools;
- Resources;
- SyncState;
- migration importer;
- JSON reconciliation;
- verification report.

### UI-001..018 Premium UI
- tokens;
- shell;
- operational strip;
- filters;
- card compact;
- card normal;
- card focus;
- signals;
- adaptive grid;
- expand motion;
- overview;
- activity;
- ideas;
- tasks;
- agents;
- resources;
- mobile;
- accessibility/reduced motion.

### ACT-001..008 Activity
- ingest;
- resolve;
- normalize;
- dedupe;
- tier algorithm;
- SSE;
- timeline;
- notifications.

### SYNC-001..009 Integrations
- adapter interface;
- Wiki;
- GitHub;
- field ownership;
- provenance;
- conflict detection;
- resolution;
- scheduler;
- degraded behavior.

### BOT-001..004 Telegram
- API client;
- idea;
- inbox;
- auth/error behavior.

### OPS-001..008 Hardening
- security;
- backup;
- restore;
- visual regression;
- E2E;
- performance;
- release checklist;
- cutover/rollback.

## 14. MVP cutover scope

Обязательно до замены legacy:
- Projects;
- status/focus/priority/current/next/progress;
- Ideas;
- Inbox;
- Tools;
- Agents visibility/basic management;
- Telegram intake;
- premium adaptive board;
- expanded/workspace;
- activity events;
- Wiki/GitHub sync health;
- migration verification;
- backup/rollback.

Можно после cutover:
- natural-language command parsing;
- graph/entity animated background;
- advanced agent execution;
- rich deliverables UI;
- multi-user RBAC beyond baseline;
- advanced analytics.

## 15. Quality bar

Нельзя закрывать UI phase только потому, что функционально кнопки работают. Для этого проекта visual/motion quality является acceptance criterion.

Каждый крупный UI milestone проходит:
- desktop screenshot review;
- mobile screenshot review;
- motion review;
- accessibility check;
- real-data density check.
