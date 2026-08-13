# PJ-CORE Control Dashboard v2 — Migration Plan

Статус: Approved for implementation
Дата: 2026-08-13

## 1. Цель

Перенести функциональность и данные legacy `pj-c0m/pj-core` в `pj-c0m/pj-core-control` без потери проектов, ideas, inbox, tools, agents, Telegram targets и operational metadata.

После cutover legacy приложение переводится в read-only/archive, но backup сохраняется.

## 2. Основной принцип

Не делать big-bang rewrite.

Миграция выполняется через совместимую новую backend-модель и проверяемый import pipeline.

## 3. Этап A — Inventory

Перед изменением production:
- определить deployed legacy commit;
- определить deployed Control commit;
- снять schema dump;
- получить row counts по каждой legacy таблице;
- проверить migration history Alembic;
- снять backup DB;
- сохранить `.env` без публикации секретов;
- зафиксировать Telegram bot deployment;
- экспортировать список проектов и ключей.

## 4. Этап B — Backend transplant

В `pj-core-control` переносится/переиспользуется:
- SQLAlchemy patterns;
- Project/ProjectNote/Inbox/Tools/Agents/Telegram domain logic;
- Alembic migration approach;
- validated behavior ideas states;
- relevant tests, если существуют.

Не переносится как целевая архитектура:
- old Jinja UI;
- form/redirect API как основной public interface;
- direct bot→DB writes.

## 5. Этап C — New schema

Создать новую schema с расширенными entities.

Legacy поля не удалять до завершения migration verification. Если семантика поменялась, использовать migration mapping/compatibility fields.

## 6. Этап D — Importer

Создать idempotent command:

```bash
pjcore-control migrate-legacy --source <legacy-db> --dry-run
pjcore-control migrate-legacy --source <legacy-db> --apply
```

Importer должен:
- не хранить secrets в output;
- логировать mapping;
- сохранять original legacy ids в migration metadata;
- не создавать duplicates при повторном запуске;
- выдавать summary counts.

## 7. Data mapping

### Project

Перенести:
- id reference;
- key;
- alias;
- name;
- status;
- stage_goal;
- next_action;
- priority;
- is_focus;
- project_root;
- progress_pct;
- timestamps;
- last_idea_seen_at.

`progress_pct`:
- если новых `mvp_pct/prod_pct` нет, импортировать как compatibility MVP candidate и пометить provenance;
- не выдумывать PROD значение.

### ProjectNote

Перенести полностью.
Idea states сохраняются 1:1.

### InboxItem

Перенести content/state/project/timestamps.

### ProjectTool / GlobalTool

Перенести полностью.

### AgentType / AgentBinding

Перенести полностью, затем enrich новыми role/developer fields только из подтверждённых источников.

### TelegramTarget

Перенести metadata + `token_ref`; реальные token secrets остаются в environment/secret store.

### Deliverables / Artifacts

Legacy содержит эти сущности. Даже если новый UI не показывает их в cutover v1, данные нельзя терять.

Варианты:
- мигрировать в compatibility tables;
- либо сразу включить в Resource/Deliverable domain.

Рекомендуется сохранить entities как first-class data и вывести UI позже.

## 8. New Control JSON reconciliation

Текущий `data/projects.json` содержит дополнительную Control metadata.

Importer должен сопоставлять проекты по порядку:
1. slug/id mapping table;
2. key;
3. exact normalized name;
4. manual mapping.

Из JSON можно импортировать подтверждённые:
- icon;
- summary;
- currentWork;
- nextStep;
- owner;
- pinned;
- mvp;
- prod;
- lastActivity, если provenance подтверждён/помечен как bootstrap.

При конфликте с legacy/wiki значения не перезаписывать молча.

## 9. Dry-run report

Обязательный вывод:
- projects source/target count;
- notes count;
- new/seen/done/rejected ideas counts;
- inbox state counts;
- tools;
- agent bindings;
- Telegram targets;
- deliverables/artifacts;
- unresolved project mappings;
- conflicts;
- rows skipped;
- validation errors.

## 10. Dual verification period

Перед окончательным cutover:
- новый Control работает на копии данных;
- legacy остаётся доступен read-only или временно как контрольный источник;
- сравниваются counts и ключевые user flows;
- Telegram writes направляются только в одну систему, чтобы не получить divergence.

## 11. Cutover

Последовательность:
1. объявить maintenance/write freeze legacy;
2. final backup;
3. final migration/import delta;
4. integrity checks;
5. launch new API/UI/worker/bot;
6. smoke tests;
7. verify all project counts/signals;
8. switch reverse proxy/domain;
9. keep legacy read-only;
10. observe and only then archive runtime.

## 12. Rollback

Rollback должен быть подготовлен до cutover:
- reverse proxy back to legacy;
- preserved legacy DB backup;
- no destructive schema changes to source DB;
- Telegram bot route revert;
- documented last safe commits.

Новый Control DB после rollback не удалять: сохранить для forensic/delta comparison.

## 13. Acceptance checklist

- все projects присутствуют;
- project keys/aliases корректны;
- focus корректен;
- statuses/priority сохранены;
- ideas counts совпадают;
- idea states совпадают;
- inbox counts совпадают;
- tools доступны;
- agents доступны;
- Telegram `/idea` и `/inbox` пишут в новый API;
- нет duplicate rows;
- migration можно повторить на clean target;
- legacy source не изменён importer-ом;
- backup restore проверен.
