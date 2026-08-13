# PJ-CORE Control Dashboard v2 — Implementation Handoff

Статус: Approved implementation brief
Дата: 2026-08-13

## 1. Для кого этот документ

Для Codex, Jessica, Luna, другого coding-агента или разработчика, который начинает/продолжает реализацию `pj-c0m/pj-core-control`.

Перед кодированием необходимо прочитать документы `00`–`08` в этой директории.

## 2. Цель задачи

Собрать новый PJ-CORE Control Dashboard v2 как единый premium command center, заменяющий legacy `pj-c0m/pj-core` и текущий static/JSON prototype `pj-core-control`.

Нельзя строить третий параллельный Dashboard.

## 3. Неподлежащие изменению решения

1. Runtime product — `pj-c0m/pj-core-control`.
2. Legacy `pj-core` — донор backend/data logic и migration source, затем read-only/archive.
3. PJ-CORE Wiki остаётся canonical long-term knowledge base.
4. Control DB хранит operational state.
5. `projects.json` не primary storage.
6. Telegram bot не пишет напрямую в DB после cutover.
7. Главный UI — adaptive premium project grid.
8. Есть три уровня: Control Board → Expanded Card → Project Workspace.
9. ActivityEvent — first-class entity.
10. Sync не является unrestricted bidirectional replication.
11. Premium visual/motion quality является acceptance criterion.
12. Никакие secrets не коммитить и не выводить во frontend.

## 4. Что взять из legacy `pj-core`

Сохранить поведение/данные:
- Project;
- ProjectNote;
- Idea states new/seen/done/rejected;
- InboxItem;
- ProjectTool;
- GlobalTool;
- AgentType;
- AgentBinding;
- TelegramTarget;
- Deliverable/Artifact data;
- focus/status/priority/current-next/progress semantics.

Не переносить как конечный UX:
- старый Jinja dashboard;
- form/redirect UX;
- direct bot DB access.

## 5. Что взять из текущего `pj-core-control`

Сохранить идеи:
- premium dark visual direction;
- adaptive card sizes;
- pinned;
- search/filter/fullscreen;
- MVP/PROD;
- smooth grid;
- responsive behavior;
- Aurora допустима для lock/login;
- background dot/entity field как optional subtle layer.

Не сохранять как архитектурное ограничение:
- single `index.html`;
- JSON-only state;
- client-side pseudo-auth pattern lock как security boundary.

## 6. Порядок начала разработки

Первая рабочая ветка должна сначала сделать Foundation vertical slice:

1. repo structure;
2. FastAPI + DB + migrations;
3. Project + Idea + ActivityEvent;
4. `/api/v1/projects`;
5. новый frontend shell;
6. одна premium project card из API;
7. add idea flow;
8. activity event appears;
9. tests;
10. Docker run.

Не начинать одновременно Wiki/GitHub/Telegram/natural-language commands, пока foundation slice не работает end-to-end.

## 7. Frontend implementation rule

Если используется React/Preact:
- TypeScript strict;
- component boundaries по spec;
- no giant App component;
- server state отдельно от UI state;
- animation library только для оправданных shared transitions;
- design tokens centralized.

Если используется vanilla/HTMX:
- ES modules;
- HTML fragments/components;
- no 20k-line monolith;
- no global mutable state soup;
- motion/state logic modular.

## 8. UI quality gate

Для каждой card state показать реальный screenshot/preview на:
- desktop;
- mobile.

Нельзя считать карточку готовой, если:
- она выглядит как generic admin template;
- используются чрезмерные neon borders;
- контент скачет при обновлении;
- hover/expand вызывают layout jank;
- information density не проверена на реальных PJ-CORE проектах.

## 9. Data safety gate

До любого production migration:
- dry-run;
- source backup;
- counts;
- idea state counts;
- import idempotency;
- rollback.

Не изменять legacy source DB importer-ом.

## 10. Integration truthfulness

Если agent transport/Knowledge Protocol ещё не подключён:
- UI показывает unavailable/queued/not connected;
- не показывать fake success «агенту отправлено», если реального transport нет.

То же для Wiki/GitHub health.

## 11. Definition of first meaningful milestone

Milestone `V2 Foundation Preview` считается готовым, когда:
- приложение разворачивается;
- реальные/fixture projects приходят из DB API;
- adaptive grid работает;
- premium compact/normal/focus card работают;
- project expands;
- идея создаётся и меняет signal counter;
- ActivityEvent создаётся;
- mobile основной board usable;
- unit + basic E2E pass.

## 12. Документирование изменений

При архитектурных изменениях обновлять соответствующий `docs/*.md`.

Новые подтверждённые решения, меняющие каноническую архитектуру/статус PJ-CORE, должны синхронизироваться с `pj-c0m/pj-core-wiki` на русском языке.

Предположения не фиксировать как подтверждённые факты.
