" Move up and down by 5 lines
noremap <S-Down> 5j
noremap <S-Up> 5k
inoremap <S-Down> <C-o>5j
inoremap <S-Up> <C-o>5k

" Copy and paste mappings
xnoremap <Leader>p p  " Paste over visual selection
xnoremap p pgvy       " Paste over visual selection and keep selection
inoremap <C-v> <C-r>+ " Paste from system clipboard in insert mode
vnoremap <C-c> "+y    " Copy to system clipboard in visual mode
" inoremap <C-p> <C-r> " (commented out)

" Window splitting shortcuts
command! -nargs=0 hs sp
command! -nargs=0 sh sp
command! -nargs=0 sv vs

nnoremap <A-C-Left> <C-o>
nnoremap <A-C-Right> <C-i>

" Insert new line in normal mode
nnoremap <CR> o<Esc>

" Move lines up and down
noremap <A-Up> :m .-2<CR>==
noremap <A-Down> :m .+1<CR>==

inoremap <A-Up> <Esc>:m .-2<CR>==gi
inoremap <A-Down> <Esc>:m .+1<CR>==gi

vnoremap <A-Up> :m '<-2<CR>gv=gv
vnoremap <A-Down> :m '>+1<CR>gv=gv

" Ctrl + del in insert mode
inoremap <C-H> <C-o>db
inoremap <C-Del> <C-o>dw

" Enable search highlighting
set hlsearch

" Enable line numbers and relative line numbers
set number
set relativenumber

" Sync clipboard between OS and Vim
set clipboard=unnamedplus

" Enable break indent<
set breakindent

" Save undo history
set undofile

" Case-insensitive searching unless \C or capital letter is used
set ignorecase
set smartcase

" Keep signcolumn on by default
set signcolumn=yes

" Set completion options for a better experience
set completeopt=menuone,noselect

