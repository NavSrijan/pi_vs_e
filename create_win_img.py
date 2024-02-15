from PIL import Image, ImageDraw, ImageFont

def write_over_image(text, font_size, image_path):
    image = Image.open(image_path)
    width, height = image.size
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("fonts/anton.ttf", font_size)  

    # Write the title text
    title_text = text
    text_width, text_height = draw.textsize(title_text, font=font)
    text_x = (width - text_width) / 2  # Center the text horizontally
    text_y = height - text_height - 400  # Place the text near the bottom

    draw.text((text_x, text_y), title_text, font=font, fill="red")  

    image.save(image_path)

