" indent/legv8.vim
setlocal indentexpr=LIndent()

function! LIndent()
	let line = getline(v:lnum)
	let previousNum = prevnonblank(v:lnum)
	let prev = getline(previousNum)
	if prev =~ "\:$" 
		return indent(previousNum) + &tabstop
	endif
endfunction
