from PIL import Image, ImageDraw, ImageFont


def create_photo(msg, id):
    img = Image.open('handlers/flashcards/base.jpg')
    idraw = ImageDraw.Draw(img)

    width, height = img.size

    fontsize = 1

    font = ImageFont.truetype("arial.ttf", size=fontsize)

    while font.getsize(msg)[0] < 0.6 * img.size[0]:
        fontsize += 1
        font = ImageFont.truetype("arial.ttf", size=fontsize)
    if fontsize > 200:
        fontsize = 200
    font = ImageFont.truetype("arial.ttf", size=fontsize)
    w, h = font.getsize(msg)

    idraw.text((width / 2, (height - 10) / 2), msg, font=font, fill='black', anchor="mm")

    img.save(f'handlers/flashcards/{id}:front.png')
