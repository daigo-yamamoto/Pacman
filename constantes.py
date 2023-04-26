# Arquivo com todas as constantes que vamos utilizar

LARGURA_NO = 16
ALTURA_NO = 16
NUM_LINHA = 36
NUM_COLUNA = 28
LARGURA_TELA = NUM_COLUNA*LARGURA_NO
ALTURA_TELA = NUM_LINHA*ALTURA_NO
TAMANHO_TELA = (LARGURA_TELA, ALTURA_TELA)

# Movimentacao
PARADO = 0
CIMA = 1
BAIXO = -1
ESQUERDA = 2
DIREITA = -2

# CORES
PRETO = (0, 0, 0)
AMARELO = (255, 255, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)

# Jogadores
PACMAN = 0
PONTOS = 1
PONTOSPODER = 2
FANTASMA = 3

# Modos do fantasma
SALVAR = 0
PERSEGUIR = 1
FRETE = 2
SPAWN = 3
