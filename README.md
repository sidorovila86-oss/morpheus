# MORPHEUS AT THE DESK

Браузерная игра: ты режиссёр сна. Выбираешь, кто из посетителей попадёт в сон клиента, и этим лепишь его психику.

## Запуск

```
powershell -ExecutionPolicy Bypass -File serve.ps1 -Port 8768
```

Потом открыть http://localhost:8768/morpheus/proto/

## Сборка для itch.io

```
python morpheus/build_itch.py
```

Создаёт `morpheus/dist/` и `morpheus/morpheus-itch.zip` (в git не хранятся).

## Где что

- `morpheus/proto/` — сама игра (`index.html`, `lang.js`, `week.js`, `album.js`, `music.js`, `menu.js`, шрифты, музыка).
- `morpheus/art/` — генераторы пиксель-арта и готовые спрайты (`art/px/out/`).
- `morpheus/DESIGN.md`, `SCRIPT.md`, `UI_UX.md`, `ASSETS.md` — дизайн, сценарий, интерфейс, ассеты.
- `morpheus/localization.csv` — тексты на разных языках.
- `morpheus/mockup/` — ранние макеты.
