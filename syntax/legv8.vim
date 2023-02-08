" Vim syntax file
" Language: LEG-V8
" Maintainer: Anvitha (@anvitha305 on GitHub :3)
" Latest Revision: 5 February 2023

if exists('b:current_syntax') | finish| endif

" ignore the case of register names, etc.
syntax case ignore
" constants in legv8
syntax match constant "\#\d+\"

" registers in legv8
syntax match reg "\v<[Xx][0-9]>"
syntax match reg "\v<[Xx][12][0-9]>"
syntax match reg "\v<[Xx][3][0-1]>"
" alternate register names
syntax match reg "\v<ip[0-1]|sp|fp|lr|xzr>"
syntax match reg "\v<IP[0-1]|SP|FP|LR|XZR>"

" comments are // in this version of legv8.
syntax match comment "\v\/\/.*$"

" branches
syntax match branch "\v.+:$"

" keywords in legv8
syntax match instructions "\vst[xu]r"
syntax match instructions "\va[nd]di"
" begin highlighting the specific things outlined in matching patterns
highlight default link constant Number
highlight default link instructions Keyword
highlight default link reg StorageClass
highlight default link comment Comment
highlight default link branch Function
let b:current_syntax= 'legv8'
