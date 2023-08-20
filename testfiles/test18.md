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
