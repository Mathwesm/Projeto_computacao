"""
Utilitários de tempo
Funções para manipulação e formatação de tempo
"""

import time
from typing import Optional


def format_time(seconds: float) -> str:
    """
    Formata tempo em segundos para formato legível

    Args:
        seconds: Tempo em segundos

    Returns:
        String formatada 'MM:SS' ou 'HH:MM:SS'
    """
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


def get_timestamp() -> float:
    """
    Retorna o timestamp atual em segundos

    Returns:
        Timestamp em segundos
    """
    return time.time()


class Timer:
    """
    Classe para controle de tempo e cronômetro
    """

    def __init__(self):
        """Inicializa o timer"""
        self._start_time: Optional[float] = None
        self._pause_time: Optional[float] = None
        self._elapsed_paused: float = 0.0
        self._is_running: bool = False
        self._is_paused: bool = False

    def start(self) -> None:
        """Inicia o timer"""
        if not self._is_running:
            self._start_time = time.time()
            self._elapsed_paused = 0.0
            self._is_running = True
            self._is_paused = False

    def stop(self) -> float:
        """
        Para o timer e retorna o tempo decorrido

        Returns:
            Tempo decorrido em segundos
        """
        if self._is_running:
            elapsed = self.get_elapsed()
            self._is_running = False
            self._is_paused = False
            self._start_time = None
            self._pause_time = None
            self._elapsed_paused = 0.0
            return elapsed
        return 0.0

    def pause(self) -> None:
        """Pausa o timer"""
        if self._is_running and not self._is_paused:
            self._pause_time = time.time()
            self._is_paused = True

    def resume(self) -> None:
        """Resume o timer após pausa"""
        if self._is_running and self._is_paused:
            if self._pause_time is not None:
                self._elapsed_paused += time.time() - self._pause_time
            self._pause_time = None
            self._is_paused = False

    def reset(self) -> None:
        """Reseta o timer"""
        self._start_time = time.time() if self._is_running else None
        self._pause_time = None
        self._elapsed_paused = 0.0
        self._is_paused = False

    def get_elapsed(self) -> float:
        """
        Retorna o tempo decorrido em segundos

        Returns:
            Tempo decorrido
        """
        if not self._is_running or self._start_time is None:
            return 0.0

        if self._is_paused and self._pause_time is not None:
            return self._pause_time - self._start_time - self._elapsed_paused

        return time.time() - self._start_time - self._elapsed_paused

    def get_elapsed_formatted(self) -> str:
        """
        Retorna o tempo decorrido formatado

        Returns:
            Tempo formatado como string
        """
        return format_time(self.get_elapsed())

    @property
    def is_running(self) -> bool:
        """Verifica se o timer está rodando"""
        return self._is_running

    @property
    def is_paused(self) -> bool:
        """Verifica se o timer está pausado"""
        return self._is_paused


class FPSCounter:
    """
    Contador de FPS (Frames Per Second)
    """

    def __init__(self, sample_size: int = 60):
        """
        Inicializa o contador de FPS

        Args:
            sample_size: Número de frames para calcular média
        """
        self.sample_size = sample_size
        self.frame_times = []
        self.last_time = time.time()

    def tick(self) -> None:
        """Registra um frame"""
        current_time = time.time()
        delta_time = current_time - self.last_time
        self.last_time = current_time

        self.frame_times.append(delta_time)
        if len(self.frame_times) > self.sample_size:
            self.frame_times.pop(0)

    def get_fps(self) -> float:
        """
        Retorna o FPS atual

        Returns:
            FPS médio
        """
        if not self.frame_times:
            return 0.0

        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        if avg_frame_time == 0:
            return 0.0

        return 1.0 / avg_frame_time

    def reset(self) -> None:
        """Reseta o contador"""
        self.frame_times.clear()
        self.last_time = time.time()
