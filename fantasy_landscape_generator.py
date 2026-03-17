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
    "Пустыня": ["Дюны", "Оазисы", "Песчаные бури", "Развалины древних цивилизаций"],
    "Степи": ["Ковыльные поля", "Холмы", "Старинные курганы", "Сухие русла рек"],
    "Тундра": ["Моховые поля", "Каменные валуны", "Полярные сияния", "Замёрзшие озёра"],
    "Вулканические земли": ["Лавовые поля", "Жерла вулканов", "Серные испарения", "Обсидиановые пещеры"],
    "Острова": ["Коралловые рифы", "Пальмовые рощи", "Подводные пещеры", "Сокровищница пиратов"],
    "Подземелья": ["Тёмные коридоры", "Сокровищницы", "Ловушки", "Подземные реки"]
}

FEATURES = [
    "Древние руины", "Таинственный алтарь", "Святилище природы", "Затерянный город",
    "Магический водопад", "Обсерватория звёзд", "Сад забытых богов", "Кристальные пещеры",
    "Портал в иной мир", "Храм забытых предков"
]

DANGERS = [
    "Ядовитые туманы", "Скрытые ямы", "Иллюзорные пути", "Переменные магические поля",
    "Бродячие монстры", "Коварные ловушки", "Ментальные чудовища", "Магические паразиты",
    "Паутина времени", "Проклятые земли"
]

NPCS = [
    "Отшельник-знахарь", "Голем с душой", "Путешествующий торговец", "Дух предка",
    "Хранитель знаний", "Пленный дух", "Пират-призрак", "Мудрый друид",
    "Теневой странник", "Артефактор-кузнец"
]

QUESTS = [
    "Найти потерянный артефакт", "Снять древнее проклятие", "Исследовать загадочные руины",
    "Освободить пленный дух", "Найти путь домой", "Спасти деревню от нападения",
    "Заполучить силу природы", "Открыть скрытый портал", "Раскрыть древнюю тайну", "Уничтожить источник зла"
]

MAGIC = [
    "Природная энергия", "Запретная мощь", "Астральная магия", "Телекинез",
    "Восстановление", "Иллюзия", "Элементальное заклинание", "Проклятие", "Телепортация", "Дикая магия"
]

WEATHER = ["Пасмурно", "Дождливо", "Солнечно", "Туманно", "Штормово", "Снежно", "Ветрено", "Ясно", "Метельно", "Сумрачно"]
MOOD = ["Зловещее", "Загадочное", "Печальное", "Таинственное", "Спокойное", "Опасное", "Вдохновляющее", "Прекрасное", "Угрожающее", "Безмятежное"]

SYMBOLS = {
    "Горный хребет": ["⛰️", "🏔️", "🪨", "🦅"],
    "Древний лес": ["🌲", "🌳", "🍄", "🦌"],
    "Болотистые топи": ["🌿", "🐸", "🐉", "💧"],
    "Пустыня": ["🏜️", "🐫", "☀️", "🦂"],
    "Степи": ["🌾", "🐎", "🏜️", "🌅"],
    "Тундра": ["❄️", "🌨️", "🐻", "🌌"],
    "Вулканические земли": ["🌋", "🔥", "⚡", "🪱"],
    "Острова": ["🏝️", "🌴", "🦜", "🐬"],
    "Подземелья": ["🕳️", "🕷️", "💰", "⛏️"]
}

def generate_landscape(seed=None):
    if seed:
        random.seed(seed)
    else:
        seed = random.randint(1000, 9999)
    
    terrain_type = random.choice(TERRAIN)
    biome_features = random.sample(BIOMES[terrain_type], k=2)
    feature = random.choice(FEATURES)
    danger = random.choice(DANGERS)
    npc = random.choice(NPCS)
    quest_hook = random.choice(QUESTS)
    magic_element = random.choice(MAGIC)
    weather = random.choice(WEATHER)
    mood = random.choice(MOOD)
    symbols = SYMBOLS[terrain_type]
    
    landscape = {
        'id': f"land-{hex(random.randint(0x100000, 0xFFFFFF))[2:]}",
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'seed': seed,
        'terrain_type': terrain_type,
        'biome_features': biome_features,
        'feature': feature,
        'danger': danger,
        'npc': npc,
        'quest_hook': quest_hook,
        'magic_element': magic_element,
        'weather': weather,
        'mood': mood,
        'visual_symbols': symbols
    }
    
    return landscape

def describe_landscape(landscape):
    terrain = landscape['terrain_type']
    features = landscape['biome_features']
    feature = landscape['feature']
    danger = landscape['danger']
    npc = landscape['npc']
    quest = landscape['quest_hook']
    magic = landscape['magic_element']
    weather = landscape['weather']
    mood = landscape['mood']
    symbols = landscape['visual_symbols']
    
    desc = f"{'='*50}\n"
    desc += f"Ландшафт: {terrain} (семя: {landscape['seed']})\n"
    desc += f"{'='*50}\n\n"
    desc += f"Время и погода: {weather}, настроение — {mood.lower()}.\n"
    desc += f"Магическая стихия: {magic}.\n\n"
    desc += f"Территория богата:\n"
    desc += "  " + "\n  ".join(['• ' + f for f in features]) + "\n"
    desc += f"Особенность: {feature}.\n"
    desc += f"Опасность: {danger}.\n"
    desc += f"Местный персонаж: {npc}.\n"
    desc += f"Сюжетный крючок: {quest}.\n"
    desc += f"\nВизуальные ориентиры:\n"
    desc += " ".join(symbols) + "\n"
    return desc

def draw_ascii_map(landscape):
    map_symbols = landscape['visual_symbols']
    terrain_char = landscape['terrain_type'][0]
    npc_name = landscape['npc'][:8]  # truncate to fit
    
    ascii_map = r"""  ┌─────────────────────────────┐
  │         {} {} {}           │
  │                             │
  │        {}{}{} {}{}{} {}{}{}         │
  │       {}{}{}{}{}{}{}{}        │
  │      {}{}{} {}{}{}  {}{}{}        │
  │     Опасная зона              │
  │          {:<8}                │
  │        Достопримечательность     │
  └─────────────────────────────┘""".format(
        map_symbols[0], map_symbols[1], map_symbols[2],
        terrain_char*3, terrain_char*3, terrain_char*3,
        terrain_char*3, terrain_char*3, terrain_char*3,
        terrain_char*3, terrain_char*3, terrain_char*3, terrain_char*3,
        terrain_char*3, terrain_char*3, terrain_char*3,
        terrain_char*3, terrain_char*3, terrain_char*3,
        npc_name
    )
    return ascii_map

def main():
    print("🎲 Генератор фэнтези-ландшафтов для D&D")
    print("="*50)
    
    landscapes = []
    for i in range(3):
        seed = random.randint(1000, 9999)
        landscape = generate_landscape(seed)
        landscapes.append(landscape)
        print(f"\nГенерация #{i+1}")
        print(f"Семя: {seed}")
        print(describe_landscape(landscape))
        print(draw_ascii_map(landscape))
    
    # Сохраняем в JSON
    with open('generated_landscapes.json', 'w', encoding='utf-8') as f:
        json.dump(landscapes, f, ensure_ascii=False, indent=2)
    
    print("\n✅ Готово! Сохранено в generated_landscapes.json")
    print("\nСоветы для Мастера:")
    print("- Используйте 'seed' для воспроизведения одного и того же ландшафта")
    print("- Изменяйте параметры вручную для создания кастомных миров")
    print("- Используйте 'quest_hook' как основу для приключений")

if __name__ == '__main__':
    main()