from PIL import Image, ImageDraw, ImageFont


def find_font_size(text, font, image, target_width_ratio):
    tested_font_size = 100
    tested_font = ImageFont.truetype(font, tested_font_size)
    observed_width, observed_height = get_text_size(text, image, tested_font)
    estimated_font_size = tested_font_size / (observed_width / image.width) * target_width_ratio * 1.5
    if estimated_font_size > 35:
        estimated_font_size = 35
    elif estimated_font_size < 18:
        estimated_font_size = 18
    return round(estimated_font_size)


def get_text_size(text, image, font):
    im = Image.new('RGB', (image.width, image.height))
    draw = ImageDraw.Draw(im)
    return draw.textsize(text, font)


def create_photo(msg, id):
    width_ratio = 1.5  # Portion of the image the text width should be (between 0 and 1)
    font_family = "handlers/flashcards/pillow.ttf"
    text = msg

    image = Image.open('handlers/flashcards/base.jpg')
    width, height = image.size
    editable_image = ImageDraw.Draw(image)
    font_size = find_font_size(text, font_family, image, width_ratio)
    # Чтобы текст не был слишком большим или слишком маленьким

    list_line = []
    list_words = text.split()

    font = ImageFont.truetype(font_family, font_size)

    if len(list_words) > 1:

        font = ImageFont.truetype(font_family, font_size)

        if get_text_size(text, image, font)[0] > 300:
            count = ''
            for i in range(len(list_words)):
                if get_text_size(count + list_words[i] + ' ', image, font)[0] <= 300:
                    count += list_words[i] + ' '
                else:
                    list_line.append(count[:-1])
                    count = list_words[i] + ' '
            list_line.append(count[:-1])
        else:
            list_line.append(text)

        if len(list_line) % 2 == 0:
            print(list_line)
            print(get_text_size(text, image, font))
            count = (len(list_line) // 2) * get_text_size(text, image, font)[1]
            for i in range(len(list_line)):
                editable_image.text((width / 2, (height + 30) / 2 - count), list_line[i], font=font, fill='black',
                                    anchor="mm")
                count -= get_text_size(text, image, font)[1]
        else:
            count = (len(list_line) - 1) // 2 * get_text_size(text, image, font)[1] + get_text_size(text, image, font)[
                1] / 2
            for i in range(len(list_line)):
                editable_image.text((width / 2, (height + 30) / 2 - count), list_line[i], font=font, fill='black',
                                    anchor="mm")
                count -= get_text_size(text, image, font)[1]

    else:
        editable_image.text((width / 2, height / 2), text, font=font, fill='black', anchor="mm")

    image.save(f'handlers/flashcards/{id}:front.png')
