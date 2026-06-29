#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

int check_flag(char *flag);

int main(int argc, char* argv[]) {
        if (argc < 2) {
                printf("usage: %s <flag>\n", argv[0]);
                exit(1);
        }

        if (check_flag(argv[1])) {
                printf("ok\n");
        } else {
                printf("no\n");
        }
}

#define TABL_SIZE 0x100

void *tabl[TABL_SIZE];
int check_flag(char *flag) {
        uint32_t hash = 0xdeadbeef;
        uint32_t target_hash;

        if (*(flag++) != 'f') return 0;
        if (*(flag++) != 'l') return 0;
        if (*(flag++) != 'a') return 0;
        if (*(flag++) != 'g') return 0;

#define NEXT goto *tabl[*(flag++)]
#define RESET_JUMPTABLE { \
        for (int x = 0; x < TABL_SIZE; x++) { \
                tabl[x] = &&fail; \
        } \
}

	target_hash = 0xe5c6650d;
	goto block_8;
block_0:
	RESET_JUMPTABLE;
	hash ^= 0x2412579d;
	tabl['i'] = &&block_10;
	NEXT;
block_1:
	RESET_JUMPTABLE;
	hash ^= 0x21681081;
	tabl['4'] = &&block_32;
	tabl['H'] = &&block_4;
	NEXT;
block_2:
	RESET_JUMPTABLE;
	hash ^= 0x5582a3bd;
	tabl['0'] = &&block_19;
	tabl['T'] = &&block_26;
	tabl['O'] = &&block_32;
	tabl['v'] = &&block_9;
	tabl['k'] = &&block_15;
	tabl['1'] = &&block_22;
	NEXT;
block_3:
	RESET_JUMPTABLE;
	hash ^= 0xea5f24b6;
	tabl['y'] = &&block_34;
	tabl['c'] = &&block_34;
	tabl['x'] = &&block_24;
	tabl['K'] = &&block_27;
	NEXT;
block_4:
	RESET_JUMPTABLE;
	hash ^= 0x52daad3;
	tabl['1'] = &&block_10;
	NEXT;
block_5:
	RESET_JUMPTABLE;
	hash ^= 0xe2a01335;
	tabl['_'] = &&block_31;
	tabl['f'] = &&block_34;
	tabl['L'] = &&block_29;
	tabl['u'] = &&block_10;
	NEXT;
block_6:
	RESET_JUMPTABLE;
	hash ^= 0x7579501a;
	tabl['Z'] = &&block_11;
	tabl['m'] = &&block_15;
	tabl['c'] = &&block_4;
	NEXT;
block_7:
	RESET_JUMPTABLE;
	hash ^= 0x552ae5ca;
	tabl['_'] = &&block_14;
	tabl['1'] = &&block_5;
	NEXT;
block_8:
	RESET_JUMPTABLE;
	hash ^= 0x7b38785b;
	tabl['{'] = &&block_18;
	tabl['I'] = &&block_14;
	tabl['c'] = &&block_3;
	tabl['0'] = &&block_24;
	NEXT;
block_9:
	RESET_JUMPTABLE;
	hash ^= 0x775e0ec3;
	tabl['S'] = &&block_12;
	tabl['N'] = &&block_15;
	NEXT;
block_10:
	RESET_JUMPTABLE;
	hash ^= 0x5a4f4145;
	NEXT;
block_11:
	RESET_JUMPTABLE;
	hash ^= 0xc734bb05;
	tabl['E'] = &&block_34;
	NEXT;
block_12:
	RESET_JUMPTABLE;
	hash ^= 0xdfde2281;
	tabl['y'] = &&block_22;
	NEXT;
block_13:
	RESET_JUMPTABLE;
	hash ^= 0xf8f8f071;
	tabl['3'] = &&block_29;
	tabl['N'] = &&block_26;
	tabl['M'] = &&block_12;
	tabl['R'] = &&block_29;
	NEXT;
block_14:
	RESET_JUMPTABLE;
	hash ^= 0x91fcfe88;
	tabl['1'] = &&block_33;
	tabl['x'] = &&block_10;
	tabl['n'] = &&block_3;
	tabl['K'] = &&block_23;
	NEXT;
