import openai
import pyttsx3
import time
import pygame

# Define o tamanho da janela
largura = 800
altura = 600

# Inicializa o Pygame
pygame.init()

# Cria a janela do jogo
janela = pygame.display.set_mode((largura, altura), pygame.RESIZABLE)

# Define o título da janela
pygame.display.set_caption('Meu jogo')

# Define o modelo do OpenAI GPT-3
openai.api_key = "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"
model_engine = "text-davinci-002"

# Define a função que faz a pergunta ao modelo e retorna a resposta
def ask_question(question):
    prompt = (f"Pergunta: {question}\nResposta:")
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    answer = response.choices[0].text.strip()
    return answer

# Define a função que fala a resposta usando o pacote pyttsx3
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Define a cor de fundo da janela
janela.fill((0, 0, 0))

# Exibe a mensagem "Faça uma pergunta:" na janela do jogo
fonte = pygame.font.SysFont("Arial", 20)
mensagem = fonte.render("Faça uma pergunta:", True, (255, 255, 255))
janela.blit(mensagem, (10, 10))

# Define o campo de entrada de texto
fonte = pygame.font.SysFont("Arial", 20)
campo_texto = pygame.Rect(10, 40, largura - 20, 30)
pygame.draw.rect(janela, (255, 255, 255), campo_texto, 2)
pygame.display.update()

pergunta = ''
resposta = ''
enviou_pergunta = False
# Loop principal do jogo
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            # Sai do jogo quando o usuário clica no botão de fechar
            pygame.quit()
            quit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                pergunta = pergunta[:-1]
            elif evento.unicode.isalnum() or evento.unicode.isalpha() or evento.unicode.isdigit() or evento.unicode.isspace():
                pergunta += evento.unicode

            # Renderiza a pergunta na janela
            fonte = pygame.font.SysFont("Arial", 20)
            pergunta_surface = fonte.render("Pergunta: " + pergunta, True, (255, 255, 255))
            janela.blit(pergunta_surface, (10, 40)) # exibe o texto na janela

        # Verifica se o usuário apertou enter
        teclas_pressionadas = pygame.key.get_pressed()
        if teclas_pressionadas[pygame.K_RETURN]:
            # Faz a pergunta ao modelo e fala a resposta
            resposta = ask_question(pergunta)
            speak(resposta)
            pergunta = '' # reseta a pergunta após obter a resposta

    # Define a cor de fundo da janela
    janela.fill((0, 0, 0))
    # Exibe a mensagem "Faça uma pergunta:" na janela do jogo
    fonte = pygame.font.SysFont("Arial", 20)
    mensagem = fonte.render("Faça uma pergunta:", True, (255, 255, 255))
    janela.blit(mensagem, (10, 10))
    # Renderiza a pergunta na janela
    fonte = pygame.font.SysFont("Arial", 20)
    pergunta_surface = fonte.render(" " + pergunta, True, (255, 255, 255))
    janela.blit(pergunta_surface, (10, 40))

    # Renderiza a resposta na janela
    resposta_surface = fonte.render(" " + resposta, True, (255, 255, 255))
    janela.blit(resposta_surface, (10, 70))


    # Espera um pouco antes de continuar
    time.sleep(0.1)

    # Atualiza a janela
    pygame.display.update()