
# 123789

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
## 123u8

asdint sys_sigaction(int signum, const struct sigaction *action,
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

## 123u890

### 123890

#### 123[890](ComplexBlock)

### 123
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
## 123

#### 1239

# 123

## 12334
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
# 123

# 123