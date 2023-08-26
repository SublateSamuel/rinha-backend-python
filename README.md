# API de Alta Escalabilidade com FastAPI, PostgreSQL, Redis e RabbitMQ

Este projeto é uma prova de conceito (PoC) de uma API de alta escalabilidade construída usando o framework FastAPI, juntamente com tecnologias como PostgreSQL, Redis, RabbitMQ e Celery. A PoC foi projetada para demonstrar a capacidade de lidar com cargas intensivas de requisições e manter um desempenho eficiente, garantindo a escalabilidade.

## Tecnologias Utilizadas

- **FastAPI**: Um framework moderno e de alto desempenho para a construção de APIs em Python.
- **PostgreSQL**: Um sistema de gerenciamento de banco de dados relacional para armazenar informações de pessoas.
- **Redis**: Um sistema de cache em memória, utilizado para otimizar o acesso a dados frequentemente consultados.
- **RabbitMQ**: Um sistema de mensagens que possibilita a execução de tarefas assíncronas em segundo plano.
- **Celery**: Uma biblioteca que trabalha em conjunto com um message broker para facilitar o agendamento e a execução de tarefas assíncronas.
- **Docker Compose**: Uma ferramenta para orquestrar múltiplos contêineres e criar um ambiente de desenvolvimento consistente.

## Rotas Implementadas

### GET /pessoas/{pessoa_id}

Esta rota permite recuperar informações detalhadas sobre uma pessoa específica com base no ID fornecido. Ela aproveita o cache Redis para otimizar o acesso aos dados e, caso necessário, recupera informações do banco de dados PostgreSQL. Isso garante uma resposta rápida e eficiente para a consulta.

### GET /pessoas?t=<term>

Esta rota permite realizar pesquisas por pessoas com base em um termo de busca fornecido como parâmetro de consulta.

### GET /contagem-pessoas

Esta rota retorna o número total de pessoas armazenadas no banco de dados PostgreSQL.

### POST /pessoas

Esta rota permite criar uma nova entrada de pessoa no banco de dados. Ela realiza as seguintes etapas:
- Valida se o apelido da pessoa já está em uso usando o sistema de cache.
- Gera um ID único para a pessoa.
- Armazena a pessoa no banco de dados PostgreSQL.
- Inicia uma tarefa assíncrona para inserir a pessoa no banco de dados usando Celery.

   **Dados do Schema e Validações:**
   
   Ao enviar uma requisição POST para esta rota, você deve fornecer os dados do usuário no corpo da requisição. Os dados do usuário são validados de acordo com o seguinte schema:

   ```python
   class PessoaSchema(BaseModel):
       apelido: str
       nome: str
       nascimento: str
       stack: Optional[List[str]] = None
   ```

   Os seguintes validadores são aplicados:

   - `apelido`: Deve ser uma string única que identifica o apelido da pessoa.
   - `nome`: Nome da pessoa.
   - `nascimento`: Data de nascimento da pessoa no formato AAAA-MM-DD.
   - `stack`: Lista opcional de strings, onde cada item deve ter no máximo 32 caracteres.

   Além disso, os campos `nome`, `apelido` e `nascimento` não podem ser nulos e devem ser strings válidas.

## Execução da PoC

Siga estas etapas para executar a prova de conceito:

1. Clone este repositório para o seu sistema local.

2. Certifique-se de ter o Docker Compose instalado em seu ambiente.

3. Navegue até o diretório do projeto no terminal.

4. Execute o seguinte comando para iniciar os serviços definidos no arquivo `docker-compose.yml`:

   ```bash
   docker-compose up -d
   ```

5. Aguarde até que todos os contêineres estejam em execução.

6. Acesse a documentação interativa da API em seu navegador, utilizando o URL `http://localhost:9999/docs`.

## Considerações Finais

Esta PoC oferece um vislumbre de como construir uma API robusta e escalável utilizando tecnologias modernas e práticas de desenvolvimento. Ela destaca a importância de utilizar cache para otimização de consultas, tarefas assíncronas para melhorar a performance geral da aplicação e validações sólidas para garantir a integridade dos dados recebidos. Este projeto pode servir como ponto de partida para a construção de aplicações maiores e mais complexas que exigem alta escalabilidade. Certifique-se de personalizar as configurações conforme necessário e explorar ainda mais as funcionalidades avançadas das tecnologias empregadas.