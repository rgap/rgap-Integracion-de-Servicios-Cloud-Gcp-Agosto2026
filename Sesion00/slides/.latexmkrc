# Compila slides.tex -> build/slides.pdf.
# XeLaTeX es necesario para la tipografia Arial de la plantilla UTP.
$pdf_mode = 5;            # 5 = xelatex
$xelatex  = 'xelatex -interaction=nonstopmode -synctex=1 %O %S';

# Todo lo generado (PDF incluido) va a build/.
$out_dir  = 'build';

$clean_ext = 'nav snm xdv synctex.gz';
