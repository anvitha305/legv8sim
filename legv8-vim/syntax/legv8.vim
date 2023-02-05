" Vim syntax file
" Language: LEG-V8
" Maintainer: Anvitha (@anvitha305 on GitHub :3)
" Latest Revision: 5 February 2023

" am allowing case differences for names of instructions, regs etc
set ignorecase

" constants in legv8
syntax match constant "\v<#\d+>"

" registers in legv8 [x0-x31]
syntax match reg "\v<x[0-9]|[12][0-9]|[3][0-1]>"
" alternate register names
syntax match reg "\v<ip[0-1]|sp|fp|lr|xzr>"