block_15:
	RESET_JUMPTABLE;
	hash ^= 0x52ebdac5;
	NEXT;
block_16:
	RESET_JUMPTABLE;
	hash ^= 0xc5c14262;
	tabl['4'] = &&block_20;
	tabl['b'] = &&block_5;
	tabl['P'] = &&block_31;
	NEXT;
block_17:
	RESET_JUMPTABLE;
	hash ^= 0xdca5b353;
	tabl['3'] = &&block_28;
	tabl['l'] = &&block_6;
	NEXT;
block_18:
	RESET_JUMPTABLE;
	hash ^= 0xf11ddff7;
	tabl['f'] = &&block_2;
	tabl['i'] = &&block_32;
	NEXT;
block_19:
	RESET_JUMPTABLE;
	hash ^= 0x3d2bf042;
	tabl['r'] = &&block_21;
	tabl['w'] = &&block_0;
	tabl['L'] = &&block_23;
	tabl['_'] = &&block_32;
	tabl['A'] = &&block_23;
	NEXT;
block_20:
	RESET_JUMPTABLE;
	hash ^= 0xd334886f;
	tabl['n'] = &&block_7;
	tabl['x'] = &&block_32;
	tabl['7'] = &&block_10;
	tabl['U'] = &&block_6;
	NEXT;
block_21:
	RESET_JUMPTABLE;
	hash ^= 0xef7e85ec;
	tabl['t'] = &&block_30;
	tabl['n'] = &&block_31;
	NEXT;
block_22:
	RESET_JUMPTABLE;
	hash ^= 0x866d7002;
	tabl['}'] = &&check_hash;
	tabl['T'] = &&block_15;
	NEXT;
block_23:
	RESET_JUMPTABLE;
	hash ^= 0x4cea2df0;
	tabl['_'] = &&block_1;
	NEXT;
block_24:
	RESET_JUMPTABLE;
	hash ^= 0xb2ddc481;
	tabl['I'] = &&block_0;
	tabl['1'] = &&block_27;
	tabl['v'] = &&block_9;
	NEXT;
block_25:
	RESET_JUMPTABLE;
	hash ^= 0xccf719ab;
	tabl['t'] = &&block_17;
	tabl['j'] = &&block_22;
	NEXT;
block_26:
	RESET_JUMPTABLE;
	hash ^= 0x786e30ef;
	tabl['4'] = &&block_12;
	tabl['u'] = &&block_22;
	tabl['S'] = &&block_22;
	NEXT;
block_27:
	RESET_JUMPTABLE;
	hash ^= 0x19faa06e;
	tabl['h'] = &&block_6;
	NEXT;
block_28:
	RESET_JUMPTABLE;
	hash ^= 0x72d6bc20;
	tabl['r'] = &&block_23;
	tabl['H'] = &&block_24;
	NEXT;
block_29:
	RESET_JUMPTABLE;
	hash ^= 0xc12ea9b8;
	tabl['t'] = &&block_25;
	NEXT;
block_30:
	RESET_JUMPTABLE;
	hash ^= 0x6238d0a0;
	tabl['r'] = &&block_16;
	tabl['U'] = &&block_28;
	NEXT;
block_31:
	RESET_JUMPTABLE;
	hash ^= 0xf8e45086;
	tabl['b'] = &&block_13;
	tabl['g'] = &&block_9;
	NEXT;
block_32:
	RESET_JUMPTABLE;
	hash ^= 0x10fc9eee;
	tabl['n'] = &&block_3;
	tabl['I'] = &&block_34;
	tabl['k'] = &&block_24;
	NEXT;
block_33:
	RESET_JUMPTABLE;
	hash ^= 0xbda17da2;
	tabl['s'] = &&block_5;
	tabl['D'] = &&block_32;
	tabl['p'] = &&block_3;
	tabl['M'] = &&block_25;
	NEXT;
block_34:
	RESET_JUMPTABLE;
	hash ^= 0xccc93ff7;
	tabl['w'] = &&block_26;
	tabl['a'] = &&block_10;
	tabl['k'] = &&block_0;
	NEXT;


check_hash:
        return (target_hash == hash);

fail:
        return 0;
}
