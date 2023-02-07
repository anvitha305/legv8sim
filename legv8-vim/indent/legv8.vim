" indent/legv8.vim
setlocal indentexpr=LIndent()

function! LIndent()
	let line = getline(v:lnum)
	let previousNum = prevnonblank(v:lnum)
	let prev = getline(previousNum)
	if previous =~ "\:$" 
		return indent(previousNum) + &tabstop
	endif
endfunction
