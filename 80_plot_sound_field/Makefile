
OBJ=fill_black.o

# 作成対象をすべて作る．もしこの一文がないと，
# a.out だけを見て，b.outはいらないから，
# 無視されて終了する．
all: a.out

a.out: fill_black.o
	cc $< -o $@ -lm

.SUFIXES:
.SUFIXES: .c .o
.c.o:
	cc -c $<

clean:
	${RM} *.out *.o
