# Pacman (Capybaras in CTA)

## What is it?
Capybaras in CTA é uma variação do tradicional, famoso e amado por todos Pac-Man, feito em python, usando POO e com algumas variações nossas e um toque pessoal com experiências vividas no CTA, H8 e ITA, de modo geral.
Há algumas homenagens á queridos colegas e professores que foram explicados com mais detalhes na apresentação do projeto e que podem servir de easter eggs.
Pac-Man apesar de ser um jogo relativamente antigo, é bastante interessante por conter alguns conceitos diferentes e que podem ser mais explorados, como por exemplo, o uso da inteligência artificial na construção das personalidades de cada fantasma, o comportamento early, mid e late stage de cada fase, previsão de rotas para interceptação, imprevisibilidade e probabilidades.

## How to play
Baixe os arquivos do jogo e dê o comando “py jogo.py” no terminal. Use as setas do teclado para movimentar a capivara, fuja dos fantasmas, pegue o máximo de pontos que conseguir. Os círculos brancos grandes lhe darão o poder de comer os fantasmas enquanto estes estiverem azul escuro, que é um modo "assustado". Divirta-se!

## Overview
Aqui, daremos uma explicada rápida em algumas das implementações para facilitar o entendimento do código.

# constantes.py
Armazenamos qualquer valor que não mude (constantes) em um único arquivo. Assim, se precisarmos alterar manualmente esses valores, não precisamos ficar procurando eles em vários arquivos. As cores foram definidas como tuplas RGB.

# vetor.py
Classe Vetor2:
A classe vetores será o ponto chave para trabalharmos com a posição e movimentação dos objetos do jogo

Inicialização:
As coordenadas x e y são apenas as coordenadas para as quais o vetor aponta, inicializamos o vetor com elas e com o erro que será usado para descartar eventuais diferenças na sexta casa decimal na hora de comparar os vetores.

![image](https://user-images.githubusercontent.com/128277005/234742798-6d213920-9fb0-4e4e-9a97-4fa9ada8469c.png)

Métodos aritméticos:
Esses métodos basicamente irão permitir a adição e subtração de vetores, sua multiplicação e divisão, bem como checar a igualdade entre eles. 
![image](https://user-images.githubusercontent.com/128277005/234742855-8ad2e04e-2506-45c8-a8bc-977a005ce148.png)

Métodos de magnitude:
Aqui nós temos dois métodos, um deles retorna o tamanho real do vetor usando a operação sqrt e outro retorna tal tamanho ao quadrado. É bom ter os dois pois sempre que pudermos evitar a operação raíz durante o jogo é bom evitá-la. Por exemplo, quando queremos apenas comparar o tamanho de dois vetores podemos usar o método que retorna o tamanho ao quadrado, economizando a operação math.sqrt():
![image](https://user-images.githubusercontent.com/128277005/234742897-44c3e828-75b8-46c8-be9a-561c8e040e95.png)

Métodos de cópia:
Os métodos de cópia retornam uma cópia do vetor para que nós tenhamos uma nova instância dele para que mexamos nela sem alterá-lo, fazemos isso de três maneiras diferentes métodos um retorna um vetor, outro uma tupla e outro uma tupla de inteiros:
![image](https://user-images.githubusercontent.com/128277005/234742939-f60a57fd-d749-4cf1-9009-1a8b670e6055.png)

# no.py

Classe No:
Aqui nós criamos os nós que serão a base da movimentação do pacman, basicamente o pacman poderá apenas circular na malha de nós e a partir dos nós faremos o mapa. Na imagem abaixo, os nós são os círculos vermelhos e o pacman o círculo amarelo, o pacman só pode andar entre os caminhos que ligam os nós. 
![image](https://user-images.githubusercontent.com/128277005/234742984-e8e9a3b1-dd26-4649-a38a-a303c90c4b2f.png)


Classe GrupoNo
Com essa classe os mapas serão efetivamente montados a partir do grupo de nós.

# mapa.txt
Possui efetivamente o desenho do mapa a partir dos nós que será usado no jogo.

# andarilhos.py
Classe Andarilho:
Aqui nós fizemos a classe pai de todas as figuras que se movem no jogo, essa classe é importante pois tanto os fantasmas quanto o pacman seguem a mesma dinâmica base de movimento, que é regida pelos nós, então faz sentido separar tal dinâmica numa única classe e depois fazer a classe pacman e fantasmas herdá-la.

