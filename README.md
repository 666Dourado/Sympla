# Desafio Sympla
 Markdown do Desafio proposto pela Sympla
 
 
 O intuito desse projeto é ober informações de eventos do site da [Sympla](https://www.sympla.com.br/), armazena-los em um banco de dados, analiza-los e criar uma API que disponibilize as informações de um evento atraves de um Id Evento.
 
Abaixo temos a estrutura básica do projeto.

![Estrutura Projeto](https://i.pinimg.com/originals/62/77/d4/6277d4ed4cf4f274e116a24dee1b45ce.png)


## Tecnologias Utilizadas:

1. Serviço de Obtenção dos Eventos: Python, Selenium, Beautiful Soup e Py.Test
2. Banco de Dados: PostgreSQL
3. API: Python e Flask
4. Extras: Power BI (Utilizado para fazer analises adicionais dos dados)


## Descrição dos Entregaveis:

### Serviço de Obtenção dos Eventos

#### Panorama do Serviço
Como já citado esse serviço tem o intuito de obter os dados dos enventos do site da Sympla e armazena-los num banco de dados. Para coletar os dados do site utilizei uma técnica chamada de [Web Scraping](https://blogbrasil.westcon.com/o-que-e-web-scraping), que resumidademente é o ato de criar robôs para percorrer e coletar informações de um site utilizando o codigo fonte visivel no inspetor de elementos.

O sistema funciona da seguinte maneira, primeiramente ele percorre a tabela tb_tipoevento, que é uma tabela no banco contendo todos os tipos eventos que há no site. Desenvolvi dessa maneira pois notei que ao navegar pela página solcitando o carregamento de mais eventos chegava num ponto que não trazia mais eventos, (numero da ordem de 10.000 eventos) por isso decidi buscar por tipo evento e também ganharia em mais um parametro para análise.


![Tabela tb_tipoevento](https://i.pinimg.com/originals/42/ae/6b/42ae6b97dc9d581594ead3227284843a.png)


Ao percorrer essa tabela, pego o primeiro registro com o status sendo igual a zero, abro uma guia no navegador utilizando o Selenium, passando a url com o tipo evento. Exemplo: https://www.sympla.com.br/eventos/festas-shows


![Pagina Selenium](https://i.pinimg.com/originals/81/e3/26/81e32684653c35c9a149ae1a2a146fbe.png)


Utilizei o Selenium para abrir a página ao invez de outras ferramentas de Web Scraping pois com ela posso navegar por páginas de forma natural, solcitando mais dados "clicando" de forma automatizada no botao "Carregar Mais".

Sendo assim, ao abrir o navegador, o sistema percorre todos os eventos, salvando os dados de URL, Tipo Evento e Data Criação no banco, ao encontrar um evento e obter a URL, utilizo outra ferramenta de Web Scraping para recuperar os demais dados do evento. Com o Beautiful Soup realizo um request nos dados da pagina da URL capturada anteriomente, obtendo assim os demais dados como Loca, Data, Nome Evento, etc.

Resumidamente, com o Selenium obtenho as URLs percorrendo a pagina principal sem entrar evento por evento e com o Beautiful Soup realizo a obtenção dos dados dos eventos por meio do request na página.

Após fazer isso salvo esses dados no banco de dados.


![tb_eventos](https://i.pinimg.com/originals/25/9f/3b/259f3bb9fa3908b6d4f41daab5c94e3e.png)


Após percorrer todos os eventos desse Tipo Evento, o sistema passa para o proximo Tipo Evento e ao terminar todos eles ele volta para o primeiro fazendo um loop sem fim, coletando todos os eventos 24x7.

Um ponto importante a ser destacado é que eu não consegui recuperar os eventos de todas as URLs que coletei. Isso porque existem paginas diferentes que não seguem um padão. Caso seja continuado o projeto seria importante mapear todos os tipos de paginas existentes. Por exemplo existe eventos na pagina "www.sympla.com.br" e na "https://bileto.sympla.com.br"

Para se ter uma ideia, dos 19.406 URLs coletadas, consegui obter dados de 85%. 

![Contagem de Eventos](https://i.pinimg.com/originals/1c/02/8a/1c028a891e28ec714f76305043e3be64.png)


#### Pastas do Serviço e Arquitetura

As pastas e os arquivos estão dispostos da seguinte forma:

- Sympla - Web Scraping
>       Config
>          banco.py
>       Controller
>          controller.py
>          controllerBanco.py
>          controllerAuxiliar.py
>          test_pytest.py
>       Scraper
>          scraper.py
>       Service
>          service.py
>       __init__py


O serviço foi desenvolvido de forma que ao iniciar é feito uma chamada no serviçe que faz o gerenciamento da Controller que por sua vez controla as demais ações no sistema, cominicando com a controller de banco quando necessita de fazer alguma ação no banco ou com a scraper quando solicita algum dado do site da Sympla.


### Banco de Dados
Como já dito foi usado o banco PostgreSQL para persistir os dados desse projeto e o pgAdmin para a interfaçe Web.

O sistema utiliza de 4 tabelas para seu funcionamento.


![Tabelas](https://i.pinimg.com/originals/52/c8/fa/52c8fa89c4ad001e36f9c1e76581e757.png)


A tb_eventos e a tb_tipoevento já visualizamos a suas utilizades, quanto a tb_datas é nela que armazeno todas as datas de um determinado evento. Por exemplo, se um evento inicia no dia 15/09/2019 ao dia 18/09/2019 o mesmo possui uma duração de 4 dias, se inicia num domingo e finaliza numa quarta feira. Com esses dados eu consigo saber a distribuição dos eventos por dia da semana.

![tb_datas](https://i.pinimg.com/originals/8d/8b/72/8d8b7254de56057b1c327e87ed791aa0.png)

Na tb_valoringresso eu armazeno o valor de todos os ingressos por lote e por evento, com isso tenho a informação de todos os ingressos e na tb_eventos armazeno somente o valor de ingresso mais caro por evento.

![tb_valoringresso](https://i.pinimg.com/originals/ce/a2/73/cea2736c7ec3352db6093ef0da6da381.png)


Observando agora na tb_eventos:

![tb_eventos](https://i.pinimg.com/originals/5c/66/f2/5c66f235df954cd8470afea0540dbf56.png)


### Análises

Com os dados salvos no banco, podemos partir para responder as seguintes perguntas:

Qual é a localidade com maior volume de eventos ?

Fazendo uma consulta obtendo a quantidade de eventos por cidade e por estado verifiquei que São Paulo - SP possui o maior volume de eventos com 2674 eventos.

![evento_cidade](https://i.pinimg.com/originals/b1/64/d3/b164d3ed1cbcb1b6231c4d866d5ba94b.png)

![evento_estado](https://i.pinimg.com/originals/9d/bc/ba/9dbcbabe4601034d4d0a9c95a83b1068.png)

Graficamente:

![evento_localidade](https://i.pinimg.com/originals/b8/0b/45/b80b4549e7e0acb268beb62e5667e0e5.png)

Qual é a quantidade média de lotes (tipos de tickets) por eventos ?

Somanto todos os lotes 31.679 e dividindo pela quantidade de eventos 16.587, obtive a média de 1.9 lotes por evento.

![media_lotes](https://i.pinimg.com/originals/b4/93/a2/b493a25370540bb1d06dff4ecb3c4be5.png)

- Qual é a frequencia de eventos por dia da semana ?

Fazendo uma consulta obtive os seguintes resultados:

![eventos_semana](https://i.pinimg.com/originals/02/f6/44/02f644e4cecb30690f45b8b816817323.png)

Graficamente:

![eventos_semana_grafico](https://i.pinimg.com/originals/23/bc/97/23bc974e9568594615a31ee4b4e05655.png)

Podemos observar que de segunda a sabado o numero de eventos vai crescendo e no domingo há uma brusca redução.

Dos eventos coletados, qual possui maior valor de ingresso ?

Realizando uma analise pude verificar que o ingresso mais caro é do evento Master Valley Governanca Nova Economia, com um ingresso de R$ 9.999,99. Link do evento: https://www.sympla.com.br/master-valley---governanca--nova-economia__566380

![ingresso](https://i.pinimg.com/originals/6a/a3/7f/6aa37fa3196db9e2b3e5406b75c27888.png)

![ingresso](https://i.pinimg.com/originals/66/c1/73/66c1730f12481a00aaae3b58a698bdcd.png)

![ingresso](https://i.pinimg.com/originals/f4/69/d0/f469d08f91614aafe61e87edcd8219f1.png)


### Extras
Foi proposto alguns desafios extras, que foram os seguintes:

- Testes automatizados
- Executar o programa dentro de um container
- Construir uma API
- Ler o link para o Facebook da descrição dos enventos

Dos quais desenvolvi os seguintes:
- Testes automatizados
- Construir uma API

Testes automatizados.

Utilizando a biblioteca Pytest criei alguns casos de testes automatizados para alguns métodos da aplicação.

![pytest](https://i.pinimg.com/originals/a2/ef/b6/a2efb691a9ef80327258e418261b5cf2.png)


Api eventos

Utilizando Python e Flask desenvovi uma api para que ao passar o id de um evento retornasse os dados desse evento.

Codigo Fonte:

![API_eventos](https://i.pinimg.com/originals/2e/f3/70/2ef370b4042ad39572cfeacf00d7815f.png)

Exemplo do funcionamento:

![API](https://i.pinimg.com/originals/47/8e/55/478e550011940502aec0c58491776ae2.png)


Alem do que foi solicitado, tomei a liberdade de criar um dashboard no Power BI para ter uma melhor visibilidade das análises. O arquivo do Power BI encontra-se tambem no repositorio do projeto.

![analises](https://i.pinimg.com/originals/30/1e/34/301e34896ea1e482251404e690a75520.png)


Com esse dashboad consegui visualizar a distribuição dos eventos pelo tipo de evento e constatar que grande parte dos eventos são do tipo Aprender e Negocios, o que corresponde a 67% do total de eventos. Verifiquei que cerca de 77% dos eventos são pagos e que 96% dos eventos não são online. E que 428 eventos são de outro site chamado Bileto.

### Considerações Finais

Eu utilizei o Trello para organizar as tarefas desse projeto:

![trello](https://i.pinimg.com/originals/a5/a7/6c/a5a76ceb2850431c7ec2c8d6fe65f9f7.png)


Podem perceber que das tarefas que me propus a fazer, 3 não foram concluidas. 
- ORM do banco de dados (queria desenvolver com o Pony o orm para persistir os dados do Python para o PostgreSQL)
- Rodar a API no Docker
- Descobrir quais eventos tem menção ao Facebook


Quero mais uma vez agradeçer a oportunidade e dizer que esse projeto alem de desafiador foi divertido.
Obrigado.




