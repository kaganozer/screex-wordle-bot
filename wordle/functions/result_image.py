from PIL import Image, ImageDraw, ImageFont

from wordle.functions.check_guess import check_guess

colors = {"g": "#22ba4a", "y": "#d1b536", "b": "#2c2c2e"}


def result_image(guesses: list, secret: str):
    PADDING = 20
    WIDTH = 100
    HEIGHT = 100

    word_length = len(secret)
    IMAGE_WIDTH = word_length * (WIDTH + PADDING) + PADDING
    IMAGE_HEIGHT = 6 * (HEIGHT + PADDING) + PADDING

    image = Image.new("RGBA", (IMAGE_WIDTH, IMAGE_HEIGHT))
    draw = ImageDraw.Draw(image)

    for i, guess in enumerate(guesses):
        results = check_guess(guess, secret)
        for j, result in enumerate(results):
            TOP_LEFT_X = j * (WIDTH + PADDING) + PADDING
            TOP_LEFT_Y = i * (HEIGHT + PADDING) + PADDING
            BOTTOM_RIGHT_X = (j + 1) * (WIDTH + PADDING)
            BOTTOM_RIGHT_Y = (i + 1) * (HEIGHT + PADDING)

            draw.rounded_rectangle(
                (
                    TOP_LEFT_X,
                    TOP_LEFT_Y,
                    BOTTOM_RIGHT_X,
                    BOTTOM_RIGHT_Y
                ),
                fill=colors[result],
                radius=PADDING / 2
            )

            letter = guess[j]
            letter_uppercase = "İ" if letter == "i" else letter.upper()

            TEXT_X = (TOP_LEFT_X + BOTTOM_RIGHT_X) / 2
            TEXT_Y = (TOP_LEFT_Y + BOTTOM_RIGHT_Y) / 2
            font = ImageFont.truetype(
                "fonts/OpenSans-Bold.ttf", 60, encoding="utf-8"
            )
            draw.text((TEXT_X, TEXT_Y), letter_uppercase, "white", font, "mm")

    return image
