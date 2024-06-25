'''20240620 initial template to be modified accordingly'''
import os
from misc import extract_date

def generate_slide_frames(title, filenames1, filenames2):
    # Initialize an empty string to accumulate LaTeX code
    latex_content = ''

    # Generate LaTeX code for each filename in the list
    for filename in filenames1:
        date = extract_date(filename.split('/')[-1])
        for file in filenames2:
            if extract_date(file.split('/')[-1]) == date:
                slide_number = os.path.splitext(os.path.basename(filename))[0]
                latex_content += rf'''
    \begin{{frame}}[fragile]{{{title}}}
        \frametitle{{{title}}}
        \framesubtitle{{End date: {date}}}
        \begin{{columns}}
            \begin{{column}}{{0.5\textwidth}}
                \centering
                \includegraphics[width=1.1\linewidth,height=1.3\textheight,keepaspectratio]{{{file}}}
            \end{{column}}
            \begin{{column}}{{0.5\textwidth}}
                \centering
                \includegraphics[width=1.1\linewidth,height=1.3\textheight,keepaspectratio]{{{filename}}}
            \end{{column}}
        \end{{columns}}
    \end{{frame}}
    '''

    return latex_content

# Example usage:
# List of filenames and comments for each slide set
dir_list = ['BARC_timeseries_fort_nelson_cut_composite','MRAP_images','BARC_timeseries_fort_nelson_L2','L2_images','clipped_BARC', 'non_clipped_BARC']
slide_list = [[] for i in range(len(dir_list))]

for i in range(len(dir_list)):
    files = os.listdir(dir_list[i])
    file_list = []
    for n in range(len(files)):
        if files[n].split('.')[-1] == 'png':
            file_list.append([files[n].split('_')[0], f'{dir_list[i]}/{files[n]}'])
        else:
            continue;
    file_list.sort()
    
    slide_list[i] = [f[1] for f in file_list]


slide_set1 = slide_list[0]
slide_set2 = slide_list[1]
slide_set3 = slide_list[2]
slide_set4 = slide_list[3]
slide_set5 = slide_list[4]
slide_set6 = slide_list[5]
# LaTeX preamble and end code
latex_preamble = r'''
\documentclass{beamer}
\usepackage{graphicx}
\usepackage{array}
\title{BARC}
\author{Sterling von Dehn and Ash Richardson}
\institute{B.C. Wildfire Service}
\date{\today}

\begin{document}

\begin{frame}
	\titlepage
\end{frame}


\begin{frame}
	\frametitle{Table of Contents}
	\tableofcontents % Automatically generates the table of contents
\end{frame}
'''

latex_end = r'''
\end{document}
'''

# Make the presentation

with open('presentation.tex', 'w') as file:
    file.write((latex_preamble + r'''\section{Notebook}''' +
                generate_slide_frames('BARC classes/ Google Earth Engine/ Full scene + clipped', slide_set5, slide_set6 ) + r'''\section{Comparisons}''' +
                generate_slide_frames('Local implementation + Google Earth Engine',['non_clipped_BARC/2021-09-07_non_clipped_sparks_lake_BARC.png','non_clipped_BARC/2024-06-19_non_clipped_fort_nelson_BARC.png'],['2021-09-07__BARC_classification.png','2024-06-19_MRAP_BARC_classification.png']) + 
                r'''\section{MRAP Data}''' +
                generate_slide_frames('SWIR + BARC/ time series/ MRAP', slide_set1, slide_set2 ) + r'''\section{L2 Data}''' +
                generate_slide_frames('SWIR + BARC/ time series/ L2', slide_set3, slide_set4 )
                + latex_end
                ).replace('_','\\_')) 
    
os.system('pdflatex presentation.tex; rm *.log *.nav *.aux *.snm *.vrb; open presentation.pdf')


#generate_slide_frames('Comparision of notebook vs script', ['20210907__BARC_classification.png'], ['non_clipped_BARC/20210907_non_clipped_sparks_lake_BARC.png'] ) 