;;; legv8.el --- major mode for editing LEGV8 assembly. -*- coding: utf-8; lexical-binding: t; -*-

;; Copyright © 2023 Anvitha Ramachandran

;; Author: Anvitha Ramachandran (aramachandra [at] umass [dot] edu)
;; Version: 1.2
;; Created: 18 Feb 2023
;; Keywords: legv8
;; Homepage: https://github.com/anvitha305/legv8sim

;; This file is not part of GNU Emacs.

;;; License:
;; You can redistribute and/or modify the code under the terms of the Apache 2.0 license.

;;; Commentary:

;; Tool for code coloring and editing LEGV8 assembly.

;;; Code:

;; font-lock list:

(setq legv8-font-lock-keywords
      (let* (
            ;; define several category of keywords
            (x-keywords '("add" "addi" "adds" "addis" "orr" "subs" "b" "andi" "ands"))
            ;; generate regex string for each category of keywords
            (x-keywords-regexp (regexp-opt x-keywords 'words))

        `(
          (,x-keywords-regexp . 'font-lock-keyword-face)
          ;; note: order above matters, because once colored, that part won't change.
          ;; in general, put longer words first
          )))

;;;###autoload
(define-derived-mode legv8-mode c-mode "lsl mode"
  "Major mode for editing LEGV8 Assembly"
  ;; code for syntax highlighting
  (setq font-lock-defaults '((legv8-font-lock-keywords))))

;; add the mode to the `features' list
(provide 'legv8-mode)
;;; legv8-mode.el ends here
