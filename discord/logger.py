class Logger:
    """A utility class for logging messages, supporting log levels, color-coded console output, 
        optional file logging, and redaction of sensitive information. 
    """
    DEBUG = '\033[36m'
    """Debug color: CYCAN"""

    INFO = '\033[32m'
    """Info color: GREEN"""

    WARNING = '\033[33m'
    """Warning color: YELLOW"""

    ERROR = '\033[31m'
    """Error color: RED"""

    CRITICAL = '\033[41m'
    """Critical color: RED HIGHLIGHT"""

    TIME = '\033[90m'
    """Timestamp color: GRAY"""

    RESET = '\033[0m'
    """Reset color: DEFAULT"""
    
    def __init__(self, dev_mode: bool = False, quiet: bool = False):
        """Initializes logger. Opens log file 'bot.log' for writing.

        Args:
            dev_mode (bool, optional): toggle debug messages. Defaults to False.
            quiet: (bool, optional): supress low-priority logs (INFO, DEBUG, WARN). Defaults to False.
        """
        try:
            self.fp = open('bot.log', 'w', encoding="utf-8")
            """Log file for writing."""
        except Exception as e:
            self.log_error(f"Error {type(e)}: {e}")
            self.log_traceback()

        self.dev_mode = dev_mode
        """If debug logs should be printed."""

        self.quiet = quiet
        """If only high-level logs should be printed."""
    
    def now(self):
        """Returns current timestamp

        Returns:
            (str): timestamp formatted in YYYY-MM-DD HH:MM:SS
        """
        from datetime import datetime
        
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def log_traceback(self):
        if self.dev_mode == True:
            import traceback
            self._log("DEBUG", self.DEBUG, traceback.format_exc())
    
    def _log(self, level: str, color: str, message: str):
        """Internal helper that writes formatted log to both file and console.

        Args:
            level (str): DEBUG, INFO, WARN, CRITICAL, ERROR
            color (str): color specified by Logger properties
            message (str): descriptive message to log
        """
        if self.quiet and level not in ('ERROR', 'CRITICAL', 'HIGH'):
            return # suppress lower-level logs in quiet mode
        
        date = self.now()
        self.fp.write(f"[{date}] {level}: {message}\n")
        self.fp.flush()
        print(f"{self.TIME}[{date}]{self.RESET} {color}{level}:{self.RESET} {message}\n")
    
    def log_debug(self, message: str):
        """Logs a debug-level message.

        Args:
            message (str): descriptive message to log
        """
        if self.dev_mode == True:
            self._log("DEBUG", self.DEBUG, message)
    
    def log_info(self, message: str):
        """Logs a info-level message.

        Args:
            message (str): descriptive message to log
        """
        self._log("INFO", self.INFO, message)
    
    def log_warn(self, message: str):
        """Logs a warn-level message.

        Args:
            message (str): descriptive message to log
        """
        self._log("WARN", self.WARNING, message)
    
    def log_error(self, message: str):
        """Logs a error-level message.

        Args:
            message (str): descriptive message to log
        """
        self._log("ERROR", self.ERROR, message)
    
    def log_critical(self, message: str):
        """Logs a critical-level message.

        Args:
            message (str): descriptive message to log
        """
        self._log("CRITICAL", self.CRITICAL, message)

    def log_high_priority(self, message: str):
        """Always log this, regardless of quiet/dev_mode.

        Args:
            message (str): descriptive message to log
        """
        self._log("HIGH", self.INFO, message)
        
    def redact(self, data: dict, replacement: str ='*** REDACTED ***'):
        """Recusively redact sensitive fields (token, password, authorization, api_key) from data.

        Args:
            data (_type_): JSON to sanitize
            replacement (str, optional): what sensitive data is replaced with. Defaults to '*** REDACTED ***'.

        Returns:
            (dict): sanitized JSON
        """
        keys_to_redact = ['token', 'password', 'authorization', 'api_key']
        
        def _redact(obj):
            if isinstance(obj, dict):
                return {
                    k: (replacement if k.lower() in keys_to_redact else _redact(v))
                    for k, v in obj.items()
                }
            elif isinstance(obj, list):
                return [_redact(item) for item in obj]
            return obj

        import copy

        return _redact(copy.deepcopy(data))
    
    def close(self):
        """Closes the log file."""
        self.fp.close()
