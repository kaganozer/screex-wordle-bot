from PIL import Image, ImageDraw, ImageFont

colors = {"g": "#22ba4a", "y": "#d1b536", "b": "#2c2c2e", "d": "#161617"}


def keyboard_image(letters: list[dict]):
    PADDING = 20
    WIDTH = 60
    HEIGHT = 60

    length = len(letters[0].keys())
    IMAGE_WIDTH = length * (WIDTH + PADDING) + PADDING
    IMAGE_HEIGHT = 3 * (HEIGHT + PADDING) + PADDING

    image = Image.new("RGBA", (IMAGE_WIDTH, IMAGE_HEIGHT))
    draw = ImageDraw.Draw(image)

    for i, row in enumerate(letters):
        for j, letter in enumerate(row.keys()):
            TOP_LEFT_X = j * (WIDTH + PADDING) + PADDING
            TOP_LEFT_Y = i * (HEIGHT + PADDING) + PADDING
            BOTTOM_RIGHT_X = (j + 1) * (WIDTH + PADDING)
            BOTTOM_RIGHT_Y = (i + 1) * (WIDTH + PADDING)

            if i:
                TOP_LEFT_X += (WIDTH + PADDING) * (2 * i - 1) / 2
                BOTTOM_RIGHT_X += (WIDTH + PADDING) * (2 * i - 1) / 2
            
            color = row[letter]
            
            draw.rounded_rectangle(
                (TOP_LEFT_X, TOP_LEFT_Y, BOTTOM_RIGHT_X, BOTTOM_RIGHT_Y),
                fill=colors[color],
                radius=PADDING / 2,
            )

            letter_uppercase = "İ" if letter == "i" else letter.upper()

            TEXT_X = (TOP_LEFT_X + BOTTOM_RIGHT_X) / 2
            TEXT_Y = (TOP_LEFT_Y + BOTTOM_RIGHT_Y) / 2
            font = ImageFont.truetype("fonts/OpenSans-Bold.ttf", 30, encoding="utf-8")
            draw.text((TEXT_X, TEXT_Y), letter_uppercase, "white", font, "mm")

    return image
