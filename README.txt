1. Instruções para execução do microserviço:
    *  docker-compose build (Caso nao tenha sido feito ainda)
    *  docker-compose up -d 


2. Justificativa do padrão SAGA escolhido:
    Nosso grupo chegou no consenso de que o melhor modelo para ser utilizado em nosso projeto é o de coreografia. 

    Nosso projeto está dividido em 3 microserviços com 3 pessoas diferentes, e uma das vantagens da SAGA coreografada 
    é justamente o desacoplamento de cada serviço, ou seja, eles podem ser autonomos e responsáveis pela sua prórpia lógica de transação, 
    logo, possibilitando uma maior flexibilidade e escalabilidade. Nos possibilita a usar diferentes tecnologias como vem sendo feito e diferentes 
    modos de implementações.

    A respeito da escabilidade, como não existe um único ponto central de coordenação (orquestrada), ela se torna muito melhor, pois não existe gargalo de desempenho.

    Pensando agora no ambiente de serviço de Fastfood, precisamos garantir a disponibilidade, ou seja, se um serviço falhar durante uma transação, 
    os outros serviços permanecem em execução sem depender do "controle central". Alem disso, sabemos que é um setor muito dinâmico, em alguns momentos podemos ter
    uma grande demanda e em outros nem tanto, mais um ponto onde nao podemos depender de um orquestrador para distribuicao dos serviços.

    Por fim, não podemos deixar de falar sobre desacoplamento, um sistema de fast food possui várias operações senda executadas a todo momento(pedidos, pagamentos, entregas),
    o modelo coreografado nesse cenário, nos possibilita que os servicos rodem de forma independente.

3. 

    "C:\Users\gusta\2024-03-18-Report-Produtos.html"
    "C:\Users\gusta\2024-03-18-Report-Pedido.html"

4. Relatório RIPD

5. Desenho Arquitetura

6. Link do vídeo






