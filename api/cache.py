from redis import Redis

cache = Redis(
    host="redis",   # Endereço do servidor Redis
    port=6379,      # Porta padrão do Redis
    db=0,           # Número do banco de dados
    socket_keepalive=True,   # Manter conexões ativas
    health_check_interval=30,  # Intervalo para verificar a saúde da conexão
    max_connections=20,
)
