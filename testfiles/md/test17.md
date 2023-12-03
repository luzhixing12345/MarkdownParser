
不过由于 p->trapframe 又是一个结构体, 这里只能看到地址, 所以输入 `p p->trapframe->a7` 即可看到结果为 7. 除此之外由于下面也使用了 `num = p->trapframe->a7;` 来进行赋值, 所以也可以再往下 n 一步然后查看 num, 如下图所示的两种方式

|typedef|type|32-bit size (bytes)|64-bit size (bytes)|
|:--:|:--:|:--:|:--:|
|ElfN_Addr|Unsigned program address, uintN_t|4|8|
|ElfN_Off|Unsigned file offset, uintN_t|4|8|
|ElfN_Section|Unsigned section index, uint16\_t|2|2|
|ElfN_Versym|Unsigned version symbol information, uint16\_t|2|2|
|Elf\_Byte|unsigned char|1|1|
|ElfN\_Half|uint16\_t|2|2|
|ElfN\_Sword|int32\_t|4|4|
|ElfN\_Word|uint32\_t|4|4|
|ElfN\_Sxword|int64\_t|8|8|
|ElfN\_Xword|uint64\_t\-|8|8|

ElfN\_Xword|uint64\_t\-

