from fpdf import FPDF
import re

class FuncionesParaPDFS:

    @staticmethod
    def calcular_altura_lista_pdf(pdf, texto, ancho, alto_linea):
        # Obtiene las líneas que ocupará el texto sin dibujar nada
        lineas = pdf.multi_cell(ancho, alto_linea, texto, border=0, align="L", split_only=True)
        return max(alto_linea * len(lineas), alto_linea)  # al menos 1 línea
    
    @staticmethod
    def dibujar_fila(pdf, cols, anchos, alto_linea):
        """
        cols: lista de textos [propietario, mensaje, fecha, estado]
        anchos: lista de anchos por columna
        """
        x_ini = pdf.get_x()
        y_ini = pdf.get_y()

        # Calcular altura de cada celda
        alturas = [FuncionesParaPDFS.calcular_altura_lista_pdf(pdf, texto, anchos[i], alto_linea) for i, texto in enumerate(cols)]
        h_fila = max(alturas)

        # Salto de página si no entra la fila completa
        if y_ini + h_fila > pdf.h - pdf.b_margin:
            pdf.add_page()
            y_ini = pdf.get_y()

        # Dibujar cada celda con altura uniforme
        x = x_ini
        for i, texto in enumerate(cols):
            w = anchos[i]
            pdf.rect(x, y_ini, w, h_fila)  # borde
            pdf.set_xy(x, y_ini)
            align = "L" if i == 1 else "C"  # mensaje alineado a la izquierda
            pdf.multi_cell(w, alto_linea, texto, border=0, align=align)
            x += w
            pdf.set_xy(x, y_ini)

        # Avanzar a la siguiente fila
        pdf.set_xy(x_ini, y_ini + h_fila)
        # Avanzar a la siguiente fila
        pdf.set_xy(x_ini, y_ini + h_fila)