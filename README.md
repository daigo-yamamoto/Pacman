# Pacman (Capybaras in CTA)

## What is it?
Capybaras in CTA é uma variação do tradicional, famoso e amado por todos, Pac-Man, feito em python, usando POO e com algumas variações nossas e um toque pessoal com experiências vividas no CTA, H8 e ITA, de modo geral.
Há algumas homenagens a queridos colegas e professores que foram explicados com mais detalhes na apresentação do projeto e que podem servir de easter eggs.
Pac-Man apesar de ser um jogo relativamente antigo, é bastante interessante por conter alguns conceitos diferentes e que podem ser mais explorados, como por exemplo, o uso da inteligência artificial na construção das personalidades de cada fantasma, o comportamento early, mid e late stage de cada fase, previsão de rotas para interceptação, imprevisibilidade e probabilidades.


https://user-images.githubusercontent.com/128277005/234746286-228e1c19-8c14-46a7-ba00-c0d5dda28e02.mp4


## How to play
Baixe os arquivos do jogo e execute o comando “py jogo.py” no terminal. Use as setas do teclado para movimentar a capivara, fuja dos fantasmas, pegue o máximo de pontos que conseguir. Os círculos brancos grandes lhe darão o poder de comer os fantasmas enquanto estes estiverem azul escuro, que é um modo "assustado". Divirta-se!

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

