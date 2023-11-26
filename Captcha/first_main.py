import random
import svgwrite

captcha_text = ""


# Funktion zur Generierung eines zufälligen Zeichens (Buchstabe oder Zahl)
def generate_random_character():
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return random.choice(characters)


# Funktion zur Generierung des Captcha-Texts
def generate_captcha_text(length):
    return "".join(generate_random_character() for _ in range(length))


# Funktion zur Erstellung eines SVG-Captcha-Bilds
def create_captcha_svg(captcha_text):
    dwg = svgwrite.Drawing('captcha.svg', profile='tiny', size=(150, 50))

    for i in range(len(captcha_text)):
        x = i * 25 + 10
        y = 30
        rotation = random.randint(-30, 30)
        char = captcha_text[i]

        # Zeichne das Zeichen mit Rotation
        dwg.add(dwg.text(char, insert=(x, y), fill='red', font_size=20, transform=f"rotate({rotation}, {x}, {y})"))

        # Füge Linienmuster hinzu
        for _ in range(10):
            x1 = random.uniform(x - 5, x + 15)
            y1 = random.uniform(y - 10, y + 10)
            x2 = random.uniform(x - 5, x + 15)
            y2 = random.uniform(y - 10, y + 10)
            dwg.add(dwg.line(start=(x1, y1), end=(x2, y2), stroke=svgwrite.rgb(0, 0, 0, '%')))

        for _ in range(10):
            x1 = random.uniform(x - 5, x + 15)
            y1 = random.uniform(y - 10, y + 10)
            x2 = random.uniform(x - 5, x + 15)
            y2 = random.uniform(y - 15, y + 15)
            dwg.add(dwg.line(start=(x1, y1), end=(x2, y2), stroke=svgwrite.rgb(150, 50, 0, '%')))

        dwg.save()
        print("Captcha wurde in 'captcha.svg' gespeichert.")
