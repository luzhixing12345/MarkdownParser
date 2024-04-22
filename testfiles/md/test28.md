- [深入理解Linux进程调度](https://mp.weixin.qq.com/s?__biz=Mzg2OTc0ODAzMw==&mid=2247506713&idx=1&sn=38ca5f3af28d741b46e0197a5decd0a2&chksm=ce9ac737f9ed4e21f8a39efd85be7390863ab13faa9bafc1f031f1adef8b0c2b561f04302b20&scene=178&cur_album_id=2519398872503353344#rd)
- [Linux进程调度器的设计--Linux进程的管理与调度(十七)](https://blog.csdn.net/gatieme/article/details/51702662)
- [Linux内核学习笔记(5)-- 进程调度概述](https://www.cnblogs.com/tongye/p/9575602.html)
- [进程调度](https://blog.csdn.net/qq_38847853/article/details/80554515)
- [yeefea linux_kernel_dev4](https://yeefea.com/os/linux_kernel_dev4/)
- [linux内核分析 CFS(完全公平调度算法)](https://www.cnblogs.com/tianguiyu/articles/6091378.html)
- [进程管理](https://kernel.blog.csdn.net/article/details/51456569)
- [万字长文,锤它!揭秘Linux进程调度器](https://www.51cto.com/article/701537.html)
- [Linux CFS 调度器:原理、设计与内核实现](https://arthurchiao.art/blog/linux-cfs-design-and-implementation-zh/)
- [深入理解Linux内核进程的管理与调度(全知乎最详细)](https://zhuanlan.zhihu.com/p/472955572)
- [O(1) scheduler](https://en.wikipedia.org/wiki/O(1)_scheduler)
- [linux 进程优先级及调度](https://www.cnblogs.com/abels0025/p/11430740.html)

https://www.cnblogs.com/abels0025/p/11430740.html

https://arthurchiao.art/blog/linux-cfs-design-and-implementation-zh/

<https://arthurchiao.art/blog/linux-cfs-design-and-implementation-zh/>

https://zhuanlan.zhihu.com/p/472955572

> 内核能抢占了不代表内核一定会抢占,内核会不会抢占由config选项控制(`[CONFIG_PREEMPT](https://cateee.net/lkddb/web-lkddb/PREEMPT.html)`),可以开启也可以关闭,因为内核抢占还会影响系统的响应性和性能.
> 
> 开启内核抢占会提高系统的响应性但是会降低一点性能,关闭内核抢占会降低系统的响应性但是会提高一点性能.因此把内核抢占做成配置项,可以让大家灵活配置.
> 
> 服务器系统一般不需要与用户交互,所以会关闭内核抢占来提高性能,桌面系统会开启内核抢占来提高系统的响应性,来增加用户体验.

`[sched_yield](https://linux.die.net/man/2/sched_yield)`