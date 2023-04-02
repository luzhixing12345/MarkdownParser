
```python
"""
This program demonstrates how to use all the keywords and syntax in Python
"""
# Importing modules
import math

# Defining a function
def greet(name):
    """
    This function greets the person passed in as a parameter
    """
    print(f"Hello, {name}!")

# Using conditional statements
x = 5
if x > 0:
    print("x is positive")
elif x < 0:
    print("x is negative")
else:
    print("x is zero")

# Using loops
for i in range(5):
    print(i)

# Using lists and list comprehension
fruits = ["apple", "banana", "cherry"]
new_list = [x for x in fruits if "a" in x]
print(new_list)

# Using dictionaries
person = {"name": "John", "age": 36, "country": "Norway"}
print(person)

# Using sets
thisset = {"apple", "banana", "cherry"}
thisset.add("orange")
print(thisset)

# Using try-except blocks
try:
    print(x)
except NameError:
    print("Variable x is not defined")
except:
    print("Something else went wrong")

# Using lambda functions
x = lambda a : a + 10
print(x(5))

# Using classes and objects
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p1 = Person("John", 36)
print(p1.name)
print(p1.age)

# Using recursion
def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n-1)

print(factorial(5))
```

```c
/*
 *Copyright (c) 2023 All rights reserved
 *@description: 有关信号处理的四个系统调用 中断处理程序中处理信号的函数 =>
 *do_signal
 *@author: Zhixing Lu
 *@date: 2023-03-17
 *@email: luzhixing12345@163.com
 *@Github: luzhixing12345
 */

#include <asm/segment.h>
#include <linux/kernel.h>
#include <linux/sched.h>
#include <signal.h>

volatile void do_exit(int error_code);

int sys_sgetmask() {
    return current->blocked;
}

int sys_ssetmask(int newmask) {
    int old = current->blocked;

    current->blocked = newmask & ~(1 << (SIGKILL - 1));
    return old;
}

static inline void save_old(char *from, char *to) {
    int i;

    verify_area(to, sizeof(struct sigaction));
    for (i = 0; i < sizeof(struct sigaction); i++) {
        put_fs_byte(*from, to);
        from++;
        to++;
    }
}

static inline void get_new(char *from, char *to) {
    int i;

    for (i = 0; i < sizeof(struct sigaction); i++)
        *(to++) = get_fs_byte(from++);
}

int sys_signal(int signum, long handler, long restorer) {
    struct sigaction tmp;

    if (signum < 1 || signum > 32 || signum == SIGKILL)
        return -1;
    tmp.sa_handler = (void (*)(int))handler;
    tmp.sa_mask = 0;
    tmp.sa_flags = SA_ONESHOT | SA_NOMASK;
    tmp.sa_restorer = (void (*)(void))restorer;
    handler = (long)current->sigaction[signum - 1].sa_handler;
    current->sigaction[signum - 1] = tmp;
    return handler;
}

int sys_sigaction(int signum, const struct sigaction *action,
                  struct sigaction *oldaction) {
    struct sigaction tmp;

    if (signum < 1 || signum > 32 || signum == SIGKILL)
        return -1;
    tmp = current->sigaction[signum - 1];
    get_new((char *)action, (char *)(signum - 1 + current->sigaction));
    if (oldaction)
        save_old((char *)&tmp, (char *)oldaction);
    if (current->sigaction[signum - 1].sa_flags & SA_NOMASK)
        current->sigaction[signum - 1].sa_mask = 0;
    else
        current->sigaction[signum - 1].sa_mask |= (1 << (signum - 1));
    return 0;
}

void do_signal(long signr, long eax, long ebx, long ecx, long edx, long fs,
               long es, long ds, long eip, long cs, long eflags,
               unsigned long *esp, long ss) {
    unsigned long sa_handler;
    long old_eip = eip;
    struct sigaction *sa = current->sigaction + signr - 1;
    int longs;
    unsigned long *tmp_esp;

    sa_handler = (unsigned long)sa->sa_handler;
    if (sa_handler == 1)
        return;
    if (!sa_handler) {
        if (signr == SIGCHLD)
            return;
        else
            do_exit(1 << (signr - 1));
    }
    if (sa->sa_flags & SA_ONESHOT)
        sa->sa_handler = NULL;
    *(&eip) = sa_handler;
    longs = (sa->sa_flags & SA_NOMASK) ? 7 : 8;
    *(&esp) -= longs;
    verify_area(esp, longs * 4);
    tmp_esp = esp;
    put_fs_long((long)sa->sa_restorer, tmp_esp++);
    put_fs_long(signr, tmp_esp++);
    if (!(sa->sa_flags & SA_NOMASK))
        put_fs_long(current->blocked, tmp_esp++);
    put_fs_long(eax, tmp_esp++);
    put_fs_long(ecx, tmp_esp++);
    put_fs_long(edx, tmp_esp++);
    put_fs_long(eflags, tmp_esp++);
    put_fs_long(old_eip, tmp_esp++);
    current->blocked |= sa->sa_mask;
}

```