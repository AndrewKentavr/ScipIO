from PIL import Image, ImageDraw, ImageFont


def find_font_size(text, font, image, target_width_ratio):
    tested_font_size = 100
    tested_font = ImageFont.truetype(font, tested_font_size)
    observed_width, observed_height = get_text_size(text, image, tested_font)
    estimated_font_size = tested_font_size / (observed_width / image.width) * target_width_ratio
    return round(estimated_font_size)


def get_text_size(text, image, font):
    im = Image.new('RGB', (image.width, image.height))
    draw = ImageDraw.Draw(im)
    return draw.textsize(text, font)


def create_photo(msg, id):
    width_ratio = 0.5  # Portion of the image the text width should be (between 0 and 1)
    font_family = "arial.ttf"
    text = msg

    image = Image.open('handlers/flashcards/base.jpg')
    width, height = image.size
    editable_image = ImageDraw.Draw(image)
    font_size = find_font_size(text, font_family, image, width_ratio)
    if font_size > 200:
        font_size = 200
    font = ImageFont.truetype(font_family, font_size)

    editable_image.text((width / 2, (height - 20) / 2), text, font=font, fill='black', anchor="mm")

    image.save(f'handlers/flashcards/{id}:front.png')
