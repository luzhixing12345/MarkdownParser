```bash
(base) kamilu@LZX:~/libc$ ./main --help
Usage: ls [OPTION]... [dest] [src] [other-number]...

A brief description of what the program does and how it works.

  -h   --help      show help information
  -v   --version   show version
  -i   --input     input file
  -s   --string


Additional description of the program after the description of the arguments.
```

**xargparse 使用了动态内存分配, 所以最后请注意使用 `XBOX_free_argparse` 释放内存**

参数fd是要关闭的文件描述符.当一个进程终止时,内核对该进程所有尚未关闭的文件描述符调用close关闭,所以即使用户程序不调用close,在终止时内核也会自动关闭它打开的所有文件, 但是程序中应该手动关闭. 由open返回的文件描述符一定是该进程尚未使用的**最小**描述符.
