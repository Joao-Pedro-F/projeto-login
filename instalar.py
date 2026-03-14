
import subprocess
import sys

def install_requirements():
    """Instala todas as dependências do requirements.txt"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Todas as dependências foram instaladas com sucesso!")
    except subprocess.CalledProcessError:
        print("❌ Ocorreu um erro ao instalar as dependências.")

if __name__ == "__main__":
    install_requirements()