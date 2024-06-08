import os
import pygame
import random

# Inicializa o Pygame
pygame.init()
# Define o título da janela do jogo
pygame.display.set_caption('Jogo da cobrinha')
# Define as dimensões da tela do jogo
largura, altura = 1280, 720
# Inicializa o relógio para controlar a taxa de atualização da tela
relogio = pygame.time.Clock()
# Cria a janela do jogo
tela = pygame.display.set_mode((largura, altura))
# Define a fonte para exibir texto na tela
fonte = pygame.font.SysFont("Arial", 25)

# Definição das cores em RGB
preto = (0, 0, 0)
branco = (255, 255, 255)
vermelha = (255, 0, 0)
verde = (0, 255, 0)
laranja = (255, 165, 0)

# Tamanho do quadrado da cobra
tamanho_quadrado = 20
# Velocidade inicial da cobra
velocidade_cobra = 13

# Caminho absoluto para a imagem de fundo
caminho_imagem = r"C:\Users\monta\Desktop\Developer\Programador_Junior_Python\Jogo_cobrinha\green-2696851_1280.jpg"

# Verificar se a imagem existe
if not os.path.exists(caminho_imagem):
    print(f"Erro: A imagem '{caminho_imagem}' não foi encontrada.")
    pygame.quit()
    exit()

# Carregar a imagem de fundo
imagem_fundo = pygame.image.load(caminho_imagem)
imagem_fundo = pygame.transform.scale(imagem_fundo, (largura, altura))

# Função para gerar a posição da comida da cobra
def gerar_comida():
    comida_x = random.randrange(0, largura - tamanho_quadrado) // tamanho_quadrado * tamanho_quadrado
    comida_y = random.randrange(0, altura - tamanho_quadrado) // tamanho_quadrado * tamanho_quadrado
    return comida_x, comida_y

# Função para desenhar a comida na tela
def desenhar_comida(tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, branco, [comida_x, comida_y, tamanho, tamanho])

# Função para desenhar a cobra na tela
def desenhar_cobra(tamanho, pixels, cor):
    for i, pixel in enumerate(pixels):
        # Alterna a cor da cobra entre preto e laranja
        cor_atual = preto if i % 2 == 0 else laranja
        pygame.draw.rect(tela, cor_atual, [pixel[0], pixel[1], tamanho, tamanho])

# Função para desenhar a pontuação na tela
def desenhar_pontuacao(pontuacao):
    texto = fonte.render(f"Pontuação: {pontuacao}", False, vermelha)
    tela.blit(texto, [1, 1])

# Função para selecionar a direção e velocidade da cobra
def selecionar_velocidade(tecla, direcao_atual):
    if tecla == pygame.K_DOWN and direcao_atual != "cima":
        return 0, tamanho_quadrado, "baixo"
    elif tecla == pygame.K_UP and direcao_atual != "baixo":
        return 0, -tamanho_quadrado, "cima"
    elif tecla == pygame.K_RIGHT and direcao_atual != "esquerda":
        return tamanho_quadrado, 0, "direita"
    elif tecla == pygame.K_LEFT and direcao_atual != "direita":
        return -tamanho_quadrado, 0, "esquerda"
    return None

# Função principal que roda o jogo
def rodar_jogo():
    fim_jogo = False
    pausado = False

    # Posição inicial da cobra
    x  = largura // 2
    y =  altura // 2

    velocidade_x = 0
    velocidade_y = 0
    direcao_atual = None

    tamanho_cobra = 1
    pixels = []

    comida_x, comida_y = gerar_comida()

    while not fim_jogo:
        tela.blit(imagem_fundo, (0, 0))

        # Verifica os eventos (como teclas pressionadas ou fechar a janela)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_jogo = True
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    pausado = not pausado
                if not pausado:
                    nova_velocidade = selecionar_velocidade(evento.key, direcao_atual)
                if nova_velocidade:
                    velocidade_x, velocidade_y, direcao_atual = nova_velocidade
        if not pausado:
            
            # Verifica se a cobra bateu nas bordas da tela
            if x < 0 or x >= largura or y < 0 or y >= altura:
                fim_jogo = True

            #Regra de movimentação da cobra, sempre que andar um quadrado ela ira excluir sua ultima posição (rabo)
            pixels.append([x, y])
            if len(pixels) > tamanho_cobra:
                del pixels[0]
            #Regra para se a cobra bater nela mesma encerrar o jogo
            for pixel in pixels[:-1]:
                if pixel == [x, y]:
                    fim_jogo = True


            desenhar_comida(tamanho_quadrado, comida_x, comida_y)

            x += velocidade_x
            y += velocidade_y

            # Desenha a cobra na tela com a cor preta
            desenhar_cobra(tamanho_quadrado, pixels, preto)

            desenhar_pontuacao(tamanho_cobra - 1)

            # Atualiza a tela
            pygame.display.update()
            # Verifica se a cobra comeu a comida
            if x == comida_x and y == comida_y:
                tamanho_cobra += 1
                comida_x, comida_y = gerar_comida()
            # Controla a velocidade da cobra
            relogio.tick(velocidade_cobra)

# Chama a função principal para iniciar o jogo
rodar_jogo()
# Finaliza o Pygame
pygame.quit()