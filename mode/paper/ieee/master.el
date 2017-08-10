;
;   Copyright (c) 2016-2017 Philipp Paulweber
;   All rights reserved.
;
;   Developed by: Philipp Paulweber
;                 https://github.com/ppaulweber/liborg
;
;   This file is part of liborg.
;
;   liborg is free software: you can redistribute it and/or modify
;   it under the terms of the GNU General Public License as published by
;   the Free Software Foundation, either version 3 of the License, or
;   (at your option) any later version.
;
;   liborg is distributed in the hope that it will be useful,
;   but WITHOUT ANY WARRANTY; without even the implied warranty of
;   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
;   GNU General Public License for more details.
;
;   You should have received a copy of the GNU General Public License
;   along with liborg. If not, see <http://www.gnu.org/licenses/>.
;

(load-file (concat (file-name-directory load-file-name) "../paper.el"))

(unless (boundp 'org-latex-classes)(setq org-latex-classes nil))
(add-to-list 'org-latex-classes
'("paper-ieee-master"
"\\documentclass{IEEEtran}
[NO-DEFAULT-PACKAGES]
[NO-PACKAGES]
[EXTRA]"
("\\section{%s}"       . "\\section*{%s}")
("\\subsection{%s}"    . "\\subsection*{%s}")
("\\subsubsection{%s}" . "\\subsubsection*{%s}")
("\\paragraph{%s}"     . "\\paragraph*{%s}")
("\\subparagraph{%s}"  . "\\subparagraph*{%s}")
)
)
