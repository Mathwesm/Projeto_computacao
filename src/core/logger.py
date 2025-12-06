"""
Sistema de logging centralizado para o projeto
Fornece loggers configurados para diferentes módulos
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str,
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    console: bool = True
) -> logging.Logger:
    """
    Configura e retorna um logger

    Args:
        name: Nome do logger (geralmente __name__ do módulo)
        level: Nível de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Caminho para arquivo de log (opcional)
        console: Se deve logar no console

    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Evita duplicação de handlers
    if logger.handlers:
        return logger

    # Formato dos logs
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler para console
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # Handler para arquivo
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str, debug: bool = False) -> logging.Logger:
    """
    Retorna um logger configurado com configurações padrão

    Args:
        name: Nome do logger
        debug: Se True, usa nível DEBUG

    Returns:
        Logger configurado
    """
    level = logging.DEBUG if debug else logging.INFO
    log_dir = Path('logs')
    log_file = log_dir / 'game.log'

    return setup_logger(name, level=level, log_file=log_file, console=True)
