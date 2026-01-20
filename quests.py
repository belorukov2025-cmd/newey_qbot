# quests.py - список всех квестов (можно редактировать как угодно)

SOLO_QUESTS = {
    "day_1_quest_1": "Sit for 20 min on a bench by the fountain in Bryant Park, breathe deeply, no gadgets 🌳🪑",
    "day_1_quest_2": "Walk slowly for 15 min along High Line, observe the city and people 🚶‍♂️🌉",
    
    "day_2_quest_1": "Find a quiet spot near Bethesda Fountain, sit 25 min listening to water 💧",
    "day_2_quest_2": "Stroll through The Ramble, enjoy the forest sounds for 20 min 🌲",
    
    # ... и так далее до day_30 (я сократил, полный список ниже)
    
    # Пример для последнего дня
    "day_30_quest_1": "Sit at Battery Park with view of Statue of Liberty, reflect for 20 min 🗽",
    "day_30_quest_2": "Final walk along High Line end, say goodbye to the city for 25 min 🌅"
}

GROUP_QUESTS = {
    "day_1": "Light yoga on the grass (20–30 min stretching, breathing, poses as you like) 🧘‍♂️",
    "day_2": "Slow mindful walk together (20–30 min, no rush, just enjoy the path) 🚶‍♂️",
    "day_3": "Picnic on the lawn (bring snacks, chat, relax) 🍎",
    "day_4": "Ferry ride (if near, enjoy the water view, 20–30 min) 🚤",
    "day_5": "Visit street performance / concert / art (listen/watch together) 🎶",
    "day_6": "Mini concert — sing favorite songs together without music 🎤",
    "day_7": "Story circle — share short stories on theme of the day 📖",
    "day_8": "Secret Santa — bring small gift (<$10), give to random person 🎁",
    # ... и так далее до day_30
    "day_30": "Final gratitude circle — share one thing you're thankful for today ❤️"
}

# Полный список групповых квестов (30 штук, чередование 8 типов)
GROUP_QUEST_TYPES = [
    "Light yoga on the grass (20–30 min stretching, breathing, poses as you like) 🧘‍♂️",  # 1
    "Slow mindful walk together (20–30 min, no rush, just enjoy the path) 🚶‍♂️",      # 2
    "Picnic on the lawn (bring snacks, chat, relax) 🍎",                             # 3
    "Ferry ride (if near, enjoy the water view, 20–30 min) 🚤",                      # 4
    "Visit street performance / concert / art (listen/watch together) 🎶",           # 5
    "Mini concert — sing favorite songs together without music 🎤",                  # 6
    "Story circle — share short stories on theme of the day 📖",                     # 7
    "Secret Santa — bring small gift (<$10), give to random person 🎁",              # 8
]

# Генерируем 30 групповых квестов с чередованием типов
GROUP_QUESTS = {}
for day in range(1, 31):
    type_index = (day - 1) % len(GROUP_QUEST_TYPES)  # чередование 1–8
    GROUP_QUESTS[f"day_{day}"] = GROUP_QUEST_TYPES[type_index]

# Для соло — пока оставил шаблон, ты можешь расширить до 60
SOLO_QUESTS = {}
for day in range(1, 31):
    SOLO_QUESTS[f"day_{day}_quest_1"] = f"Sit quietly for 20 min in a peaceful spot 🌳🪑 (day {day})"
    SOLO_QUESTS[f"day_{day}_quest_2"] = f"Take a calm walk for 15 min, observe everything around 🚶‍♂️ (day {day})"
