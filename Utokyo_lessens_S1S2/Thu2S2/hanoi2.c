#include  <stdio.h>

/*--- 円盤をx軸からy軸へ移動 ---*/
void hanoi(int no, int x, int y){
    int  xstk[100], ystk[100], sstk[100];       /* スタック */
    int  ptr = 0;                               /* スタックポインタ */
    int  sw = 0;

    while (1) {
        if (sw == 0 && no > 1) {
            xstk[ptr] = x;              /* xの値をプッシュ */
            ystk[ptr] = y;              /* yの値をプッシュ */
            sstk[ptr] = sw;             /* swの値をプッシュ */
            ptr++;
            no = no - 1;
            y = 6  - x - y;
            continue;
        }
        printf("[%d]を%d軸から%d軸へ移動\n", no, x, y);
        if (sw == 1 && no > 1) {
            xstk[ptr] = x;              /* xの値をプッシュ */
            ystk[ptr] = y;              /* yの値をプッシュ */
            sstk[ptr] = sw;             /* swの値をプッシュ */
            ptr++;
            no = no - 1;
            x = 6  - x - y;
            if (++sw == 2) sw = 0;
            continue;
        }
        do {
            if (ptr-- == 0)             /* スタックが空になったら */
                return; 
            x  = xstk[ptr];             /* 値を保存していたxをポップ */
            y  = ystk[ptr];             /* 値を保存していたyをポップ */
            sw = sstk[ptr] + 1;         /* 値を保存していたswをポップ */
            no++;
        } while (sw == 2);
    }
}

int main(void){
    int  n=4;     /* 円盤の枚数 */
    hanoi(n, 1, 3);

    return 0;
}