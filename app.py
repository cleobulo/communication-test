import socket
import ssl
import sys

def test_connection(ip, port, cert_path):
    print(f"--- Testando {ip}:{port} ---")
    
    # Criação do contexto SSL
    context = ssl.create_default_context()
    
    # Carrega o seu certificado .crt
    try:
        context.load_verify_locations(cert_path)
    except Exception as e:
        print(f"Erro ao carregar certificado: {e}")
        return

    # Tenta a conexão via socket
    try:
        # Define um timeout para não travar o script
        with socket.create_connection((ip, port), timeout=5) as sock:
            # Tenta envolver o socket com a camada SSL
            with context.wrap_socket(sock, server_hostname=ip) as ssock:
                print(f"Conexão estabelecida com sucesso!")
                print(f"Versão SSL/TLS: {ssock.version()}")
                # Opcional: imprimir dados do certificado do servidor
                # print(ssock.getpeercert())
    except socket.timeout:
        print(f"Erro: Timeout ao tentar conectar em {ip}:{port}")
    except ssl.SSLError as e:
        print(f"Erro de SSL (Handshake falhou): {e}")
    except ConnectionRefusedError:
        print(f"Erro: Conexão recusada pelo servidor {ip}:{port}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    print("-" * 30)

# --- Configurações ---
CERTIFICADO = ""
ALVOS = [
    {"ip": "", "port": 0},
    {"ip": "", "port": 0}
]

if __name__ == "__main__":
    for alvo in ALVOS:
        test_connection(alvo["ip"], alvo["port"], CERTIFICADO)
