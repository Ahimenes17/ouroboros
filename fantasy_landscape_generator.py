import random
import json
from datetime import datetime

# === Основные параметры landscapes ===
TERRAIN = [
    "Горный хребет", "Древний лес", "Болотистые топи", "Пустыня",
    "Степи", "Тундра", "Вулканические земли", "Острова", "Подземелья"
]

BIOMES = {
    "Горный хребет": ["Скальные вершины", "Ледники", "Исчезающие тропы", "Пещеры"],
    "Древний лес": ["Деревья-гиганты", "Заброшенные руины", "Сияющие грибы", "Туманные поляны"],
    "Болотистые топи": ["Тростниковые заросли", "Гниющее болото", "Озёра с бугристой водой", "Заброшенные хижины"],
    "Пустыня": ["Дюны", "Оазисы", "Песчаные бури", "Развалины древних цивилизаций"]
}

FEATURES = [
    "Древние руины", "Таинственный водопад", "Таинственный алтарь", "Обломка восхода луны",
    "Заброшенная пещера", "Остатки святилища", "Таинственная роща", "Кристалловые спиры", "Магическое зеркало", "Проклятые статуи"
]

LANDMARKS = [
    "Архитектура с тайными стенами", "Болотистая водопад", "Пещерный образ", "Магический круг", "Таинственный лабиринт",
    "Обломки с прорастающей породой", "Навигационный обелиск", "Ворота с медитативным свечением", "Прорастающая порода", "Проклятые кристаллы"
]

DANGERS = [
    "Ядовитые испарения", "Травящие пески", "Магическое поле", "Подменные пещероборы", "Обезвреживающие земли",
    "Лавины", "Чумы", "Воровские порталы", "Проклятые лабиринты", "Навигационные поляны состояния"
]

NPCS = [
    "Одинокий отшельник", "Чужой из Óстрова", "Проклятый голем", "Друид древних земель", "Мёртвый торговец",
    "Обеспокоенный страж", "Беженец по проклятым тропам", "Потерянный воин", "Мутант с душой", "Охотник"
]

QUEST_HOOKS = [
    "Найти запретительный артефакт", "Освободить древнюю статую", "Победить странника от проклятия", "Найти скрытый секрет", "Найти путь к запрещённому городу",
    "Спасти захваченных", "Найти способ вернуть магию", "Встретить запрещённое портало", "Найти предмет для лечения", "Предотвратить древнего бога"
]

WEATHER = [
    "Снежно", "Солнечно", "Туманно", "СерпENTO", "Воздушно", "Метеорологическое",
    "Стояно", "Посадочно", "Морозное", "Облачное"
]

MOODS = [
    "зловещее", "таинственное", "загадочное", "странное", "мерцающее",
    "заброшенное", "странное", "необычное", "тревожное", "опасное"
]

MAP_SYMBOLS = ["🌍", "🗺", "🏙", "🌫", "🌌", "🏖", "🏘", "🕺", "🗺️", "🌊"]



def generate_landscape(seed: int) -> dict:
    """Создать одну конфигурацию ландшафта с одной семейкой описаний."""
    random.seed(seed)
    
    terrain_type = random.choice(TERRAIN)
    biome = random.choice(BIOMES[terrain_type])
    features = random.sample(FEATURES, 2)
    landmark = random.choice(LANDMARKS)
    danger = random.choice(DANGERS)
    npc = random.choice(NPCS)
    quest_hook = random.choice(QUEST_HOOKS)
    weather = random.choice(WEATHER)
    mood = random.choice(MOODS)
    map_symbols = random.sample(MAP_SYMBOLS, 3)
    
    return {
        "seed": seed,
        "terrain_type": terrain_type,
        "biome": biome,
        "features": features,
        "landmark": landmark,
        "danger": danger,
        "npc": npc,
        "quest_hook": quest_hook,
        "weather": weather,
        "mood": mood,
        "map_symbols": map_symbols,
        "visual_symbols": map_symbols
    }

def describe_landscape(landscape: dict) -> str:
    """Сгенерировать текстовое описание ландшафта."""
    desc = f"Семя: {landscape['seed']}\n"
    desc += "="*50 + "\n"
    desc += f"Ландшафт: {landscape['terrain_type']} (семя: {landscape['seed']})\n"
    desc += "="*50 + "\n"
    
    desc += f"Время и погода: {landscape['weather']}, настроение — {landscape['mood']}.\n"
    desc += "Магическая стихия: Элементальное заклинание.\n"
    desc += "Территория богата:\n"
    desc += "  " + "\n  ".join(['• ' + f for f in landscape['features']]) + "\n"
    desc += f"Особенность: {landscape['landmark']}.\n"
    desc += f"Опасность: {landscape['danger']}.\n"
    desc += f"Местный персонаж: {landscape['npc']}.\n"
    desc += f"Сюжетный крючок: {landscape['quest_hook']}.\n"
    desc += f"\nВизуальные ориентиры:\n"
    desc += " ".join(landscape['map_symbols']) + "\n"
    return desc

def draw_ascii_map(landscape):
    map_symbols = landscape['visual_symbols']
    terrain_char = landscape['terrain_type'][0]
    npc_name = landscape['npc'][:8]  # truncate to fit
    
    ascii_map = r"""  ┌──────────────────────────────────────┐
  │         {} {} {}           │
  │                             │
  │        {}{}{} {}{}{} {}{}{}         │
  │       {}{}{}{}{}{}{}{}        │
  │      {}{}{} {}{}{}  {}{}{}        │
  │     Опасная зона              │
  │          {:<8}                │
  │        Достопримечательность     │
  └──────────────────────────────────────┘"""
    return ascii_map.format(
        map_symbols[0], map_symbols[1], map_symbols[2],
        terrain_char*3, terrain_char*3, terrain_char*3,
        terrain_char*3, terrain_char*3, terrain_char*3,
        terrain_char*3, terrain_char*3, terrain_char*3, terrain_char*3,
        terrain_char*3, terrain_char*3, terrain_char*3,
        terrain_char*3, terrain_char*3, terrain_char*3,
        npc_name
    )

def main():
    print("🎲 Генератор фэнтезий-ландайтов для D&D")
    print("="*50)
    
    landscapes = []
    for i in range(3):
        seed = random.randint(1000, 9999)
        landscape = generate_landscape(seed)
        landscapes.append(landscape)
        print(f"\nГенерация #{i+1}")
        print(f"Семя: {seed}")
        print("="*50)
        
        print(describe_landscape(landscape))
        print("="*50)
        print(draw_ascii_map(landscape))
        print("="*50)
    
    print(f"\n📊 Статистика:")
    print(f"• Генерировано ландайтов: {len(landscapes)}")
    print(f"• Семи использовано: {[l['seed'] for l in landscapes]}")
    print(f"• Типы местности: {len(set([l['terrain_type'] for l in landscapes]))}")

if __name__ == "__main__":
    main()