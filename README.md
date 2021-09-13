# Nota: 
  O código original entregue durante a cadeira em 2020.3 se encontra no branch Original, o ramo main possui alguma mudanças

# Untitled Wizard Game
  Untitled Wizard Game é um jogo top-down shooter desenvolvido usando Pygame baseado no minigame _Journey of The Prairie King_ de _Stardew Valley_, de onde tiramos grande parte dos sprites além da música de fundo. O jogador controla um mago e deve matar as hordas de zumbis para coletar moedas que servem como pontuação, utilizando os itens que os inimigos dropam para poder se manter vivo o máximo de tempo possivel e coletar a maior quantidade de moedas antes de morrer e passar para a próxima fase. 

  Os itens são:
  - moedas simples (1 ponto)
  - moedas especiais (10 pontos)
  - botas aladas (aumento permanente de velocidade movimento)
  - cristais mágicos (aumento permantente de velocidade de tiro)
  - pergaminho vermelho (aumento temporário de velocidade de tiro)
  - pergaminho roxo (aumento temporário da quantidade de tiros)
  - pergaminho azul (temporariamente paralisa os inimigos)

  O jogador começa cada fase com 3 de vida, perdendo um de vida sempre que colide com um inimigo, as botas e cristais são upgrades permanentes enquanto os pergaminhos são itens consumíveis, podendo ter mais de um ativo ao mesmo tempo, mas apenas guardando um no inventário de cada vez, se você já tem um pergaminho no iventário e coleta um novo pergaminho esse pergaminho sera usado automaticamente.

# Como Baixar e Jogar:
  Para rodar o jogo basta ter python e pygame instalados, baixar o zip ou clonar esse repositório e rodar o arquivo game.py no diretório do arquivo. 
 
  controles: wasd para movimento, botão esquerdo do mouse para atirar, tecla de espaço para ativar o pergaminho atual.

## Divisão de tarefas:
|            Equipe              |          Tarefas           |
| ------------------------------ | -------------------------- |
| **Filipe Gomes** | Jogador, Itens e Projéteis |
| **Humberto Lima Felipe Guimarães** | Inimigos |
| **Rodrigo Moura** | Mapas |
| **Jonathas Vinicius** | UI e HUD |
| **Felipe Guimarães** | Novos Sprites |

## Link para o codigo fonte:
- https://github.com/FilipeGomesMelo/Game_IP

## Organização do código:
  O código é separado em seis módulos, cada um contendo uma ou mais classes responsáveis pelo funcionamento do jogo, o módulo _game_ é o componente principal liga todos os outros:
## **Game.py**:
> game.py é a espinha dorsal do nosso jogo, é ela que coordena tudo e todas as interações entre as muitas partes desse jogo. Game.py importa todas as outras classes com exceção de projectile.py, além de importar random e datetime.
>  
>	Fora fazer o setup inicial (inicializar pygame, pygame.mixer, inicializar o display, carregar as imagens sons e música, criar o jogador e o mapa, a lista que vai conter todos os inimigos, o dicionário que vai conter os itens coletados na fase atual, entre outras coisas), game.py tem as funções texto, que desenha uma mensagem de texto na tela. A função recebe uma string, uma cor, a posição x e y do texto e o tamanho, a função draw_all que recebe o game_state (‘play’ se o jogo está sendo jogado e ‘start’ quando está esperando o jogador apertar espaço para começar uma nova fase), draw_all chama todas as funções para desenhar o mapa, os inimigos, o jogador (que também desenha as balas) e o HUD. Por último, temos o main, que é onde tudo acontece. Ela possui um loop infinito responsável por rodar o jogo. Criar  novos objetos, atualizar e desenhar todos objetos existentes, destruir objetos que não deveriam mais existir, checar dano e colisão, coletar os itens, entre muitas outras coisas são feitas no main.
>	
>	Algo importante de notar sobre o game.py é a variável dt, que representa o tempo que passou desde o último quadro em ticks. Esse valor vai ser utilizado para calcular velocidades em pixels por tick, e não pixels por quadro, tornando o movimento estável mesmo que a taxa de quadros por segundo flutue. 
Design IU e Armazenamento De Itens Coletados:
> 
> O armazenamento dos itens no mapa foi feito usando o conceito de listas, enquanto a quantidade de itens coletados foi salva por meio de dicionários onde a chave representa o tipo de item. Quanto a da vida do jogador, foi usando um loop for i in range da quantidade máxima de vida do jogador, se i for menor que a vida atual do jogador, é desenhado um coração cheio em coordenadas x baseadas em i; se não, é desenhado um coração vazio na mesma posição onde o coração cheio seria desenhado.  Os itens são separados em duas categorias: itens colecionáveis (pontuação como a moeda e moeda especial e buffs permanentes como os cristais de mana e botas) e itens consumíveis (feitiços de tempo, sobrecarga, e multiplicação). Quando um jogador mata um inimigo, é gerado um número aleatório que determina se o inimigo vai deixar um item e qual tipo de item vai ser esse. Apesar de todos os tipos de itens coletados serem contados pelo dicionário, apenas a quantidade de itens colecionáveis é relevante para o jogador, então esses são mostrados do lado esquerdo logo abaixo dos corações. Como o jogador só pode carregar um item consumível por vez, esse é mostrado no canto superior direito. Caso um novo item consumível seja coletado, mas já tenha um outro item atual, os efeitos do novo item coletado serão ativados automaticamente. Para trocar de item, o jogador precisa primeiro usar o item atual e então coletar o novo item. 
#
## **Mapa.py**:
> Mapa.py é o módulo que cria e desenha o mapa do jogo, na classe mapa. Objetos com colisão como projéteis, inimigos e o jogador acessam as informações dessa classe para fazer essa colisão durante a partida.

