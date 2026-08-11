# Compila slides.tex -> slides.pdf en esta misma carpeta.
# XeLaTeX es necesario para la tipografia Arial de la plantilla UTP.
$pdf_mode = 5;            # 5 = xelatex
$xelatex  = 'xelatex -interaction=nonstopmode -synctex=1 %O %S';
$clean_ext = 'nav snm xdv synctex.gz';
