# 🚤 Система управления лодкой

Проект представляет собой систему управления лодкой с различными типами двигателей и веслами.

## 📁 Структура проекта

```
boat_project/
├── core/                    # Основные компоненты
│   ├── boat.py             # Класс лодки
│   ├── oar.py              # Класс весла
│   └── propulsion_system.py # Система движения
├── interfaces/             # Интерфейсы
│   └── interfaces.py       # Базовые интерфейсы
├── utils/                  # Утилиты
│   ├── metrics.py          # Метрики
│   └── logging_config.py   # Конфигурация логирования
├── config/                 # Конфигурация
│   ├── requirements.txt    # Зависимости
│   └── pyproject.toml      # Настройки проекта
├── tests/                  # Тесты
│   ├── test_boat.py
│   ├── test_oar.py
│   └── test_propulsion_system.py
├── setup.py                # Установка проекта
└── README.md               # Документация
```

## 🛠️ Установка

1. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # для Linux/Mac
   venv\Scripts\activate     # для Windows
   ```

2. Установите зависимости:
   ```bash
   pip install -r config/requirements.txt
   ```

3. Установите проект в режиме разработки:
   ```bash
   pip install -e .
   ```

## 🧪 Тестирование

Запуск тестов:
```bash
pytest
```

Проверка качества кода:
```bash
python scripts/check_code_quality.py
```

## 💻 Использование

```python
from core.boat import Boat
from core.oar import Oar
from core.propulsion_system import PropulsionSystem, PropulsionType

# Создание компонентов
oars = [Oar(2.5, "wood"), Oar(2.5, "wood")]
propulsion = PropulsionSystem(type_=PropulsionType.MANUAL)

# Создание лодки
boat = Boat(
    name="MyBoat",
    weight=100,
    oars=oars,
    propulsion_system=propulsion
)

# Управление лодкой
boat.move(force=50)  # Начать движение
boat.stop()          # Остановиться

# Получение статуса
status = boat.get_status()
print(status)
```

## ✨ Особенности

- 🚤 Поддержка различных типов двигателей (ручной, механический, электрический)
- 📊 Система метрик для мониторинга производительности
- 📝 Подробное логирование операций
- 🏷️ Полностью типизированный код
- ✅ Обширное покрытие тестами

## 📝 Лицензия

MIT License