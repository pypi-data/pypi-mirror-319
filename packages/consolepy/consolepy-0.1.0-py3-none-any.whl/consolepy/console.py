
class Console():

    
    @staticmethod
    def b_title(text,char='󱋰',charv=''):

        # Crear un titulo con bordes

        line = char * (len(text) + 4)
        return f"{line}\n{charv} {text} {charv}\n{line}"
    @staticmethod
    def box(text,char='󱋰',charv=''):
        # Crea una caja con bordes
        box = char * (len(text) + 4)
        char_finaly = charv + " " * (len(text)+2) + charv
        return f"{box}\n{char_finaly}\n{char_finaly}\n{charv} {text} {charv}\n{char_finaly}\n{char_finaly}\n{box}"




