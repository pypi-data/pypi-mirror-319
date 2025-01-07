import logging
import sys
from colorama import Fore, Style, init
from datetime import datetime

# Inicializa o Colorama para compatibilidade com Windows
init(autoreset=True)

class LoggerManager:
    def __init__(self):
        self.logger = None

    def setup_logger(self, name="GlobalLogger", level=logging.DEBUG):
        """Configura o logger"""
        if self.logger:
            return self.logger  # Retorna o logger já configurado

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Formatação do log com cores e data personalizada
        formatter = self.ColoredFormatter('%(levelname)s: %(message)s')

        # Handler para console
        if not self.logger.handlers:  # Evita adicionar handlers duplicados
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        # Adiciona nível "success" customizado
        self.add_success_level()

        return self.logger

    def add_success_level(self):
        """Adiciona um nível customizado chamado SUCCESS"""
        logging.SUCCESS = 25  # Define o nível entre INFO (20) e WARNING (30)
        logging.addLevelName(logging.SUCCESS, "SUCCESS")

        def success(self, message, *args, **kwargs):
            if self.isEnabledFor(logging.SUCCESS):
                self._log(logging.SUCCESS, message, args, **kwargs)
                
        logging.Logger.success = success

    def setup_global_exception_handler(self):
        """Substitui o excepthook para capturar exceções globais"""

        def global_exception_handler(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                # Permite que KeyboardInterrupt não seja tratado como erro
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return

            # Loga a exceção como erro
            self.logger.error(
                exc_value,
                exc_info=(exc_type, exc_value, exc_traceback)
            )

        # Substitui o excepthook padrão
        sys.excepthook = global_exception_handler

    class ColoredFormatter(logging.Formatter):
        """Formatter personalizada para adicionar cores e formatação de data"""
        COLOR_MAP = {
            "DEBUG": Fore.BLUE,
            "INFO": Fore.CYAN,
            "WARNING": Fore.YELLOW,
            "ERROR": Fore.RED,
            "CRITICAL": Fore.RED + Style.BRIGHT,
            "SUCCESS": Fore.GREEN,
        }
        
        def format(self, record):
            dt = datetime.fromtimestamp(record.created)
            time_str = dt.strftime('%d/%m/%Y - %H:%M:%S.%f')[:-3]  # Remove os últimos 3 dígitos dos microssegundos
            levelname = record.levelname
            color = self.COLOR_MAP.get(levelname, "")
            record.levelname = f"{color}{time_str} - {levelname}{Style.RESET_ALL}"  # Aplica a cor e reseta após
            return super().format(record)
