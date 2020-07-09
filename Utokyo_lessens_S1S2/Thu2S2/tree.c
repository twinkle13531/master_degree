public add(tree){
    if (leaf) return;
    list.add(tree);
}

public String tostring

class Starck
def RPN()

/********************************************************************************
 * number.c -- ファイルの数字を調べ、小さい数から順に出力する。
 * ******************************************************************************/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

struct node {
    int     value;            // このノードが保持している値
    struct  node *left_ptr;   // 左枝
    struct  node *right_ptr;  // 右枝
};
// ツリーの頂点 root
static struct node *root = NULL;

/********************************************************************************
 * make_tree   -- ノードを作成し、ツリーに数値を挿入
 *
 * パラメータ
 *      node   -- 現在のノード。ダブルポインタ（ポインタ変数へのポインタ）
 *      value  -- テキストから取り出した、挿入する数値
 ********************************************************************************/
void add(struct node **node, int value)
{

    // ノードが存在しない場合
    if ((*node) == NULL) {

        // 新しい領域を割り当てノードを作成する
        (*node) = malloc(sizeof(struct node));
        if ((*node) == NULL){
            fprintf(stderr, "NULL");
            exit (8);
        }

        // メンバを初期化
        (*node)->left_ptr  = NULL;
        (*node)->right_ptr = NULL;
        (*node)->value     = value;

        // make_tree関数を終了
        return;
    }


    if ((*node)->right_ptr = NULL) {
        add(&(*node)->right_ptr, value);
    }
    // 小さかったら左枝に移動
    else {
        add(&(*node)->left_ptr, value);
    }
}

void remove(struct node **node, int value)
{

}

/********************************************************************************
 * print_value -- 再帰関数。ツリー中の数値を小さい順から画面に出力
 *
 * パラメータ
 *      now    -- 出力するツリーのルート
 ********************************************************************************/
void print(struct node *now)
{
    if (now == NULL)
        return;

    print(now->left_ptr);
    printf("%d\n", now->value);
    print(now->right_ptr);
}

int main()
{
    add(value);
    print(root);
    return (0);
}