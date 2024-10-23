from PIL import Image, ImageFilter
import pytesseract

img = Image.open('sample2.png')

# blur the image
resized_img = img.filter(ImageFilter.GaussianBlur(radius=2))
resized_img.save('./sample_resized.png')

# sharpen the image
sharpened_img = resized_img.filter(ImageFilter.SHARPEN)
sharpened_img.save('./sample_sharpened.png')

# set page layout detection configuration
custom_config = r'--psm 3'
print(pytesseract.get_languages(config=''))

# apply text extraction on different images
print('---------------------  Original  ---------------------')
result = pytesseract.image_to_string(img, lang='eng', config=custom_config)
print(result)
print(pytesseract.image_to_data(Image.open('sample2.png'), config=custom_config))

print('---------------------  Resized  ---------------------')
print(pytesseract.image_to_string('sample_resized.png', lang='eng'))

print('---------------------  Sharpened  ---------------------')
print(pytesseract.image_to_string('sample_sharpened.png', lang='eng'))

