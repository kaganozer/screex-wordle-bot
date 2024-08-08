def check_guess(guess: str, secret: str):
    word_length = len(guess)
    secret_list = list(secret)
    results = list("b" * word_length)

    for index, letter in enumerate(guess):
        if secret_list[index] == letter:
            secret_list[index] = "*"
            results[index] = "g"
    for index, letter in enumerate(guess):
        if results[index] == "g":
            continue
        for j in range(word_length):
            if secret_list[j] == letter:
                secret_list[j] = "*"
                results[index] = "y"
                break

    return results
