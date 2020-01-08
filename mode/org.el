;
;   Copyright (C) 2014-2020 Philipp Paulweber
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


;; enable languages for in-buffer code evaluation
(org-babel-do-load-languages
 'org-babel-load-languages
 '((latex . t)
   (python . t)
   (R . t)
   )
 )

(setq org-latex-with-hyperref nil)
(setq org-latex-listings 'listings)

(unless (boundp 'org-latex-prefer-user-labels)
  (setq org-latex-prefer-user-labels t)
  )

;; (org-link-set-parameters
;;  "red"
;;  :follow (lambda (path) (message "You clicked me."))
;;  :export (lambda (path desc backend)
;;            (cond
;;             ((eq 'html backend)
;;              (format "<font color=\"red\">%s</font>"
;;                      (or desc path)))))
;;  :face '(:foreground "red")
;;  :help-echo "Click me for a message.")

;; (if (fboundp 'org-link-set-parameters)
;; )


(org-add-link-type "%" nil 
(lambda (path desc format)
    (let ((alist (split-string path ":"))
          )
      (if (eq format 'latex)
          (if (eq (length alist) 1)
              (format "\\cite{%s}" (nth 0 alist) desc)
            (if (eq (length alist) 2)
                (format "\\cite[p.~%s]{%s}" (nth 1 alist) (nth 0 alist) desc)                 
              (if (eq (length alist) 3)
                  (format "\\cite[pp.~%s--%s]{%s}" (nth 1 alist) (nth 2 alist) (nth 0 alist) desc)
                (error "unsupported page range in 'cite' markup!")
                )
              )
            )
        )     
      )
    )
  )

(org-add-link-type "r" nil
  (lambda (path desc format)
    (let ((alist (split-string path ":"))
          )
      (if (eq format 'latex)
          (if (eq (length alist) 1)
              (format "\\ref{%s}" (nth 0 alist) desc)
            (if (eq (length alist) 2)
                (format "%s\\ref{%s}" (nth 0 alist) (nth 1 alist) desc)
	      (error "unsupported 'ref' markup!")
	      )
	    )
        )
      )
    )
  )

(setq org-paper-acro (make-hash-table :test 'equal))

(org-add-link-type "'" nil
  (lambda (path desc format)
    (let ((alist (split-string path ":")))
    (let ((key (if (>= (length alist) 1) (nth 0 alist) "")))
    (let ((value (gethash key org-paper-acro)))
      (if value
          (puthash key (+ value 1) org-paper-acro)          
        (puthash key 0 org-paper-acro)          
        )
      (if (eq format 'latex)
          (let ((epilog (format "\\%s{%s}{"
                          (if value "hyperlink" "hypertarget")
                          key)
                        )
                (prolog "}")
                )
            (if (eq (length alist) 1)
                (format "%s\\ac{%s}%s" epilog key prolog desc)
              (if (eq (length alist) 2)
                  (format "%s\\ac{%s}%s%s" epilog key (nth 1 alist) prolog desc)                 
                (if (eq (length alist) 3)
                    (format "%s\\ac%s{%s}%s%s" epilog (nth 2 alist) key (nth 1 alist) prolog desc)
                  (error "unsupported acronym range in 'cite' markup!")
                  )
                )
              )
            )
        )
      )))
    )
  )

;; (org-add-link-type "???" nil
;;   (lambda (path desc format)
;;     (let ((alist (split-string path "::"))
;;           )
;;       (if (eq format 'latex)
;;           (if (eq (length alist) 1)
;;               (format "\\todo{%s}" (nth 0 alist) desc)
;;             (if (eq (length alist) 2)
;; 		(let ((namelist (split-string (nth 0 alist) ","))
;; 		      )
;; 		  (format "\\todo[color=notecolor_%s]{\\textbf{%s:} %s}" (nth 0 alist) (nth 0 namelist) (nth 1 alist) desc)
;; 		  )
;; 	      (error "unsupported 'todo' markup!")
;; 	      )
;; 	    )
;; 	)
;;       )
;;     )
;;   )

(setq org-confirm-babel-evaluate nil)


(setq org-latex-to-pdf-process '("make"))


(setq org-ref-insert-cite-key "C-c )")

;; (setq reftex-cite-format '("$:%l"))

(eval-after-load 'reftex-vars
  '(progn
     (setq reftex-cite-format
           '((?\C-m . "$:%l")
             )
           )))

;; (defun org-ref-cite-link-format (keyword desc format)
;;   (cond
;;    ((eq format 'html) (format "(<cite>%s</cite>)" path))
;;    ((eq format 'latex)
;;     (concat "$:" (when desc (format "[%s]" desc)) ""
;;             (mapconcat (lambda (key) key) (org-ref-split-and-strip-string keyword) ",")
;;             ""))))

;; (org-add-link-type
;;  "cite"
;;  'org-ref-cite-onclick-minibuffer-menu ;; clicking function
;;  'org-ref-cite-link-format) ;; formatting function



(require 'cl)
(defun delete-org-comments (backend)
  (loop for comment in (reverse (org-element-map (org-element-parse-buffer)
				    'comment 'identity))
	do
	(setf (buffer-substring (org-element-property :begin comment)
				(org-element-property :end comment))
              "")))
(add-hook 'org-export-before-parsing-hook 'delete-org-comments)



;; (defun org-mode-reftex-setup ()
;;   (load-library "reftex")
;;   (and (buffer-file-name)
;;        (file-exists-p (buffer-file-name))
;;        (reftex-parse-all))
;;   (define-key org-mode-map (kbd "C-c )") 'reftex-citation)
;;   )
;; (add-hook 'org-mode-hook 'org-mode-reftex-setup)

;; (defun org-mode-reftex-setup ()
;;   (load-library "reftex")
;;   (and (buffer-file-name) (file-exists-p (buffer-file-name))
;;        (progn
;;          disk
;;          (global-auto-revert-mode t)
;;          (reftex-parse-all)
;;          (reftex-set-cite-format "$:%l")
;;          ))
;;   (define-key org-mode-map (kbd "C-c )") 'reftex-citation)
;;   (define-key org-mode-map (kbd "C-c (") 'org-mode-reftex-search)
;;   )


;(add-to-list 'org-export-latex-emphasis-alist '( ("?" "\\cite{%s}" nil) ) )

;; (custom-set-variables
;;  '(org-emphasis-alist
;;    (quote
;;     (;("*" org-level-3 "<b>" "</b>")
;;      ;("/" org-level-3 "<i>" "</i>")
;;      ;("+" org-code "<b>" "</b>" verbatim)
;;      ;("#" org-level-4 org-code "<b>" "</b>")
;;      ;("=" org-code "<code>" "</code>" verbatim)
;;      ;("|" org-level-3 bold "<b>" "</b>")
;;      ("?" org-level-4 org-code "<b>" "</b>")
;;      ;("^" org-level-3 bold "<b>" "</b>")
;;      )
;;     )
;;    )
;;  '(org-export-latex-emphasis-alist
;;    (quote
;;     (;("*" "\\textbf{%s}" nil)
;; ;     ("/" "\\textit{%s}" nil)
;; ;     ("+" "\\label{%s}" nil)
;; ;     ("#" "\\ref{%s}" nil)
;; ;     ("=" "\\texttt{%s}" nil)
;; ;     ("|" "\\ac{%s}" nil)
;;      ("?" "\\cite{%s}" nil)
;; ;     ("^" "\\ppquote{%s}" nil)
;;      )
;;     )
;;    )
;;  '(reftex-cite-format "?%l??")
;;  )


;; ignore_heading tag in Org mode, based on the manual and func docs
(defun ignored-headlines-removal (backend)
    "Remove all headlines with tag ignore_heading in the current buffer.
     BACKEND is the export back-end being used, as a symbol."
    (org-map-entries
     (lambda () (delete-region (point) (progn (forward-line) (point))))
     "ignore_export"))

(add-hook 'org-export-before-parsing-hook 'ignored-headlines-removal)



;; (defun org-paper-tag-abstract (backend)
;;     "Remove all headlines with tag ignore_heading in the current buffer.
;;      BACKEND is the export back-end being used, as a symbol."
;;     ;(org-map-entries
;;     ; (lambda () (delete-region (point) (progn (forward-line) (point))))
;;     ; "no_export")

;;     (print
;;      (org-map-entries
;;       (lambda ()
;;         (print (org-get-heading t t))
;;         (edebug)
;;         )
;;       "abstract"
;;       )
;;      )
;; )

;; (add-hook 'org-export-before-parsing-hook 'org-paper-tag-abstract)


;; (defun sa-ignore-headline (contents backend info)
;;   "Ignore headlines with tag `'."
;;   (when (and (org-export-derived-backend-p backend 'latex 'html 'ascii)
;;              (string-match "\\`.*ignore.*\n"
;;                            (downcase contents)))
;;     (replace-match "" nil nil contents)))

;; (add-to-list 'org-export-filter-headline-functions 'sa-ignore-headline)