- self.mapas:
> self.mapas é o dicionário que irá armazenar as matrizes de inteiros de tamanho 21x21, onde estas irão formar três mapas distintos, um com o tema de floresta, outro com tema de deserto e o último com  tema de cemitério, dando maior variedade ao jogo e tornando-o mais divertido.

- self.tiles:	
> Para desenhar e checar a colisão dos mapas, é preciso usar cada inteiro da matriz para identificar a imagem que vai ser desenhada e o tipo de tile para a colisão. Para isso, usamos um dicionário duplo, onde cada inteiro liga a um valor sprite, a imagem extraída do sprite sheet original de Journey of The Prairie King e ampliadas com .transform para as dimensões apropriadas; e um valor type, que representa o tipo desse tile e vai ser usado para a colisão do jogador, projéteis e inimigos. Existem quatro tipos de tile: tiles de tipo spawn são usados por inimigo.py para determinar as posições de spawn dos inimigos e têm colisão somente com o jogador; os de tipo parede tem colisão com as balas, o jogador e os inimigos; de tipo chão onde tanto balas, inimigos e o jogador podem andar livremente, e os de tipo passar que apenas as balas podem atravessar, mas jogadores e inimigos são bloqueados.

- draw(self):
> A função draw será a responsável por desenhar o mapa, ela irá passar por todas as posições da matriz do mapa atual e desenhar a imagem correspondente na tela usando o dicionário de tiles. Dessa forma a parte de mapas estará pronta para ser adicionada ao game.py.

#
## **Player.py**:
> player.py é o módulo responsável por tudo ligado ao jogador, controle, movimento, colisão com os inimigos e mapas, gerar e atualizar os projéteis, entre outros. Esse módulo cria uma classe player que usa uma lista para guardar os objetos da classe projectile. Fora pygame, player importa projectile.py e math.py.

- check_enemy(self, enemies, ticks):
> check_enemy recebe a lista de inimigos e usa essas informações para calcular se qualquer um dos quatro extremos do sprite do jogador estão tocando um inimigo. Se sim, o jogador perde um de vida, ativa os frames de invulnerabilidade (iframes) do jogador e a função retorna True. Se os iframes do jogador estiverem ativados, a função não vai checar por colisão com inimigos e o jogador não recebe dano, fazendo com que o jogador não possa se machucar durante um certo intervalo depois de ser atingido. Se os iframes estão desativados, a função usa os ticks atuais e a quantidade de ticks no frame em que o jogador levou dano para poder desativar os iframes depois de uma certa quantidade de tempo.

- path_creator(self, mapa)
> Usa Dijkstra para gerar uma matriz de antecessores usada no pathfinding dos inimigos

- control(self, dt, mapa):
> Control é responsável por tudo aquilo ligado aos comandos do jogador, (WASD para se mover, espaço para usar o item atual e o mouse para criar novos projéteis). Para isso, control chama três outras funções, calculate_speed, maior_movimento_valido e new_bullets.

- calculate_speed(self, keys):
> A função calculate_speed usa as teclas pressionadas pelo jogador para determinar qual das oito direções possíveis o jogador está se movendo e usa os parâmetros de velocidade (vel e d_vel) para retornar a velocidade do jogador em cada um dos dois eixos (speedx e speedy) de forma que a soma vetorial das duas projeções seja sempre a mesma. Além de garantir que o jogador não consegue sair da tela jogável, zerando a velocidade em um determinado eixo quando necessário.

