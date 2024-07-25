import re

# Функция для замены нежелательных выражений на '...'
def clean_message(message):
    # Список выражений, которые нужно игнорировать
    ignore_patterns = [
        r'\bммм\.?\b', r'\bмм\.?\b', r'\bм\.?\b', r'\bммм\.+\b',
        r'\bммм+', r'\bааа\.?\b', r'\bох\.?\b', r'\bох!?\b',
        r'\bхмм\b', r'\bааа+', r'\bааа\.+\b'
    ]
    # Объединение паттернов в одно регулярное выражение
    combined_pattern = '|'.join(ignore_patterns)
    # Замена всех соответствий паттернам на '...'
    cleaned_message = re.sub(combined_pattern, '...', message, flags=re.IGNORECASE)
    return cleaned_message

# Пример списка сообщений
messages = [
    "ммм. Привет!",
    "Как дела? ааА!",
    "ммм... Думаю, что...",
    "ох! Это невероятно.",
    "ммм, не знаю.",
    "ааааа... Что дальше?"
]

# Очистка каждого сообщения в списке
cleaned_messages = [clean_message(message) for message in messages]

# Вывод очищенных сообщений
# for original, cleaned in zip(messages, cleaned_messages):
#     print(f"Оригинал: {original}")
#     print(f"Очищено: {cleaned}")
#     print()

print(cleaned_messages)