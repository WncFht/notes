
`lec07.pdf` 文件是关于 RISC-V 指令集和如何实现函数的计算机科学课程内容。以下是该课程内容的详细讲解:

### 1. 寄存器和它们能存储的内容
- **寄存器**:32位宽，用于存储各种值。
- 可以存储数组的开始位置、字符串、整数值等。
- 寄存器用于快速访问和处理数据。

### 2. 已学习的指令
- **加法/减法**:`add`, `sub`，用于执行基本的算术运算。
- **加常数**:`addi`，用于将寄存器的值与立即数相加。
- **内存访问**:`lw` (load word), `lb` (load byte), `sw` (store word), `sb` (store byte)，用于在寄存器和内存之间传输数据。

### 3. 逻辑指令
- 包括逻辑与（`and`）、或（`or`）、异或（`xor`）。
- 位移指令:`sll` (shift left logical), `slli` (shift left logical immediate), `sra` (shift right arithmetic), `srai` (shift right arithmetic immediate)，用于执行位操作。

### 4. 条件分支
- 用于实现 `if`、`loops` 等控制流结构。
- 格式:`{comparison} {reg1} {reg2} {label}`，例如 `beq` (branch if equal), `bne` (branch if not equal), `blt` (branch if less than), `bge` (branch if greater than or equal)。
- 没有直接的 “branch-less-than-or-equals” 和 “branch-greater-than” 指令，但可以通过交换参数来实现。

### 5. 无条件分支
- `Jump` 指令:`j label`，总是跳转到标签指定的代码位置。

### 6. If-Else 语句的实现
- 使用分支指令来实现条件执行。
- 示例:根据两个寄存器的值是否相等，执行不同的操作。

### 7. 循环示例
- 使用循环来累加数组元素的和。
- 示例代码展示了如何初始化循环变量、循环条件以及循环体。

### 8. 程序计数器（PC）
- PC 是一个寄存器，存储当前正在执行的指令的内存地址。

### 9. 增加 PC 的值
- RV32 指令是 32 位宽，即 4 字节。
- 当移动到下一条指令时，处理器会增加 PC 的值 4 字节。

### 10. 函数执行位置的改变
- 使用跳转指令改变 PC 的值，以执行不同位置的函数。

### 11. JAL 指令
- `jal` 指令用于跳转到标签，并存储返回地址。
- 将标签通过汇编器转换为 20 位偏移量。
- ![QQ_1723431266150.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202408121054698.png)


### 12. 返回地址寄存器
- 可以选择任意寄存器来存储返回地址，但按照标准约定，使用寄存器 x1，也称为 `ra`。

### 13. 跳转示例
- 展示了如何在函数调用中使用 `jal` 和 `jr` 指令进行跳转和返回。
- 用x0可以不用存返回地址
- ![QQ_1723431462347.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202408121057402.png)


### 14. 伪指令
- 伪指令对程序员可用，但不是 ISA 的一部分。
- 由汇编器转换为实际的 RISC-V 指令。
- [[cs61c_lec06]]里就讲过了

### 15. JALR 指令
- `jalr` 指令结合了寄存器和立即数来计算跳转地址。
- ![QQ_1723431531375.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202408121058912.png)

- 用于从函数返回，不需要额外保存返回地址。

### 16. 跳转总结
- 总结了不同类型的跳转指令，包括 `jal`, `jalr`, `jr`, 和 `ret`。
- ![QQ_1723431585457.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202408121059044.png)
- ![QQ_1723431599577.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202408121100656.png)
- [[跳转和返回的函数]]



### 17. 保存寄存器
- 当调用另一个函数时，需要保存当前函数使用的寄存器值，以防止被覆盖。
- save in the stack

### 18. 为栈分配空间
- 栈用于存储自动（局部）变量，这些变量在函数退出时被丢弃。

### 19. 栈指针（SP）
- SP 是一个寄存器，存储栈上最后一项的内存地址。

### 20. 栈帧
- 栈帧是栈上的一块区域，用于存储函数的局部变量和寄存器状态。

### 21. 移动栈指针
- 通过增加或减少 SP 的值来在栈上分配或释放空间。
- ![QQ_1723432105639.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202408121108171.png)


### 22. 调用约定
- 调用约定定义了哪些寄存器由调用者保存，哪些由被调用者保存。

### 23. 寄存器使用说明
- 表格列出了每个寄存器的用途和谁负责保存它们。
- ![QQ_1723432177691.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202408121109361.png)


### 24. 参数寄存器
- 函数的参数和返回值通过特定的寄存器传递。

### 25. 调用约定示例
- 展示了如何在函数调用中使用参数寄存器和返回寄存器。
- ![QQ_1723432240129.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202408121110137.png)


### 26. 函数调用的六个基本步骤
- 从参数设置到控制权返回的详细过程。
- ![QQ_1723432339577.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202408121112112.png)


这份讲义涵盖了 RISC-V 汇编语言中控制流、函数调用、寄存器使用和内存管理的关键概念和技术。通过这些内容，学生可以学习如何在 RISC-V 架构上实现复杂的程序逻辑和函数交互。