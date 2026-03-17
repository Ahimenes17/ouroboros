import random
import json
from datetime import datetime
from typing import Dict, List, Tuple

class FantasyLandscapeGenerator:
    """Генератор фэнтези-ландшафтов для настольных ролевых игр (D&D)"""
    
    def __init__(self, seed=None):
        self.seed = seed or random.randint(1, 1000000)
        random.seed(self.seed)
        
        # === Основные параметры ===
        self.terrain_types = [
            "Горный хребет", "Древний лес", "Болотистые топи", "Пустыня",
            "Степи", "Тундра", "Вулканические земли", "Острова", "Подземелья",
            "Болото", "Лес", "Равнины", "Холмы", "Каньон", "Ледники"
        ]
        
        self.biomes = {
            "Горный хребет": ["Скальные вершины", "Ледники", "Исчезающие тропы", "Пещеры", "Ущелья"],
            "Древний лес": ["Деревья-гиганты", "Заброшенные руины", "Сияющие грибы", "Туманные поляны", "Магические истоки"],
            "Болотистые топи": ["Тростниковые заросли", "Гниющее болото", "Озёра с бугристой водой", "Заброшенные хижины", "Лужи мистической жидкости"],
            "Пустыня": ["Дюны", "Оазисы", "Песчаные бури", "Развалины древних цивилизаций", "Кристаллы энергии"],
            "Степи": ["Бескрайние травы", "Кочевники", "Древние курганы", "Вихри пыли", "Таинные меgaliths"],
            "Тундра": ["Мёрзлая земля", "Снежные равнины", "Ледяные пещеры", "Северные огни", "Следы древних существ"],
            "Вулканические земли": ["Потухшие вулканы", "Лавовые поля", "Геотермальные источники", "Обсидиановые структуры", "Дымящиеся трещины"],
            "Острова": ["Коралловые рифы", "Пиратские гнёзда", "Затопленные руины", "Таинственные пещеры", "Бушевашее море"],
            "Подземелья": ["Каменные туннели", "Глубокие шахты", "Заброшенные города", "Языческие алтари", "Ловушки и секреты"]
        }
        
        self.features = [
            "Древние руины", "Таинственный монолит", "Заброшенная деревня", "Магический источник",
            "Портал в другое измерение", "Кладбище драконов", "Обитель фей", "Логово чудовища",
            "Священное дерево", "Кристаллияния гора", "Лунный камень", "Сердце природы",
            "Забытый алтарь", "Поющий водопад", "Древо судьбы", "Огненная бездна"
        ]
        
        self.weather_patterns = [
            "Постоянный туман", "Вихри магической энергии", "Непрекращающийся дождь",
            "Морозный ветер", "Звучание эха", "Светящиеся частицы", "Временные аномалии",
            "Магическая буря", "Иллюзорные отражения", "Беззвучная тишина"
        ]
        
        self.magic_levels = ["Тихая магия", "Пульсирующая энергия", "Дикая магия", "Запретная мощь"]
        
        self.dangers = [
            "Дикие звери", "Бродящие призраки", "Ожившие статуи", "Големы-стражники",
            "Ядовитые испарения", "Ложные тропы", "Иллюзии", "Проклятые артефакты",
            "Безумные从 (cultists)", "Инопланетные существа", "Ожившие растения", "Временные парадоксы"
        ]
        
        self.npcs = [
            "Отшельник-маг", "Охотник за головами", "Древний дух", "Наследник благородного дома",
            "Безумный алхимик", "Просроченный герой", "Торговец тайнами", "Проклятый принц",
            "Хранитель знаний", "Наемник с прошлым", "Фея-изгнанница", "Голем с душой"
        ]
        
        self.quest_hooks = [
            "Искать потерянный артефакт", "Защитить священное место", "Разрушить древнее проклятие",
            "Найти пропавшего родственника", "Остановить восходящего тирана", "Исследовать внезапное явление",
            "Договориться с враждебными существами", "Очистить территорию от порчи",
            "Найти способ вернуть магию", "Раскрыть заговор", "Спасти плененного духа",
            "Найти дорогу домой"
        ]
    
    def generate_region_name(self) -> str:
        """Генерация имени региона"""
        prefixes = ["Северный", "Южный", "Восточный", "Западный", "Древний", "Забытый", 
                   "Таинственный", "Проклятый", "Священный", "Беспокойный", "Холодный", "Жаркий"]
        suffixes = ["край", "степь", "лес", "хребет", "领主ство", "королевство", "земля", "удел", "район"]
        features = ["Туманов", "Теней", "Снов", "Войны", "Магии", "Драконов", "Богов", "Первых"]
        
        return f"{random.choice(prefixes)} {random.choice(features)} {random.choice(suffixes)}"
    
    def generate_landscape(self) -> Dict:
        """Генерация полного ландшафта"""
        primary_terrain = random.choice(self.terrain_types)
        secondary_terrain = random.choice([t for t in self.terrain_types if t != primary_terrain])
        
        region = {
            "region_name": self.generate_region_name(),
            "primary_terrain": primary_terrain,
            "secondary_terrain": secondary_terrain,
            "biome": random.choice(self.biomes.get(primary_terrain, ["Уникальная местность"])),
            "features": random.sample(self.features, k=random.randint(2, 4)),
            "weather": random.choice(self.weather_patterns),
            "magic_level": random.choice(self.magic_levels),
            "dangers": random.sample(self.dangers, k=random.randint(1, 3)),
            "notable_npcs": random.sample(self.npcs, k=random.randint(1, 2)),
            "quest_hooks": random.sample(self.quest_hooks, k=random.randint(1, 2))
        }
        
        return region
    
    def describe_landscape(self, region: Dict) -> str:
        """Преобразование региона в описательный текст"""
        desc = f"""
🌍 {region['region_name']}

🎯 Основной тип местности: {region['primary_terrain']}
🔄 Второстепенный тип: {region['secondary_terrain']}
🌿 Биом: {region['biome']}

✨ Особенности ландшафта:
"""
        for feat in region['features']:
            desc += f"  • {feat}\n"
        
        desc += f"\n☁️ Погодный паттерн: {region['weather']}"
        desc += f"\n🔮 Уровень магии: {region['magic_level']}"
        
        desc += f"\n\n⚠️ Опасности:\n"
        for danger in region['dangers']:
            desc += f"  • {danger}\n"
        
        desc += f"\n👥 Значимые персонажи:\n"
        for npc in region['notable_npcs']:
            desc += f"  • {npc}\n"
        
        desc += f"\n📜 Сюжетные зацепки:\n"
        for quest in region['quest_hooks']:
            desc += f"  • {quest}\n"
        
        return desc
    
    def generate_map_seed(self) -> Dict:
        """Генерация семени для карты (координаты, размеры)"""
        return {
            "seed": self.seed,
            "grid_size": random.choice([10, 15, 20, 25]),
            "hex_size": random.choice([0.5, 1.0, 1.5, 2.0]),
            "elevation_scale": random.uniform(0.8, 1.5),
            "moisture_scale": random.uniform(0.7, 1.3)
        }

def main():
    """Основная функция для запуска генератора"""
    print("=" * 60)
    print("ФЭНТЕЗИ-ГЕНЕРАТОР ЛАНДШАФТОВ ДЛЯ D&D")
    print("=" * 60)
    
    # Генерация с фиксированным seed для воспроизводимости (можно менять)
    generator = FantasyLandscapeGenerator(seed=random.randint(1, 99999))
    
    # Генерация нескольких вариантов
    for i in range(3):
        print(f"\n{'='*40}")
        print(f"ВАРИАНТ {i+1}")
        print(f"{'='*40}")
        
        landscape = generator.generate_landscape()
        description = generator.describe_landscape(landscape)
        print(description)
        
        map_seed = generator.generate_map_seed()
        print(f"\n🗺️  seed карты: {map_seed}")
    
    print("\n" + "=" * 60)
    print("Готово! Используйте эти описания для своей кампании D&D.")
    print("=" * 60)

if __name__ == "__main__":
    main()
