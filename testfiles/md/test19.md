
1. 标准输出是否是终端

   如果输出并不是终端则不使用控制序列, 比如 `ls > a.txt`, 此时如果也将虚拟控制序列输出到文件中则会出现乱码, 因为该序列是由 terminal 来负责解析和显示的, 不应该直接输出给文本文件

2. 格式化输出长度

   由于 ls 多行需要根据当前列的最大字符长度进行左对齐, 所以考虑如下代码, printf 格式化中都使用了 "%-10s" 来控制至少 10 字符的左对齐, 但由于虚拟控制字符本身占据长度, 因此第二个 printf 的输出对齐并没有按照实际显示的文字 123 进行对齐, 需要进行补齐考虑

   ```c
   #include <stdio.h>

   int main(int argc, const char **argv) {
       printf("%-10sxxx\n", "123");
       printf("%-10sxxx\n", "\033[1;91m123\033[1;0m");
       return 0;
   }
   ```