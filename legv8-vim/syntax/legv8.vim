" Vim syntax file
" Language: LEG-V8
" Maintainer: Anvitha (@anvitha305 on GitHub :3)
" Latest Revision: 5 February 2023

" am allowing case differences for names of instructions, regs etc
set ignorecase

syntax keyword instructions 
	\ add
	\ addi

" constants in legv8
syntax match constant "\v<#\d+>"


highlight default link constant Number

