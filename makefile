.SUFFIXES:
.SUFFIXES: .asm
CC              :=      gcc
CC_FLAGS        :=      -w -c
ARCH := arch
TARGET := $(wildcard *.asm)

all: $(TARGET)

%: %.asm
	$(CC) $(CC_FLAGS) -o $* $@ -I$(ARCH)
