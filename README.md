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
![image](https://user-images.githubusercontent.com/128277005/234743589-efa4d0e4-2081-46b1-bab2-c802e3a214ab.png)


Perseguir (perseguir): esse, como o modo de dispersão, é diferente para todos os fantasmas. Em geral, cada fantasma tem uma maneira de rastrear o Pacman. A mais simples delas é ter apenas a posição do Pacman como meta. 

Assustado (aleatório): Quando Pacman come um Power Pellet (círculo branco grande), os fantasmas ficam vulneráveis e o Pacman é capaz de comê-los. Durante este modo, os fantasmas se movem pelo labirinto aleatoriamente e mais devagar. 

Morte (spawn): Este é o modo em que os fantasmas ficam depois que Pacman os come. Nesse modo, o objetivo deles é chegar ao local de desova, para que possam reaparecer (vemos apenas seus olhinhos voltando). Eles também se movem muito mais rápido neste modo. Eles permanecem neste modo até chegarem ao local de desova.


Classe ModoPrincipal:
Podemos pensar no modo de espalhamento e de perseguição como modos principais e todos os outros como modos de interrupção, pois na verdade durante todo o jogo esses modos ficarão alternando segundo o tempo que definirmos. Ao longo do jogo, todos os fantasmas devem ser sincronizados com o espalhamento e a perseguição ao mesmo tempo. Portanto, deve haver algum objeto que alterna continuamente entre esses modos, independentemente do que os fantasmas estão fazendo. Os fantasmas podem entrar individualmente em um dos modos de interrupção, mas uma vez terminados, eles podem descobrir facilmente se devem estar em espalhamento ou perseguição perguntando ao objeto do modo principal.

Classe ModeController:
Essa classe foi criada para controlar os modos e para que possamos sempre saber em qual modo o fantasma deve estar. Aqui será setado as mudanças para os modos aleatório e spawn que poderão ocorrer dependendo dos eventos do jogo.

# pacman.py
Aqui nós criaremos a classe pacman, ela terá a classe andarilhos como classe pai e herdará da mesma várias propriedades.

![image](https://user-images.githubusercontent.com/128277005/234743725-ca4d947f-c099-4ee8-ab8c-d6a68e131c4a.png)

Método de atualização, (atualiza()):
Aqui nós checamos constantemente se alguma tecla válida de direção está sendo pressionada pelo jogador, e depois usamos essa direção para mover o PacMan.

Método de capturar direção (getChaveValida()):
Aqui quando nós detectamos que uma tecla de direção válida foi acionada nós retornamos sua direção correspondente, se nenhuma tecla é acionada pelo operador o retorno será simplesmente PARADO, para que não haja nenhuma mudança de direção.
![image](https://user-images.githubusercontent.com/128277005/234743832-c961de73-2101-409e-86b8-c390f74c8e49.png)

# fruta.py
Classe Fruta:
Quando criamos um objeto de fruta, apenas colocamos esse objeto de fruta entre dois nós. Apesar de não andar, ela herdará a classe andarilhos por conveniência. Aqui faremos a fruta ser criada e ter uma duração de 5 segundos o método de atualização acompanhará esse tempo.




