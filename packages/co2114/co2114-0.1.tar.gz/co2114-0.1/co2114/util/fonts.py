from sys import platform


def _get_text_font_unsafe():
    """ Returns None which should cause Pygame to fall to default """
    return None

def _get_symbolic_font_unsafe():
    """ Returns expected system font """
    match platform:
        case "linux":
            return "Ubuntu Mono" # TODO test
        case "darwin":
            return "Apple Symbols" # TODO test
        case "win32":
            return "segoe-ui-symbol" 
        case _:
            return None