![Untitled (1)](https://user-images.githubusercontent.com/128277005/234743269-6646b1df-ce87-4ff6-8d54-164c6939d7bc.jpg)

# fantasma.py

Classe fantasma:
Aqui nós iremos criar a classe fantasmas que herda a classe andarilhos e tem as característica base de todos os fantasmas, além disso criaremos também uma classe para cada tipo de fantasma que irá herdar as características da classe fantasma principal mas terá características originais específicas acerca de sua movimentação.

Classe Bafão (fantasma):
Essa é a nossa versão personalizada do fantasma vermelho, ele tem a movimentação básica já especificada na classe fantasma, então não precisa de nenhuma especificação nova, apenas herda os movimentos de fantasma (seu espalhamento é para o canto superior esquerdo e sua meta de perseguição é a própria posição do pacman).

Classe Alonso (fantasma):
Essa é a nossa versão personalizada do fantasma rosa, seu comportamento de perseguição descobre onde o pacman está e mira 4 espaços à frente dele. Seu modo de espalhamento visa o canto superior esquerdo.

Classe Rogerio (fantasma):
Essa é a nossa versão do fantasma azul claro, ele já possui uma uma movimentação de perseguição mais complexa que depende da posição do Alonso e do pacman. Seu modo de espalhamento visa o canto inferior direito.

Classe Manga (fantasma):
Essa é a nossa versão do fantasma Laranja, sua perseguição tem um comportamento duplo, se ele está perto do pacman ele age como o Alonso caso o contrário ele irá seguir seu comportamento de espalhamento para o canto inferior esquerdo.

Classe GrupoFantasma:
É melhor lidarmos com os fantasmas como um grupo do que individualmente. Isso fará com que escrevamos menos código. Nela faremos uma lista com todos os fantasmas feitos para lidarmos com eles de maneira mais simples.

# modos.py
Durante o jogo os fantasmas sempre estarão em um dos quatro diferentes modos. A diferença destes modos é basicamente o objetivo dos fantasmas:

Espalhamento (inicio): Este modo diz aos fantasmas para se espalharem para um dos quatro cantos do labirinto. Cada fantasma terá o seu tipo de espalhamento (um dos quatro cantos), todos os fantasmas começam neste modo e após 7 segundos mudam para o modo perseguição, 20 segundos depois eles voltam para esse modo e assim sucessivamente até que ocorra algum evento que faça eles irem para o modo assustado ou morte.

Perseguir (perseguir): esse, como o modo de dispersão, é diferente para todos os fantasmas. Em geral, cada fantasma tem uma maneira de rastrear o Pacman. A mais simples delas é ter apenas a posição do Pacman como meta. 

Assustado (aleatório): Quando Pacman come um Power Pellet (círculo branco grande), os fantasmas ficam vulneráveis e o Pacman é capaz de comê-los. Durante este modo, os fantasmas se movem pelo labirinto aleatoriamente e mais devagar. 

Morte (spawn): Este é o modo em que os fantasmas ficam depois que Pacman os come. Nesse modo, o objetivo deles é chegar ao local de desova, para que possam reaparecer (vemos apenas seus olhinhos voltando). Eles também se movem muito mais rápido neste modo. Eles permanecem neste modo até chegarem ao local de desova.

Classe ModoPrincipal:
Podemos pensar no modo de espalhamento e de perseguição como modos principais e todos os outros como modos de interrupção, pois na verdade durante todo o jogo esses modos ficarão alternando segundo o tempo que definirmos. Ao longo do jogo, todos os fantasmas devem ser sincronizados com o espalhamento e a perseguição ao mesmo tempo. Portanto, deve haver algum objeto que alterna continuamente entre esses modos, independentemente do que os fantasmas estão fazendo. Os fantasmas podem entrar individualmente em um dos modos de interrupção, mas uma vez terminados, eles podem descobrir facilmente se devem estar em espalhamento ou perseguição perguntando ao objeto do modo principal.

Classe ModeController:
Essa classe foi criada para controlar os modos e para que possamos sempre saber em qual modo o fantasma deve estar. Aqui será setado as mudanças para os modos aleatório e spawn que poderão ocorrer dependendo dos eventos do jogo.

# pacman.py
Aqui nós criaremos a classe pacman, ela terá a classe andarilhos como classe pai e herdará da mesma várias propriedades.

Método de atualização, (atualiza()):
Aqui nós checamos constantemente se alguma tecla válida de direção está sendo pressionada pelo jogador, e depois usamos essa direção para mover o PacMan.

Método de capturar direção (getChaveValida()):
Aqui quando nós detectamos que uma tecla de direção válida foi acionada nós retornamos sua direção correspondente, se nenhuma tecla é acionada pelo operador o retorno será simplesmente PARADO, para que não haja nenhuma mudança de direção.

![image](https://user-images.githubusercontent.com/128277005/234743832-c961de73-2101-409e-86b8-c390f74c8e49.png)

# fruta.py
Classe Fruta:
Quando criamos um objeto de fruta, apenas colocamos esse objeto de fruta entre dois nós. Apesar de não andar, ela herdará a classe andarilhos por conveniência. Aqui faremos a fruta ser criada e ter uma duração de 5 segundos o método de atualização acompanhará esse tempo.

# pontos.py

Aqui serão criados os pontos que o pacman irá “comer” durante o jogo:

Classe Pontos:
Essa é a classe dos pontos normais que serão apenas círculos de raio pequeno

Classe PowerPellet:
Essa é classe dos pontos especiais que quando ingeridos pelo pacman lhe darão o poder de comer os fantasmas, eles serão círculos grandes de raio maior.

# pausa.py

Classe Pausa:
Há uma variável pausada que pode ser True ou False. Há também um timer e um pauseTime. Nós os temos porque podemos (e queremos) ter a funcionalidade de pausar apenas por um período de tempo específico. Normalmente, pauseTime será None, o que significa que não há limite de tempo para uma pausa, como quando o jogador pressiona a barra de espaço. 


# sprites.py


Nesse arquivo importaremos as sprites do .png e faremos a interface para atribuí-las a cada classe do jogo necessária.
Esse spritesheet tem os frames de movimento da capivara, dos fantasmas, dos power ups e da criação dos labirintos. O spritesheet foi feito com base no projeto open-source: https://rainloaf.itch.io/capybara-sprite-sheet. 
Segue uma pré-visualização do arquivo png usado “spritesheetfinal.png”:

![image](https://user-images.githubusercontent.com/128277005/234744431-17bb3305-cc66-4029-86aa-a4a2e79a535c.png)

![image](https://user-images.githubusercontent.com/128277005/234744491-271dfdb2-89ff-4357-97a8-c351530d9eab.png)

# jogo.py

Este arquivo é o ponto de entrada para o nosso jogo, ou seja, o arquivo principal que quando rodado iniciará o jogo. Para isso teremos uma main nele, essa main cria uma instância da classe GameController, chama o método começar jogo e faz o loop com o método que atualiza o jogo:

![image](https://user-images.githubusercontent.com/128277005/234744531-612d0a2b-c4aa-450c-a173-421e40e581ac.png)

Classe GameController:

Inicialização:
Primeiro inicializamos o pygame, definimos a tela usando as constantes e chamamos um método que configura a tela de fundo:

![image](https://user-images.githubusercontent.com/128277005/234745367-ddecce10-5e29-40f3-9110-012340b02495.png)

inicializamos o "relógio" do jogo:

![image](https://user-images.githubusercontent.com/128277005/234744636-0a41fb96-3ac8-417b-8bf1-2eca5932ac1f.png)

Método tela de fundo (definePlanoFundo()):
criamos a tela de fundo e colocamos a cor preto nela:

![image](https://user-images.githubusercontent.com/128277005/234744676-cbaf6324-9e28-4239-b02a-62ea6c893ab4.png)

Método começar jogo (iniciaJogo()):
Começamos chamando o método que configura a tela de fundo:

![image](https://user-images.githubusercontent.com/128277005/234744710-6cd30311-2016-48e3-8d77-c1a832a8ed39.png)
Criamos os objetos pacman, pontos e fantasmas:

![image](https://user-images.githubusercontent.com/128277005/234744735-fc9c6f87-8a01-487a-b900-53956369841f.png)

Método atualiza (atualiza()):
Esse método é basicamente o loop do jogo, ele checará os eventos do jogo fará atualizações e desenhará a nova situação. Começamos achando o quanto de tempo passa a cada loop e guardando na variável dt, isso é importante pois cada computador terá uma variável dt diferente dependendo da velocidade com que foi feito o loop na máquina, ter acesso a esse valor é o que nos permitirá equalizar o tempo do jogo para que em qualquer computador a velocidade do jogo seja a mesma quando este estiver rodando:

![image](https://user-images.githubusercontent.com/128277005/234744776-9c07f6f0-4a25-4a39-82c2-6937239507e4.png)



Método desenha (desenha()):
Começamos redesenhando a tela de fundo a fim de apagar todos os desenhos do loop anterior para que a movimentação dos andarilhos (pacman e fantasmas) não gere rastros, posteriormente desenhamos os pontos, as frutas, o pacman e os fantasmas:

![image](https://user-images.githubusercontent.com/128277005/234744838-ba04e46d-3386-4538-b765-8056dc3a9cd8.png)

