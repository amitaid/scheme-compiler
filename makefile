CC		:=	gcc
CC_FLAGS	:=	-w

ARCH := arch

all: $(src)
    $(CC) $(src) -o $(dest) -L$(ARCH)
