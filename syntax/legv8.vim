" Vim syntax file
" Language: LEG-V8
" Maintainer: Anvitha (@anvitha305 on GitHub :3)
" Latest Revision: 5 February 2023

if exists('b:current_syntax') | finish| endif

" ignore the case of register names, etc.
syntax case ignore
" constants in legv8
syntax match constant "\v#\d+"

" comments are // in this version of legv8.
syntax match comment "\v\/\/.*$"

" keywords in legv8
syntax match instructions "\vstxr|stur[sdbhw]|ls[lr]|ldur[sdbh]|stur|ldur|ldursw"
syntax match instructions "\vldxr"
syntax match instructions "\va[nd]d%[i]%[s]|lda"
syntax match instructions "\vsub%[i]%[s]"
syntax match instructions "\vmovz|mov%[k]"
syntax match instructions "\vcb%[n]z|eor%[i]|orr%[i]"
syntax match instructions "\vb[lr]|b\.l[etso]|b\.g[et]|b\.h[is]|b\.[vc][cs]"
syntax match instructions "\vb\.eq|b\.ne|b\.hs|b\.mi|b\.pl|b\.al|b "
syntax match instructions "\vmul|[us]mulh|%[su]div|cmp%[i]"
syntax match instructions "\vfadd[sd]|fsub[sd]|fmul[sd]|fdiv[sd]|fcmp[sd]"

"branch labelling legv8
syntax match branch "\v\h\w+:$"
syntax match branch "\v\h\w+$"

" symbols for code segmenting
syntax match symbol "\v\.type"
syntax match symbol "\v\.glob%[a]l"
syntax match symbol "\v\.data"
syntax match symbol "\v\.word"

" registers in legv8
syntax match reg "\v[Xx][0-9i]"
syntax match reg "\v[Xx][12][0-9]"
syntax match reg "\v[Xx][3][0-1]"
" alternate register names
syntax match reg "\vip[0-1]|sp|fp|lr|xzr"

" begin highlighting the specific things outlined in matching patterns
highlight default link constant Number
highlight default link instructions Keyword
highlight default link reg StorageClass
highlight default link comment Comment
highlight default link branch Function
highlight default link symbol Keyword
let b:current_syntax= 'legv8'

