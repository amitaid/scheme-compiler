CC              :=      gcc
CC_FLAGS        :=      -w

ARCH := arch

all: $(src)
        $(CC) $(CC_FLAGS) $(src) -o $(dest) -I$(ARCH)
