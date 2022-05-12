__version__ = "0.0.1"
import siibra

assert siibra.__version__ == "0.3a17"

class ToolboxTemplate:
    def analysis(self, str_input: str, float_input: float, int_input: int) -> int:
        import time
        time.sleep(5)
        if round(int_input) % 2 == 0:
            raise Exception(f"the int_input needs to be an odd value")
        return len(siibra.atlases) + round(int_input)
