'''20240620 initial template to be modified accordingly'''
import os
from misc import extract_date

def generate_slide_frames(title, filenames, comments):
    # Initialize an empty string to accumulate LaTeX code
    latex_content = ''

    # Generate LaTeX code for each filename in the list
    for i, filename in enumerate(filenames):
        if os.path.exists(filename):
            slide_number = os.path.splitext(os.path.basename(filename))[0]
            slide_comment = comments[i] if i < len(comments) else ''
            latex_content += rf'''
    \begin{{frame}}[fragile]{{{title} - Slide {slide_number}}}
        \frametitle{{{title} - Slide {slide_number}}}
        \begin{{columns}}
            \begin{{column}}{{0.6\textwidth}}
                \includegraphics[width=\textwidth]{{{filename}}}
            \end{{column}}
            \begin{{column}}{{0.4\textwidth}}
                \raggedleft
                \small
                {slide_comment}
            \end{{column}}
        \end{{columns}}
    \end{{frame}}
'''

    return latex_content

# Example usage:
# List of filenames and comments for each slide set
dir_list = ['/Users/sterlingvondehn/Documents/nrtbs/BARC_timeserise_fort_nelson_composit','/Users/sterlingvondehn/Documents/nrtbs/L2_fort_nelson','/Users/sterlingvondehn/Documents/nrtbs/BARC_timeserise_fort_nelson_L2']
slide_list = [[] for i in range(len(dir_list))]

for i in range(len(dir_list)):
    files = os.listdir(dir_list[i])
    file_list = []
    for n in range(len(files)):
        if files[n].split('.')[-1] == 'bin':
            file_list.append(f'{dir_list[i]}/{files[n]}')
        else:
            continue;
        
    slide_list[i] = sorted(file_list, key=extract_date)


slide_set1 = slide_list[0]
slide_set2 = slide_list[1]
slide_set3 = slide_list[2]

comments_set1 = [
]
comments_set2 = [
]
comments_set3 = [
]

# LaTeX preamble and end code
latex_preamble = r'''
\documentclass{beamer}
\usepackage{graphicx}
\usepackage{array}
\begin{document}
'''

latex_end = r'''
\end{document}
'''

# Make the presentation

with open('presentation.tex', 'w') as file:
    file.write(latex_preamble +
               generate_slide_frames('Slide Set 1', slide_set1, comments_set1) +
               generate_slide_frames('Slide Set 2', slide_set2, comments_set2) + 
               generate_slide_frames('Slide Set 3', slide_set3, comments_set3) + 
               latex_end) 


