"""
Script para verificar qualidade do código
"""

import subprocess
import sys


def run_command(cmd, description):
    """Executa um comando e retorna o resultado"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}\n")

    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0


def main():
    """Função principal"""
    all_passed = True

    # Verifica formatação com black
    if not run_command(
        "black --check src/ tests/ --line-length=100",
        "Verificando formatação com Black"
    ):
        print("\n❌ Formatação incorreta. Execute: make format")
        all_passed = False
    else:
        print("\n✅ Formatação OK")

    # Verifica linting com flake8
    if not run_command(
        "flake8 src/ tests/ --max-line-length=100",
        "Verificando código com Flake8"
    ):
        print("\n❌ Problemas encontrados no código")
        all_passed = False
    else:
        print("\n✅ Linting OK")

    # Executa testes
    if not run_command(
        "pytest tests/ -v",
        "Executando testes"
    ):
        print("\n❌ Testes falharam")
        all_passed = False
    else:
        print("\n✅ Testes OK")

    print(f"\n{'='*60}")
    if all_passed:
        print("✅ TODOS OS CHECKS PASSARAM!")
        print(f"{'='*60}\n")
        return 0
    else:
        print("❌ ALGUNS CHECKS FALHARAM")
        print(f"{'='*60}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
