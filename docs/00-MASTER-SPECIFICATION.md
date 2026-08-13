# PJ-CORE Control Dashboard v2 — Master Specification

Статус: Approved for implementation
Дата: 2026-08-13
Продукт: PJ-CORE Control Dashboard
Репозиторий: `pj-c0m/pj-core-control`

## 1. Назначение

PJ-CORE Control Dashboard — единый операционный интерфейс экосистемы PJ-COM. Он объединяет новый визуальный PJ-CORE Control и функциональность legacy PJ-CORE Dashboard в один продукт.

Продукт должен отвечать на три вопроса:

1. Что сейчас происходит во всех проектах?
2. Что требует внимания Founder?
3. Что можно сделать с конкретным проектом прямо сейчас?

Control не является заменой PJ-CORE Wiki. Wiki остаётся канонической долговременной базой знаний, а Control хранит и отображает оперативное состояние, активность, входящие события и управляющие действия.

## 2. Продуктовые принципы

- Один продукт вместо двух параллельных Dashboard.
- Карточка проекта — основной UI-компонент.
- Главное представление — живая адаптивная мозаика проектов.
- Размер карточки означает свежесть активности, а не ценность проекта.
- Любая значимая активность должна отражаться в Control автоматически.
- Переходы между обзором, expanded card и workspace должны быть бесшовными.
- Founder должен иметь возможность управлять проектом без ухода в стороннюю админку.
- Информация должна быть плотной, но не визуально перегруженной.
- Премиальный визуальный язык важен наравне с функциональностью.
- Все интеграции работают через единый backend/API, а не напрямую с UI-файлами.

## 3. Источники данных

### 3.1 PJ-CORE Wiki

Источник долговременных подтверждённых знаний:
- описание проекта;
- цель;
- архитектура;
- maturity level;
- integration level;
- developer/owner;
- roadmap;
- документация;
- решения;
- ссылки на канонические артефакты.

### 3.2 PJ-CORE Control DB

Источник оперативного состояния:
- focus;
- priority;
- pinned;
- current work;
- next action;
- blocker;
- progress;
- ideas;
- inbox;
- UI state;
- project tools;
- agent bindings;
- activity events;
- notifications;
- sync state.

### 3.3 GitHub

Источник инженерной активности:
- commits;
- pull requests;
- issues;
- releases;
- documentation changes;
- CI/deploy events, если они доступны.

### 3.4 OpenClaw / Jessica / другие агенты

Источник агентной активности:
- начало и завершение работы;
- изменение статуса;
- обнаруженный блокер;
- запрос решения Founder;
- созданный артефакт;
- изменение next action;
- обновление документации.

### 3.5 Telegram bot

Канал быстрого ввода:
- идеи;
- inbox;
- в перспективе быстрые команды проекта.

## 4. Режимы интерфейса

### Level 1 — Control Board

Главный экран с адаптивной сеткой всех проектов.

Отвечает на вопрос: «Что происходит в системе?»

### Level 2 — Expanded Card

Карточка разворачивается внутри текущей сетки и показывает расширенный контекст без перехода на другую страницу.

Отвечает на вопрос: «Что сейчас происходит в этом проекте?»

### Level 3 — Project Workspace

Полноценное рабочее пространство проекта.

Отвечает на вопрос: «Покажи всё и дай управлять проектом».

## 5. Обязательный функционал

### Global

- поиск;
- command palette;
- фильтрация;
- fullscreen mode;
- operational counters;
- Founder Inbox;
- notifications;
- system status;
- глобальные инструменты;
- ручное обновление/синхронизация;
- realtime/polling обновления без полной перезагрузки страницы.

### Project

- просмотр и редактирование имени, статуса, priority;
- focus;
- pinned;
- stage goal;
- current work;
- next action;
- blocker;
- developer/owner;
- MVP progress;
- PROD progress;
- ML/IL/lifecycle state;
- project root/repository/wiki URLs;
- project tools;
- agent bindings;
- Telegram targets;
- ideas;
- notes;
- activity timeline;
- project resources;
- sync status;
- quick actions.

### Ideas

Сохраняется legacy-модель состояний:
- `new`;
- `seen`;
- `done`;
- `rejected`.

Непросмотренные идеи показываются на карточке счётчиком и сигналом.

### Founder Inbox

Поддерживает:
- входящие заметки;
- идеи без проекта;
- вопросы;
- решения, требующие Founder;
- привязку к проекту;
- преобразование в idea/note/task/decision;
- dismiss;
- history.

### Agents

Для каждого проекта:
- список агентов;
- роль;
- enabled/disabled;
- developer/lead marker;
- последняя активность;
- текущая работа;
- быстрые действия;
- переход к связанным системам.

## 6. Адаптивные tiers карточек

- Focus: до 3 суток подтверждённой активности или pinned/focus.
- Active: 4–14 суток.
- Cooling: 15–30 суток.
- Dormant: 31–90 суток.
- Archive-by-activity: более 90 суток.

Это не lifecycle status. Проект не архивируется автоматически.

### Activity policy

- `adaptive` — размер зависит от активности;
- `persistent` — не уменьшается автоматически;
- `manual` — размер/режим задаётся вручную.

## 7. Сигналы карточки

Карточка должна уметь показывать компактные indicators:
- количество новых идей;
- blockers;
- developer/active agent;
- GitHub freshness;
- Wiki sync state;
- production health;
- unresolved Founder decision;
- unread activity.

## 8. Premium UX requirement

Интерфейс не должен выглядеть как стандартная административная панель.

Обязательные свойства:
- тёмная graphite/obsidian визуальная система;
- restrained color palette;
- premium typography;
- glass/elevation эффекты без чрезмерного blur;
- ambient glow только как сигнал активности;
- shared-element transitions;
- мягкая перестройка grid;
- motion с физически правдоподобным easing;
- отсутствие дешёвых neon/RGB эффектов;
- responsive desktop/tablet/mobile layout;
- reduced-motion mode.

## 9. Definition of Done продукта

Версия считается готовой к замене legacy Dashboard, когда:

1. Все существующие проекты мигрированы без потери данных.
2. Ideas и их состояния полностью перенесены.
3. Global Inbox перенесён.
4. Telegram intake работает через новый API.
5. Project tools и global tools доступны.
6. Agent bindings доступны.
7. Focus/priority/status/progress управляются из нового UI.
8. Новый Control не зависит от `projects.json` как от primary storage.
9. Activity engine реально управляет tier карточек.
10. Wiki/GitHub sync состояние отображается.
11. Expanded card и Project Workspace работают.
12. Desktop и mobile UX проходят acceptance tests.
13. Legacy PJ-CORE переводится в read-only/archive после контрольной сверки.

## 10. Документы реализации

- `01-UX-UI-SPECIFICATION.md`
- `02-SYSTEM-ARCHITECTURE.md`
- `03-DATA-MODEL.md`
- `04-API-CONTRACT.md`
- `05-SYNC-ACTIVITY-ENGINE.md`
- `06-MIGRATION-PLAN.md`
- `07-SECURITY-TESTING-OPERATIONS.md`
- `08-IMPLEMENTATION-ROADMAP.md`
