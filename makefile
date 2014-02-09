SUFFIXES:
SUFFIXES: .asm

%: %.asm
	gcc -x c -o $@ $< -Iarch
