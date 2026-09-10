# 📋 Task Manager

Консольный менеджер задач на Python3 с сохранением в SQLite3.

Простой и мощный CLI-инструмент для управления списком задач с поддержкой приоритетов, поиском.

![Python](https://img.shields.io/badge/Python-3.13+-blue?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-blue?logo=sqlite)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Возможности

- 📝 **Добавление задач** с приоритетами (LOW, MEDIUM, HIGH)
- 📊 **Умная сортировка**: невыполненные задачи выше выполненных, высокий приоритет — выше низкого
- 🔍 **Поиск по частичному совпадению**: по ID или названию (без учёта регистра)
- ✅ **Отметка выполнения** задач
- 🗑️ **Удаление задач** с защитой от случайных действий
- 💾 **Персистентное хранение** в SQLite — данные сохраняются между запусками
- 🎨 **Красивый вывод** с цветами и таблицами через Rich
- ⚙️ **Гибкая конфигурация** через переменные окружения (`.env`)
- 🩺 **Команда диагностики** для проверки окружения

## 🛠️ Технологии

| Технология | Назначение |
|:--|:--|
| [Python 3.13+](https://www.python.org/) | Язык программирования |
| [uv](https://docs.astral.sh/uv/) | Управление зависимостями и виртуальным окружением |
| [SQLite3](https://www.sqlite.org/) | Хранение данных |
| [Typer](https://typer.tiangolo.com/) | Создание CLI-приложений |
| [Rich](https://rich.readthedocs.io/) | Красивый вывод в терминале |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | Работа с переменными окружения |

## 📋 Требования

- Python 3.13 и выше
- [uv](ttps://docs.astral.sh/uv/getting-started/installation/) - менеджер пакетов
- SQLite3

## 🚀 Установка

### 1. Клонирование репозитория

```bash
git clone git@github.com:<ваш репозиторий>/task_manager.git
cd task_manager && cp .env.example .env
```

### 2. Синхронизация зависимостей

```bash
uv sync
```

### 3. Проверка окружения

```bash
uv run task-manager doctor
```
