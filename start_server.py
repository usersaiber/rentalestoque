import os
import subprocess

def start_django_server():
    try:
        # Caminho para o diretório do projeto
        project_dir = r"C:\Users\cleiton.teixeira\OneDrive - Mantomac\TI\rental_system"

        # Mude para o diretório do projeto
        os.chdir(project_dir)

        # Executa o comando para iniciar o servidor
        subprocess.run(["python", "manage.py", "runserver", "0.0.0.0:8080"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao iniciar o servidor: {e}")
    except FileNotFoundError as fnf_error:
        print(f"Arquivo não encontrado: {fnf_error}")
    except Exception as ex:
        print(f"Erro inesperado: {ex}")
    finally:
        print("\nPressione Enter para fechar o programa...")
        input()  # Pausa para visualizar mensagens

if __name__ == "__main__":
    print("Iniciando o servidor Django...")
    start_django_server()
