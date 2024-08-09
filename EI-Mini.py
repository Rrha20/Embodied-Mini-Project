import pygame
import random
import sys
from inference_sdk import InferenceHTTPClient
import cv2
import time

# Press run and make sure you have a webcame
# It is a bit slow, I'm sorry!


pygame.init()

width, height = 1000, 700
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Math Game with Emotion Detection')

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

font = pygame.font.Font(None, 50)

CLIENT = InferenceHTTPClient(
    api_url="https://classify.roboflow.com",
    api_key="S36Lao3rIckgSTNdkvhj"
)

cap = cv2.VideoCapture(0)


def new_question(b):
    x = random.randint(1, b)
    y = random.randint(1, b)
    return x, y, x + y

def display_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    window.blit(text_surface, (x, y))

def get_emotion(image):
    result = CLIENT.infer(image, model_id="face-emotion-detection-multi/1")
    if 'predicted_classes' in result and result['predicted_classes']:
        return result['predicted_classes'][0]
    return "No emotion detected"

def game_loop():
    b= 10
    x, y, answer = new_question(b)
    user_input = ''
    feedback = ''
    correct_answers = 0
    emotion = "Loading..."
    show_hint = False
    running = True

    while running:
        success, image = cap.read()
        if success:
            emotion = get_emotion(image)
            if emotion == "happy":
                show_hint = True
            else:
                show_hint = False

        window.fill(white)

        display_text(f'Correct: {correct_answers}', black, 10, 10)

        display_text(f'{x} + {y} = ', black, 50, 100)

        display_text(user_input, black, 200, 100)

        display_text(feedback, green if feedback == 'Correct!' else red, 100, 200)

        display_text(f'Emotion: {emotion}', black, 10, 50)

        if show_hint:
            display_text(f'Hint: The answer is between {answer-2} and {answer+2}', black, 10, 150)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                cap.release()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input.isdigit() and int(user_input) == answer:
                        feedback = 'Correct!'
                        b += 1
                        correct_answers += 1
                    else:
                        feedback = 'Wrong!'

                    pygame.display.update()
                    pygame.time.delay(1000)
                    x, y, answer = new_question(b)
                    user_input = ''
                    feedback = ''
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.unicode.isdigit():
                    user_input += event.unicode

        pygame.display.update()


game_loop()