- maior_movimento_valido(self, dt, mapa, speedX, speedY):
> Para calcular a nova posição do personagem, basta somar as suas coordenadas atuais as respectivas velocidades multiplicadas pelo dt (x += speedX*dt, y += speedY*dt), porém, é preciso garantir que esse movimento vai respeitar os limites impostos pelo mapa, ou seja, que o jogador não vai poder entrar dentro de um bloco em que ele não deveria conseguir entrar, para isso, podemos checar usar divisão inteira junto com a matriz map e o dicionário tiles do mapa para saber se o bloco da posição final é do tipo ‘chao’ (único tipo de bloco no qual o jogador pode andar). Se for do tipo ‘chao’, podemos fazer o movimento sem problemas, se for de outro tipo, nós poderíamos parar o movimento, mas isso resultaria em o jogador parar antes dele tocar no bloco com o qual ele colidiu, deixando uma brecha de alguns pixels. Para evitar isso, vamos usar um loop while e ir da posição final do jogador caso não houvesse nenhum obstáculo até encontrar uma posição onde ele possa se mover (o maior movimento possível nessa direção) ou até chegar na posição original. Dessa forma, o jogador sempre vai se mover o máximo possível, tocando o bloco onde ele não consegue passar sem deixar nenhuma brecha. Ao fazer isso para os dois eixos, vamos ter a nova posição do jogador. Para saber se o jogador está dentro de um bloco que não deveria, vamos usar os cantos do quadrado do jogador, mas dessa vez, alguns pixels menores que a imagem real do jogador, para permitir que esse passe mais facilmente em passagens de apenas um bloco.
>
> Essa definitivamente não é a melhor forma de fazer esse sistema, muito menos a mais simples, porém, nós tentamos criar esse jogo usando as habilidades que desenvolvemos durante o curso, então tentamos evitar pesquisar soluções prontas para esses tipos de problemas.
(De forma resumida, se um movimento deixa o jogador dentro de um bloco onde ele não deveria conseguir entrar, vamos diminuir esse movimento pixel por pixel até encontrar um movimento que o jogador possa fazer sem desrespeitar os limites do mapa).

- new_bullets(self, keys):
> Usamos os ticks atuais e os ticks na última vez em que o jogador atirou para calcular o tempo desde o último tiro. Comparando esse tempo com o shoot_cooldown podemos garantir que o jogador só consegue atirar seguindo uma determinada cadência. Modificando shoot_cooldown podemos mudar essa cadência livremente. Depois disso, vamos checar se o jogador está apertando o botão esquerdo do mouse, se sim, usamos a posição do mouse em relação ao centro do jogador para calcular o ângulo em que o projétil vai ser lançado, salvamos esse ângulo em uma lista, depois, checamos se o item multi_shot está ativo. Se sim, vamos criar para cada bala mais duas balas com ângulos levemente diferentes. Depois disso, a função add_bullets(self, direction) é chamada e um loop for que passa por todas as direções da lista de ângulos e adiciona um projétil em cada um dos ângulos da lista de projéteis.

- update(self, dt, mapa):
> update é uma função bem simples que chama a função de controle do jogador, atualiza todos os projéteis que existem (baseado no parâmetro existe do objeto projétil) da lista e remove da lista todos os projéteis que não existem mais.

- draw(self):
> Outra função simples, ela desenha todas as balas e desenha o jogador, se o jogador está com frames de invulnerabilidade ativos ele será desenhado apenas nos frames pares para indicar isso.

#
## **Items.py**:
> items é a classe responsável pelos itens, sua colisão com o jogador e fazer com que eles desapareçam do mapa depois de certo tempo. A classe recebe um parâmetro rand aleatório de zero até 62 que determina o tipo de item e suas dimensões. O tipo vai ser usado como uma chave para o dicionário de imagens dos itens e para a coleta de itens do jogador. Importa apenas pygame.

- update(self,t):
> Update destrói o item do mapa caso esse já exista por mais tempo que deveria.
 
- draw(self):
> Desenha o item na tela.

- player_colision(self, player):
> Checa a colisão com o jogador, se o jogador estiver tocando o item, o item deixa de existir e a função retorna o tipo de item coletado, caso contrário, a função retorna -1.

