'''20240620 initial template to be modified accordingly'''
import os
from misc import extract_date

def generate_slide_frames(title, filenames1, filenames2):
    # Initialize an empty string to accumulate LaTeX code
    latex_content = ''

    # Generate LaTeX code for each filename in the list
    for filename in filenames1:
        date = filename.split('/')[-1].split('_')[0]
        for file in filenames2:
            if file.split('/')[-1].split('_')[0] == date:
                slide_number = os.path.splitext(os.path.basename(filename))[0]
                latex_content += rf'''
    \begin{{frame}}[fragile]{{{title} - Date {date}}}
        \frametitle{{{title} - Date {date}}}
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
dir_list = ['/Users/sterlingvondehn/Documents/nrtbs/BARC_timeserise_fort_nelson_composite','/Users/sterlingvondehn/Documents/nrtbs/MRAP_images','/Users/sterlingvondehn/Documents/nrtbs/BARC_timeserise_fort_nelson_L2','/Users/sterlingvondehn/Documents/nrtbs/L2_images','/Users/sterlingvondehn/Documents/nrtbs/clipped_BARC', '/Users/sterlingvondehn/Documents/nrtbs/non_clipped_BARC']
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
    file.write((latex_preamble + '\section{Notebook}' +
                generate_slide_frames('BARC classes using Sashas notebook', slide_set5, slide_set6 ) + '\section{L2 Data}' +
                generate_slide_frames('BARC and SWIR time series using L2', slide_set3, slide_set4 ) + '\section{MRAP Data}' +
                generate_slide_frames('BARC and SWIR time series using MRAP', slide_set1, slide_set2) + latex_end
                ).replace('_','\_')) 
    
os.system('pdflatex presentation.tex; rm *.log *.nav *.aux *.snm *.vrb; open presentation.pdf')


