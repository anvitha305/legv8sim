" Vim syntax file
" Language: LEG-V8
" Maintainer: Anvitha (@anvitha305 on GitHub :3)
" Latest Revision: 5 February 2023


if exists('b:current_syntax') | finish| endif

" ignore the case of register names, etc.
set ignorecase


" constants in legv8
syntax match constant "\v<#\d+>"

highlight default link instructions 
highlight default link constant Number

let b:current_syntax= 'legv8'
