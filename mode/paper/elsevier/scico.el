;
;   Copyright (C) 2014-2019 Philipp Paulweber
;   All rights reserved.
;
;   Developed by: Philipp Paulweber
;                 <https://github.com/ppaulweber/liborg>
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
;   Additional permission under GNU GPL version 3 section 7
;
;   liborg is distributed under the terms of the GNU General Public License
;   with the following clarification and special exception: Linking liborg
;   statically or dynamically with other modules is making a combined work
;   based on liborg. Thus, the terms and conditions of the GNU General
;   Public License cover the whole combination. As a special exception,
;   the copyright holders of liborg give you permission to link liborg
;   with independent modules to produce an executable, regardless of the
;   license terms of these independent modules, and to copy and distribute
;   the resulting executable under terms of your choice, provided that you
;   also meet, for each linked independent module, the terms and conditions
;   of the license of that module. An independent module is a module which
;   is not derived from or based on liborg. If you modify liborg, you
;   may extend this exception to your version of the library, but you are
;   not obliged to do so. If you do not wish to do so, delete this exception
;   statement from your version.
;

(load-file (concat (file-name-directory load-file-name) "../paper.el"))

(unless (boundp 'org-latex-classes)(setq org-latex-classes nil))
(add-to-list 'org-latex-classes
'("paper-elsevier-scico"
"\\documentclass{elsarticle}
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
