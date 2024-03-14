
> 初始(idle)进程的名字 swapper 其实就是从 UNIX 时代延续下来的, 曾经也有人给 linux 提过 [patch](https://www.uwsg.indiana.edu/hypermail/linux/kernel/0604.2/1270.html) 想要将名字改为 "idle" 但被拒绝了
>
>> Yes, swapper is because of historical reasons. In most text books for
>> Unix, the initial process on boot up is called "swapper". Probably
>> because those early Unix systems had this process handle the swapping
>> (as kswapd does today).
>> 
>> By doing this, it will probably make Linux out of sync with all the text
>> books on Unix, so it really is Linus' call.
>
> 回复的意思大致是说 swapper 只是为了和 UNIX 系统保持一致

回复的意思大致是说 swapper 只是为了和 UNIX 系统保持一致
回复的意思大致是说 swapper 只是为了和 UNIX 系统保持一致