#
## **Inimigo.py**:
> Para o desenvolvimento desse módulo, foi necessário fazer as seguintes importações: pygame, math, random e datetime.
>
> Essa é a classe dos inimigos, ela cria o inimigo em um bloco de spawn aleatório e move ele em linha reta na direção do jogador. O array de tiles é percorrido, adicionando-se a uma lista de coordenadas as tiles do tipo spawn. Dessa lista, usando como seed o instante atual, é escolhida uma posição para colocar.
> 
> A classe inimigo foi utilizada em diversas outras partes do projeto, como para testar a colisão com as balas, para excluir o inimigo caso fosse atingido.
>
> Os inimigos compartilham o mesmo código de colisão com o mapa que o jogador, com a diferença que eles podem se mover em blocos do tipo spawn. Para o seu movimento, é usado algo semelhante ao código do jogador que calcula o ângulo entre o jogador e o mouse e usa isso para gerar uma bala que se move em linha reta nessa direção. A única diferença é que os inimigos tem esse ângulo atualizado a cada frame para que eles sempre se movam na direção do jogador. Dessa forma, é trivial prender um inimigo em um canto, fazendo com que a dificuldade do jogo esteja no gerenciamento de múltiplos inimigos de origens diversas, não de cada inimigo individualmente.


## Bibliotecas/Módulos usada(o)s:
- **Pygame**:
> É a biblioteca principal utilizada em todas as partes do código.
- **Math**:
> Foi utilizada para determinar ângulos e calcular seno e cosseno para o movimento das balas e dos inimigos.
- **Datetime**:
> Foi usada para gerar seeds para o RNG usado na geração dos  itens e da posição de spawn dos inimigos no mapa.
- **Random**:
> Foi usada para gerar números aleatórios para determinar o tipo de itens e a posição de spawn dos inimigos no mapa.
- **Heapq**:
> Foi usada para o algorítmo de menor caminho Dijkstra do jogador, responsável pelo sistema de pathfinding dos inimigos.

## Conceitos:
- **Listas**:
> Listas foram utilizadas várias vezes durante o desenvolvimento do projeto, como nas listas que guardam os inimigos, itens e projéteis, as matrizes que guardam os mapas, a lista de pontuação total que guarda a pontuação de cada uma das três fases de uma partida, listas com as coordenadas dos quatro cantos de um objeto para as colisões, a lista de direções em player.py que serão usadas para criar novas balas, etc.

- **Dicionários**:
> Dicionários foram utilizados em game.py para guardar a quantidade de itens coletados em uma fase e também para guardar as imagens que serão utilizadas para os itens no HUD, além de serem usados em mapa.py e itens.py como explicado anteriormente.

- **Loops**:
> Loops foram usados diversos momentos dentro do código, a função main em game.py consiste em um grande loop while True que só é terminado usando pg.quit(). Esse tipo de loop também foi usado na detecção de colisão do jogador e inimigo com o mapa. Loops for foram usados sempre que foi preciso repetir um processo para todos itens de uma lista de objetos, como por exemplo, checar cada bala para ver se ela está tocando um inimigo, fazer update em todos os itens, inimigos e balas na tela, checar a colisão de cada item com o jogador e salvar esse item coletado nos dicionários correspondentes, etc. Loops for também foram utilizados para desenhar os corações na tela, passar por todas as casas do mapa para encontrar os tiles spawn quando um novo inimigo é criado, para desenhar cada tile do mapa, para o efeito do item multi_shot, etc.

- **Classes e Funções**:
> Foram usadas para modularizar o código, permitindo a cada integrante trabalhar com certa independência.

## Desafios/Experiência:

> Coordenar o trabalho da equipe, quem vai fazer o que, como cada pessoa está fazendo sua parte, como juntar o que foi feito, assim como o uso do github, ferramenta que muitos dos membros do grupo não estavam familiarizados, foram alguns dos maiores problemas encontrados, a forma como nós organizamos o GitHub foi por meio de um único repositório do qual todos criaram forks, onde novas features eram desenvolvidas e passadas para o repositório original usando pull requests, o que pode não ter sido a melhor abordagem, visto que ter que manter o fork atualizado com o repositório original assim como criar pull request para qualquer pequena mudança criou uma camada de dificuldade que poderia não existir se todos estivessem trabalhando em um único repositório, cada um com o seu branch. Esses problemas foram agravados pelo trabalho remoto. Se esse fosse um período convencional, nós poderíamos marcar horários para trabalhar em conjunto pessoalmente no laboratório, ajudando um ao outro e melhor controlando o desenvolvimento do projeto. Outra grande dificuldade para a maioria do grupo foi se familiarizar com uma ferramenta nunca utilizada antes, aprender a usar Pygame para desenvolver um jogo, mesmo que ‘simples’, foi difícil para boa parte dos membros. 

#
###### *Projeto referente a matéria de Introdução a programação/CIN-UFPE no periodo de 2020.2. Começamos em 12/08/2021*
