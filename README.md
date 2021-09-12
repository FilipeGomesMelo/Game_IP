# Untitled Wizard Game
  Untitled Wizard Game é um jogo top-down shooter desenvolvido usando Pygame baseado no minigame _Journey of The Prairie King_ de _Stardew Valley_, de onde tiramos grande parte dos sprites além da música de fundo. O jogador controla um mago e deve matar as hordas de zumbis para coletar moedas que servem como pontuação, utilizando os itens que os inimigos dropam para poder se manter vivo o máximo de tempo possivel e coletar a maior quantidade de moedas antes de morrer e passar para a próxima fase. 

  Os itens são:
  - moedas simples (1 ponto)
  - moedas especiais (10 pontos)
  - botas aladas (aumento permanente de velocidade movimento)
  - critais mágicos (aumento permantente de velocidade de tiro)
  - pergaminho vermelho (aumento temporário de velocidade de tiro)
  - pergaminho roxo (aumento temporário da quantidade de tiros)
  - pergaminho azul (temporariamente paralisa os inimigos)

  O jogador começa cada fase com 3 de vida, perdendo um de vida sempre que colide com um inimigo, as botas e cristais são upgrades permanentes enquanto os pergaminhos são itens consumíveis, podendo ter mais de um ativo ao mesmo tempo, mas apenas guardando um no inventário de cada vez, se você já tem um pergaminho no iventário e coleta um novo pergaminho esse pergaminho sera usado automaticamente.

## Divisão de tarefas:
|            Equipe              |          Tarefas           |
| ------------------------------ | -------------------------- |
| **Filipe Gomes** | Jogador, Itens e Projéteis |
| **Humberto Lima Felipe Guimarães** | Inimigos |
| **Rodrigo Moura** | Mapas |
| **Jonathas Vinicius** | UI e HUD |
| **Felipe Guimarães** | Novos Sprites |

## Link para o codigo fonte:
- https://github.com/tvas20/death_maze

## Organização do código:
  O código é separado em seis módulos, cada um contendo uma ou mais classes responsáveis pelo funcionamento do jogo, o módulo _game_ é o componente principal liga todos os outros:
- **Game.py**:
> game.py é o nosso arquivo principal e o arquivo que você vai executar para rodar o jogo, nele temos a nossa função main com o loop infinito que vai rodar o jogo e algumas outras funções secundárias.
- **Mapa.py**:
> mapa.py é o módulo responsável por criar e desenhar os mapas, e é utilizado para determinar a colisão das balas, do jogador e dos inimigos com o cenário.
- **Player.py**:
> player.py é o módulo responsável por tudo aquilo ligado ao jogador, o seu movimento, vida, dano, entre outras coisas. player.py também é responsável por gerar, atualizar e desenhar as balas atiradas pelo jogador.
- **Items.py**:
> items.py é o módulo responsável pelos itens que aparecem no mapa e sua colisão com o jogador.
- **Inimigo.py**:
> inimigo.py é o módulo responsável pelos inimigos, seu movimento, sua colisão com o mapa e a animação que aparece quando um inimigo é morto
- **Projectile.py**:
> projectile.py é o módulo dos projéteis do jogador, seu movimento, sua colisão com inimigos e com o mapa.

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

- **Github**:
> Inicialmente, o _Github_ foi um grande desafio para todos no grupo, pois poucos tinham conhecimento dessa ferramenta. Muitos conceitos foram aprendidos a partir de seu estudo, tanto a criação de um novo repositório quanto fazer um _git pull_, _pull request_, criar _branch_, e até mesmo aprender a formatação texto de um arquivo legivel (_README_).   
- **Programação em equipe**:
> A programação em equipe já é um grande desafio, e se torna ainda maior quando se usa uma ferramenta (Github) que pouco se conhece, ou que não se tem muita experiencia, contudo a programação em equipe se torna vantajosa apartir do momento que se encontram algumas barreiras e dificuldades, pois algumas dificuldades para alguns podem não ser para outros e vice-versa.
- **Pygame**:
> O _pygame_ foi um dos grandes desafios para toda equipe, pois foi um instrumento de uso obrigatório, em que todos deveriam saber sobre e entender o mínimo, para de imediato começarmos a trabalhar. Muitas coisas foram aprendidas com o uso dessa vasta biblioteca, que vai desde a criação de um simples quadrado movél na tela, até um jogo mais complexo conforme foi apresentado em nosso projeto. 

#
###### *Projeto referente a matéria de Introdução a programação/CIN-UFPE no periodo de 2020.2. Começamos em 12/08/2021*
