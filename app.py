import socket
import ssl
import sys
import argparse

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
def parse_args():
    parser = argparse.ArgumentParser(description="Teste de Conexão SSL/TLS")

    parser.add_argument("--cert", required=True, help="Caminho para o certificado .crt")
    parser.add_argument("--targets", required=True, help="Lista de alvos no formato ip:port separados por vírgula (ex: 192.168.1.1:443,192.168.1.2:443)")

    return parser.parse_args()

def main():
    args = parse_args()
    
    cert_path = args.cert
    targets = args.targets.split(",")

    for target in targets:
        ip, port = target.split(":")
        test_connection(ip.strip(), int(port.strip()), cert_path)

if __name__ == "__main__":
    main()
