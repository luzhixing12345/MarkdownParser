
# C.md

## [31.c](https://github.com/luzhixing12345/syntaxlight/tree/main/test/c/31.c)

```c
/*
 * main - The shell's main routine
 */
int main(int argc, char **argv) {
  char c;
  char cmdline[MAXLINE];
  int emit_prompt = 1; /* emit prompt (default) */
  /* Redirect stderr to stdout (so that driver will get all output
   * on the pipe connected to stdout) */
  dup2(1, 2);
  /* Parse the command line */
  while ((c = getopt(argc, argv, "hvp")) != EOF) {
    switch (c) {
    case 'h': /* print help message */
      usage();
      break;
    case 'v': /* emit additional diagnostic info */
      verbose = 1;
      break;
    case 'p':          /* don't print a prompt */
      emit_prompt = 0; /* handy for automatic testing */
      break;
    default:
      usage();
    }
  }
  /* Install the signal handlers */
  /* These are the ones you will need to implement */
  Signal(SIGINT, sigint_handler);   /* ctrl-c */
  Signal(SIGTSTP, sigtstp_handler); /* ctrl-z */
  Signal(SIGCHLD, sigchld_handler); /* Terminated or stopped child */
  /* This one provides a clean way to kill the shell */
  Signal(SIGQUIT, sigquit_handler);
  /* Initialize the job list */
  initjobs(jobs);
  /* Execute the shell's read/eval loop */
  while (1) {
    /* Read command line */
    if (emit_prompt) {
      printf("%s", prompt);
      fflush(stdout);
    }
    if ((fgets(cmdline, MAXLINE, stdin) == NULL) && ferror(stdin))
      app_error("fgets error");
    if (feof(stdin)) { /* End of file (ctrl-d) */
      fflush(stdout);
      exit(0);
    }
    /* Evaluate the command line */
    eval(cmdline);
    fflush(stdout);
    fflush(stdout);
  }
  exit(0); /* control never reaches here */
}

/*
 * eval - Evaluate the command line that the user has just typed in
 *
 * If the user has requested a built-in command (quit, jobs, bg or fg)
 * then execute it immediately. Otherwise, fork a child process and
 * run the job in the context of the child. If the job is running in
 * the foreground, wait for it to terminate and then return.  Note:
 * each child process must have a unique process group ID so that our
 * background children don't receive SIGINT (SIGTSTP) from the kernel
 * when we type ctrl-c (ctrl-z) at the keyboard.
 */
void eval(char *cmdline) {
  char *argv[MAXARGS];
  char buf[MAXLINE];
  int bg;
  pid_t pid;
  strcpy(buf, cmdline);
  bg = parseline(buf, argv);
  if (argv[0] == NULL)
    return;
  sigset_t mask_all, mask_one, prev;
  sigfillset(&mask_all);
  sigemptyset(&mask_one);
  sigaddset(&mask_one, SIGCHLD);
  if (!builtin_cmd(argv)) {
    sigprocmask(SIG_BLOCK, &mask_one, &prev);
    if ((pid = fork()) == 0) {
      sigprocmask(SIG_SETMASK, &prev, NULL);
      setpgid(0, 0);
      if (execve(argv[0], argv, environ) < 0) {
        printf("%s: Command not found\n", argv[0]);
        exit(0);
      }
    }
    if (!bg) {
      // 对于前台进程,添加job后解除阻塞,并通过waitfg等待子进程结束后回收
      sigprocmask(SIG_BLOCK, &mask_all, NULL);
      addjob(jobs, pid, FG, cmdline);
      sigprocmask(SIG_SETMASK, &prev, NULL);
      waitfg(pid);
    } else {
      // 后台进程不需要等待子进程,进程结束之后收到SIGCHLD信号回收即可
      sigprocmask(SIG_BLOCK, &mask_all, NULL);
      addjob(jobs, pid, BG, cmdline);
      sigprocmask(SIG_SETMASK, &prev, NULL);
      printf("[%d] (%d) %s", pid2jid(pid), pid, cmdline);
    }
  }
  return;
}

/*
 * parseline - Parse the command line and build the argv array.
 *
 * Characters enclosed in single quotes are treated as a single
 * argument.  Return true if the user has requested a BG job, false if
 * the user has requested a FG job.
 */
int parseline(const char *cmdline, char **argv) {
  static char array[MAXLINE]; /* holds local copy of command line */
  char *buf = array;          /* ptr that traverses command line */
  char *delim;                /* points to first space delimiter */
  int argc;                   /* number of args */
  int bg;                     /* background job? */
  strcpy(buf, cmdline);
  buf[strlen(buf) - 1] = ' ';   /* replace trailing with space */
  while (*buf && (*buf == ' ')) /* ignore leading spaces */
    buf++;
  /* Build the argv list */
  argc = 0;
  if (*buf == '\'') {
    buf++;
    delim = strchr(buf, '\'');
  } else {
    delim = strchr(buf, ' ');
  }
  while (delim) {
    argv[argc++] = buf;
    *delim = '\0';
    buf = delim + 1;
    while (*buf && (*buf == ' ')) /* ignore spaces */
      buf++;
    if (*buf == '\'') {
      buf++;
      delim = strchr(buf, '\'');
    } else {
      delim = strchr(buf, ' ');
    }
  }
  argv[argc] = NULL;
  if (argc == 0) /* ignore blank line */
    return 1;
  /* should the job run in the background? */
  if ((bg = (*argv[argc - 1] == '&')) != 0) {
    argv[--argc] = NULL;
  }
  return bg;
}
```

- `闭包` 符号:* 字符串集合R的闭包是指把R与自身连接零次或者多次形成的所有集合的并集, 记作 `R*`.
- **XBOX_ARG_BOOLEAN**: 适用于单参数, 例如 `-h`, 后面不需要跟其他参数信息
- **XBOX_ARG_INT**: 表示参数接收的应该是一个 int 类型的数字, 例如 `-i 100`
- **XBOX_ARG_STR**: 表示参数接收的应该是一个 char* 类型的字符串, 例如 `-s "hello world"` `-s nihao`
- **XBOX_ARG_INT_GROUP**: 表示接收一个组, 组中只有一个元素, 组的数据类型是 int
- **XBOX_ARG_INT_GROUPS**: 表示接收一个组, 组中至少有一个元素, 组的数据类型是 int
- **XBOX_ARG_STR_GROUP**: 表示接收一个组, 组的数据类型是 char*
- **XBOX_ARG_STR_GROUPS**: 表示接收一个组, 组中至少有一个元素, 组的数据类型是 char*
- **XBOX_ARG_END**: 表示结束, 添加在 options 数组的结尾