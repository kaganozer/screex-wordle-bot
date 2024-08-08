import json
import random

from wordle.functions.check_guess import check_guess


def check_stats_single(guess: str, secret: str):
    word_length = len(secret)
    with open(f"wordle/words/{word_length}_harf.txt", "r", encoding="utf-8") as file:
        words = json.loads(file.read())

    result = check_guess(guess, secret)
    filtered_words = list(
        filter(lambda word: check_guess(guess, word) == result, words)
    )
    return len(filtered_words)


def check_stats(guesses: list[str], secret: str):
    word_length = len(secret)
    with open(f"wordle/words/{word_length}_harf.txt", "r", encoding="utf-8") as file:
        words = json.loads(file.read())

    word_counts = []
    for guess in guesses:
        word_counts.append(len(words))
        result = check_guess(guess, secret)
        words = list(filter(lambda word: check_guess(guess, word) == result, words))
    word_counts.append(len(words))

    return word_counts


def stat_message(initial: int, remaining: int, correct: bool = False):
    reduction_percentage = int(((initial - remaining) / initial) * 10000) / 100
    
    if correct:
        stat_messages = [
            "Senden de bu beklenirdi, süpersin.",
            "Sonunda doğru kelimeyi buldun.",
            "İşte bu be!",
            "Uzun bir yolculuktu ama sonunda değdi.",
            "Yine bekleriz!"
        ]
    elif initial == remaining == 1:
        stat_messages = [
            "1 tane kelime kalmış, onu da bulamamışsın...",
            "Bazen aradığın kelime olmadığını bildiğin halde başka bir kelimeyi denemek istersin. Bekle, kelime mi?",
            "Beceriksizlik mi, büyük bir starteji mi? Hala 1 kelime var.",
            "Peki bu kelimeyi denemiş olman gerçekten işine yaradı mı?",
            "Bu kelimenin doğru olmadığını biliyordun, değil mi?"
        ]
    elif reduction_percentage < 20:
        stat_messages = [
                f"Çok da becerememişsin. Hala {remaining} ihtimal var.",
                f"Yaaani.. Kelime havuzunu sadece %{reduction_percentage} oranında azaltabilmişsin. {remaining} kelime kalmış.",
                f"Bu olmamış. O kadar kelimeden sadece {initial - remaining} tanesini eleyebilmişsin. {remaining} tane kalmış.",
                f"Yine de denemişsin. Önünde hala {remaining} kelime var."
                f"İhtimaller silsilesi. Olsun be. %{reduction_percentage} oranındaki azalma sonucu {remaining} kelime kalmış."
            ]
    elif reduction_percentage < 50:
        stat_messages = [
            f"Çaban takdir edilesi. Olasılıkları %{reduction_percentage} azalttın, geriye {remaining} kaldı.",
            f"Güzel oran hacı. {initial - remaining} kelime elenmiş, {remaining} kalmış.",
            f"Etkilendim hee. Tahminin seçeneklerini {remaining} kelimeye indirmiş.",
            f"Gayet temiz sonuçlar. Başlangıçta {initial}, tahminin sonrası {remaining} kelime.",
            f"Olayı kapmışsın. Kelime havuzunu %{reduction_percentage} azaltarak {remaining} kelime bırakmışsın."
        ]
    else:
        stat_messages = [
            f"Sen var yaa. Seçeneklerin bu tahminle {initial} kelimeden {remaining} kelimeye düşmüş.",
            f"Bu iş bitmiştir. {initial} kelimeden {remaining} kelimeye.",
            f"Şaaahane. {initial} kelimeden {initial - remaining} tanesini elemişsin, {remaining} tane kalmış.",
            f"%{reduction_percentage} nasıl bir oran ya? {remaining} kelime bırakmışsın, yuh.",
            f"İnanılmaz bir tahmin. {initial} kelimeden sadece {remaining} kelime kalmış."
        ]
    
    return random.choice(stat_messages)
