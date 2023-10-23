

```python
class R_XOR(Instruction):
    def stage_ex(self):
        self.isa.pipeline_register.value = (
            self.isa.pipeline_register.rs1 ^ self.isa.pipeline_register.rs2
        )

    def stage_wb(self):
        self.isa.registers[self.isa.instruction_info.rd] = self.isa.pipeline_register.value
        return super().stage_wb()
```

```python
class ISA:
    def stage_ex(self):
        """
        EX-执行.对指令的各种操作数进行运算
        """
        self.instruction.stage_ex()

    def stage_mem(self):
        """
        MEM-存储器访问.将数据写入存储器或从存储器中读出数据
        """
        self.instruction.stage_mem()

    def stage_wb(self):
        """
        WB-写回.将指令运算结果存入指定的寄存器
        """
        self.instruction.stage_wb()
```