# C++

## 1 文件操作

### 1.1 文件的概念

- C/C++把每一个文件都看成是一个有序的字节流，以文件结束标志（EOF）结束

### 1.2 文件的操作步骤

1. 打开文件，讲文件指针指向文件，决定打开文件的类型
2. 对文件进行读/写操作
3. 在使用完文件后，关闭文件

### 1.3 一些函数

#### 1.3.1 freopen 函数

```C++
FILE* freopen(const char* filename, const char* mode, FILE* stream);
```

- 参数说明
	- `filename`: 要打开的文件名
	- `mode`: 文件打开的模式，表示文件访问的权限
	- `stream`: 文件指针，通常使用标准文件流 (`stdin/stdout`) 或标准错误输出流 (`stderr`)
	- 返回值：文件指针，指向被打开文件
- 文件打开格式
	- `r`：以只读方式打开文件，文件必须存在，只允许读入数据 **（常用）**
	- `r+`：以读/写方式打开文件，文件必须存在，允许读/写数据
	- `rb`：以只读方式打开二进制文件，文件必须存在，只允许读入数据
	- `rb+`：以读/写方式打开二进制文件，文件必须存在，允许读/写数据
	- `rt+`：以读/写方式打开文本文件，允许读/写数据
	- `w`：以只写方式打开文件，文件不存在会新建文件，否则清空内容，只允许写入数据 **（常用）**
	- `w+`：以读/写方式打开文件，文件不存在将新建文件，否则清空内容，允许读/写数据
	- `wb`：以只写方式打开二进制文件，文件不存在将会新建文件，否则清空内容，只允许写入数据
	- `wb+`：以读/写方式打开二进制文件，文件不存在将新建文件，否则清空内容，允许读/写数据
	- `a`：以只写方式打开文件，文件不存在将新建文件，写入数据将被附加在文件末尾（保留 EOF 符）
	- `a+`：以读/写方式打开文件，文件不存在将新建文件，写入数据将被附加在文件末尾（不保留 EOF 符）
	- `at+`：以读/写方式打开文本文件，写入数据将被附加在文件末尾
	- `ab+`：以读/写方式打开二进制文件，写入数据将被附加在文件末尾  
**使用方式**

```C++
#include <cstdio>
#include <iostream>
int mian(void) {
	freopen("data.in", "r", stdin); 
	// data.in 就是读取的文件名，要和可执行文件放在同一目录下
	freopen("data.out", "w", stdout); 
	// data.out 就是输出文件的文件名，和可执行文件在同一目录下
	fclose(stdin);
	fclose(stdout);
}
```

#### 1.3.2 fopen 函数

```C++
FILE* fopen(const char* path, const char* mode)
```

**使用方式**

```C++
FILE *in, *out; // 定义文件指针 
in = fopen("data.in", "r"); 
out = fopen("data.out", "w"); 
/* do what you want to do */ 
fclose(in); 
fclose(out);
```

### 1.4 C++ 的 `ifstream/ofstream` 文件输入输出流

```C++
#include <fstream> 
using namespace std; 
// 两个类型都在 std 命名空间里 
ifstream fin("data.in"); 
ofstream fout("data.out"); 
int main(void) { 
	/* 中间的代码改变 cin 为 fin ，cout 为 fout 即可 */ 
	fin.close(); 
	fout.close(); 
	return 0; 
}
```

## 2 标准库

### 2.1 STL 容器

![image.png](https://raw.githubusercontent.com/WncFht/picture/main/picture/20240917140746.png)

#### 2.1.1 序列式容器

- **向量**(`vector`) 后端可高效增加元素的顺序表。
	- 可以动态分配内存
	- 重写了比较运算符及赋值运算符
	- 便利的初始化
	- [std::vector - cppreference.com](https://zh.cppreference.com/w/cpp/container/vector)
- **数组**(`array`)**C++11**，定长的顺序表，C 风格数组的简单包装。
- **双端队列**(`deque`) 双端都可高效增加元素的顺序表。
- **列表**(`list`) 可以沿双向遍历的链表。
- **单向列表**(`forward_list`) 只能沿一个方向遍历的链表。

#### 2.1.2 关联式容器

- **集合**(`set`) 用以有序地存储 **互异** 元素的容器。其实现是由节点组成的红黑树，每个节点都包含着一个元素，节点之间以某种比较元素大小的谓词进行排列。
- **多重集合**(`multiset`) 用以有序地存储元素的容器。允许存在相等的元素。
- **映射**(`map`) 由 {键，值} 对组成的集合，以某种比较键大小关系的谓词进行排列。
- **多重映射**(`multimap`) 由 {键，值} 对组成的多重集合，亦即允许键有相等情况的映射。

#### 2.1.3 无序（关联式）容器

- **无序（多重）集合**(`unordered_set`/`unordered_multiset`)**C++11**，与 `set`/`multiset` 的区别在于元素无序，只关心「元素是否存在」，使用哈希实现。
- **无序（多重）映射**(`unordered_map`/`unordered_multimap`)**C++11**，与 `map`/`multimap` 的区别在于键 (key) 无序，只关心 "键与值的对应关系"，使用哈希实现。

#### 2.1.4 容器适配器

容器适配器其实并不是容器。它们不具有容器的某些特点（如：有迭代器、有 `clear()` 函数……）。

> 「适配器是使一种事物的行为类似于另外一种事物行为的一种机制」，适配器对容器进行包装，使其表现出另外一种行为。

- **栈**(`stack`) 后进先出 (LIFO) 的容器，默认是对双端队列（`deque`）的包装。
- **队列**(`queue`) 先进先出 (FIFO) 的容器，默认是对双端队列（`deque`）的包装。
- **优先队列**(`priority_queue`) 元素的次序是由作用于所存储的值对上的某种谓词决定的的一种队列，默认是对向量（`vector`）的包装。

#### 2.1.5 共同点

##### 2.1.5.1 容器声明

- 都是 `containerName<typeName,...> name` 的形式，但模板参数（`<>` 内的参数）的个数、形式会根据具体容器而变。
- 本质原因：STL 就是「标准模板库」，所以容器都是模板类。

##### 2.1.5.2 迭代器

```C++
vector<int> data(10);

for (int i = 0; i < data.size(); i++)
	cout << data[i] << endl;

for (vector<int>::iterator iter = data.begin(); iter != data.end(); iter++)
	cout << *iter << endl;
//C++11 以后可以用 auto iter = data.begin() 来简化
```

- 分类
	- InputIterator（输入迭代器）：只要求支持拷贝、自增和解引访问。
	- OutputIterator（输出迭代器）：只要求支持拷贝、自增和解引赋值。
	- ForwardIterator（向前迭代器）：同时满足 InputIterator 和 OutputIterator 的要求。
	- BidirectionalIterator（双向迭代器）：在 ForwardIterator 的基础上支持自减（即反向访问）。
	- RandomAccessIterator（随机访问迭代器）：在 BidirectionalIterator 的基础上支持加减运算和比较运算（即随机访问）。
	- ContiguousIterator（连续迭代器）：在 RandomAccessIterator 的基础上要求对可解引用的迭代器 `a + n` 满足 `*(a + n)` 与 `*(std::address_of(*a) + n)` 等价（即连续存储，其中 `a` 为连续迭代器、`n` 为整型值）。

##### 2.1.5.3 共有函数

- `=`：有赋值运算符以及复制构造函数。
- `begin()`：返回指向开头元素的迭代器。
- `end()`：返回指向末尾的下一个元素的迭代器。`end()` 不指向某个元素，但它是末尾元素的后继。
- `size()`：返回容器内的元素个数。
- `max_size()`：返回容器 **理论上** 能存储的最大元素个数。依容器类型和所存储变量的类型而变。
- `empty()`：返回容器是否为空。
- `swap()`：交换两个容器。
- `clear()`：清空容器。
- `==`/`!=`/`<`/`>`/`<=`/`>=`：按 **字典序** 比较两个容器的大小。（比较元素大小时 `map` 的每个元素相当于 `set<pair<key, value> >`，无序容器不支持 `<`/`>`/`<=`/`>=`。）

#### 2.1.6 STL 算法

- `find`：顺序查找。`find(v.begin(), v.end(), value)`，其中 `value` 为需要查找的值。
- `reverse`：翻转数组、字符串。`reverse(v.begin(), v.end())` 或 `reverse(a + begin, a + end)`。
- `unique`：去除容器中相邻的重复元素。`unique(ForwardIterator first, ForwardIterator last)`，返回值为指向 **去重后** 容器结尾的迭代器，原容器大小不变。与 `sort` 结合使用可以实现完整容器去重。
- `sort`：排序。`sort(v.begin(), v.end(), cmp)` 或 `sort(a + begin, a + end, cmp)`，其中 `end` 是排序的数组最后一个元素的后一位，`cmp` 为自定义的比较函数。
- `stable_sort`：稳定排序，用法同 `sort()`。
- `nth_element` ：按指定范围进行分类，即找出序列中第 $\displaystyle n$ 大的元素，使其左边均为小于它的数，右边均为大于它的数。 `nth_element(v.begin(), v.begin() + mid, v.end(), cmp)` 或 `nth_element(a + begin, a + begin + mid, a + end, cmp)` 。
- `binary_search`：二分查找。`binary_search(v.begin(), v.end(), value)`，其中 `value` 为需要查找的值。
- `merge`：将两个（已排序的）序列 **有序合并** 到第三个序列的 **插入迭代器** 上。`merge(v1.begin(), v1.end(), v2.begin(), v2.end() ,back_inserter(v3))`。
- `inplace_merge`：将两个（已按小于运算符排序的）：`[first,middle), [middle,last)` 范围 **原地合并为一个有序序列**。`inplace_merge(v.begin(), v.begin() + middle, v.end())`。
- `lower_bound`：在一个有序序列中进行二分查找，返回指向第一个 **大于等于** ![](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "x") 的元素的位置的迭代器。如果不存在这样的元素，则返回尾迭代器。`lower_bound(v.begin(),v.end(),x)`。
- `upper_bound`：在一个有序序列中进行二分查找，返回指向第一个 **大于** ![](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "x") 的元素的位置的迭代器。如果不存在这样的元素，则返回尾迭代器。`upper_bound(v.begin(),v.end(),x)`。
- `next_permutation`：将当前排列更改为 **全排列中的下一个排列**。如果当前排列已经是 **全排列中的最后一个排列**（元素完全从大到小排列），函数返回 `false` 并将排列更改为 **全排列中的第一个排列**（元素完全从小到大排列）；否则，函数返回 `true`。`next_permutation(v.begin(), v.end())` 或 `next_permutation(v + begin, v + end)`。
- `prev_permutation`：将当前排列更改为 **全排列中的上一个排列**。用法同 `next_permutation`。
- `partial_sum`：求前缀和。设源容器为 ![](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "x")，目标容器为 ![](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "y")，则令 ![](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "y[i]=x[0]+x[1]+\dots+x[i]")。`partial_sum(src.begin(), src.end(), back_inserter(dst))`。

### 2.2 bitset

TODO  
[bitset - OI Wiki](https://oi-wiki.org/lang/csl/bitset/)

### 2.3 string

- 重载运算符
- 动态分配空间

```C++
std::string s;
printf("%s", s.c_str());
printf("s 的长度为 %lu", s.size()); 
printf("s 的长度为 %lu", s.length()); 
printf("s 的长度为 %lu", strlen(s.c_str()));
substr(pos, len);
insert(index, count, ch);
insert(index, str);
erase(index, count);
replace(pos, count, str);
replace(first, last, str);
```

### 2.4 pair

- `pair` 不需要额外定义结构与重载运算符

```C++
pair<int, double> p0(1, 2.0);
pair<int, double> p2 = make_pair(1, 2.0);
auto p3 = make_pair(1, 2.0);

int i = p0.first; 
double d = p0.second;
p1.first++;

priority_queue<pair<int, double> > q;
```

## 3 进阶

### 3.1 类

### 3.2 动态内存

#### 3.2.1 new 和 delete 运算符

- 栈: 声明的所有变量将占用栈内存
- 堆: 未使用的内存

```C++
new data-type;

double* pvalue = NULL;
pvalue = new double;

if (!(pvalue = new double)) {
	cout << "Error: out of memory." << endl;
	exit(1);
}

delete pvalue;
```

- new 不仅分配的内存还创建了对象
- malloc () 只分配的内存

#### 3.2.2 数组的动态内存分配

```C++
int ***array;
// 假定数组第一维为 m， 第二维为 n， 第三维为h
// 动态分配空间
array = new int **[m];
for( int i=0; i<m; i++ )
{
    array[i] = new int *[n];
    for( int j=0; j<n; j++ )
    {
        array[i][j] = new int [h];
    }
}
//释放
for( int i=0; i<m; i++ )
{
    for( int j=0; j<n; j++ )
    {
        delete [] array[i][j];
    }
    delete [] array[i];
}
delete [] array;
```

#### 3.2.3 对象的动态内存分配

```C++
#include <iostream>
using namespace std;
 
class Box
{
   public:
      Box() { 
         cout << "调用构造函数！" <<endl; 
      }
      ~Box() { 
         cout << "调用析构函数！" <<endl; 
      }
};
 
int main( )
{
   Box* myBoxArray = new Box[4]; // 一个包含 4 个 Box 对象的数组
 
   delete [] myBoxArray; // 删除数组
   return 0;
}
```

```out
调用构造函数！
调用构造函数！
调用构造函数！
调用构造函数！
调用析构函数！
调用析构函数！
调用析构函数！
调用析构函数！
```

### 3.3 命名空间

- 编译器为了区别同名函数引入了命名空间

#### 3.3.1 定义命名空间

```C++
namespace namespace_name {
 // code
}

namespace_name::code;
```

#### 3.3.2 using 指令

#### 3.3.3 不连续的命名空间

#### 3.3.4 嵌套的命名空间

```C++
namespace namespace_name1 {
   // 代码声明
   namespace namespace_name2 {
      // 代码声明
   }
}

// 访问 namespace_name2 中的成员
using namespace namespace_name1::namespace_name2;
 
// 访问 namespace_name1 中的成员
using namespace namespace_name1;
```

### 3.4 模板

- 泛型编程: 独立于任何特定类型的方式写代码

#### 3.4.1 函数模板

```C++
template <typename type> ret-type func-name(parameter list)
{
   // 函数的主体
}
```

```C++
#include <iostream>
#include <string>
 
using namespace std;
 
template <typename T>
inline T const& Max (T const& a, T const& b) 
{ 
    return a < b ? b:a; 
} 

int main ()
{
 
    int i = 39;
    int j = 20;
    cout << "Max(i, j): " << Max(i, j) << endl; 
 
    double f1 = 13.5; 
    double f2 = 20.7; 
    cout << "Max(f1, f2): " << Max(f1, f2) << endl; 
 
    string s1 = "Hello"; 
    string s2 = "World"; 
    cout << "Max(s1, s2): " << Max(s1, s2) << endl; 
 
    return 0;
}
```

#### 3.4.2 类模板

```C++
template <class type> class class-name {
// code
}
```

```C++
#include <iostream>
#include <vector>
#include <cstdlib>
#include <string>
#include <stdexcept>
 
using namespace std;
 
template <class T>
class Stack { 
  private: 
    vector<T> elems;     // 元素 
 
  public: 
    void push(T const&);  // 入栈
    void pop();               // 出栈
    T top() const;            // 返回栈顶元素
    bool empty() const{       // 如果为空则返回真。
        return elems.empty(); 
    } 
}; 
 
template <class T>
void Stack<T>::push (T const& elem) 
{ 
    // 追加传入元素的副本
    elems.push_back(elem);    
} 
 
template <class T>
void Stack<T>::pop () 
{ 
    if (elems.empty()) { 
        throw out_of_range("Stack<>::pop(): empty stack"); 
    }
    // 删除最后一个元素
    elems.pop_back();         
} 
 
template <class T>
T Stack<T>::top () const 
{ 
    if (elems.empty()) { 
        throw out_of_range("Stack<>::top(): empty stack"); 
    }
    // 返回最后一个元素的副本 
    return elems.back();      
} 
 
int main() 
{ 
    try { 
        Stack<int>       intStack;    // int 类型的栈 
        Stack<string> stringStack;    // string 类型的栈 
 
        // 操作 int 类型的栈 
        intStack.push(7); 
        cout << intStack.top() <<endl; 
 
        // 操作 string 类型的栈 
        stringStack.push("hello"); 
        cout << stringStack.top() << std::endl; 
        stringStack.pop(); 
        stringStack.pop(); 
    } 
    catch (exception const& ex) { 
        cerr << "Exception: " << ex.what() <<endl; 
        return -1;
    } 
}
```

```out
7
hello
Exception: Stack<>::pop(): empty stack
```

### 3.5 预处理器

- 不是 C++语句，不会以分号结尾

#### 3.5.1 #define 预处理

```C++
#define macro-name replacement-text 
```

#### 3.5.2 参数宏

```C++
#include <iostream>
using namespace std;
 
#define MIN(a,b) (a<b ? a : b)
 
int main ()
{
   int i, j;
   i = 100;
   j = 30;
   cout <<"较小的值为：" << MIN(i, j) << endl;
 
    return 0;
}
```

#### 3.5.3 条件编译

```C++
#ifdef NULL
   #define NULL 0
#endif

#ifdef DEBUG
   cerr <<"Variable x = " << x << endl;
#endif

#if 0
   不进行编译的代码
#endif
```

#### 3.5.4 # 和 ## 运算符

```C++
#include <iostream>
using namespace std;
 
#define MKSTR( x ) #x
 
int main ()
{
    cout << MKSTR(HELLO C++) << endl;
 
    return 0;
}
```

```C++
#include <iostream>
using namespace std;
 
#define concat(a, b) a ## b
int main()
{
   int xy = 100;
   
   cout << concat(x, y);
   return 0;
}
```

#### 3.5.5 预定义宏

![QQ_1726539879740.png](https://raw.githubusercontent.com/WncFht/picture/main/picture/QQ_1726539879740.png)

### 3.6 信号处理

![QQ_1726539936441.png](https://raw.githubusercontent.com/WncFht/picture/main/picture/QQ_1726539936441.png)

#### 3.6.1 signal () 函数

```C++
void (*signal (int sig, void (*func)(int)))(int); 

signal(registered signal, signal handler)
```

```C++
#include <iostream>
#include <csignal>
#include <unistd.h>
 
using namespace std;
 
void signalHandler( int signum )
{
    cout << "Interrupt signal (" << signum << ") received.\n";
 
    // 清理并关闭
    // 终止程序  
 
   exit(signum);  
 
}
 
int main ()
{
    // 注册信号 SIGINT 和信号处理程序
    signal(SIGINT, signalHandler);  
 
    while(1){
       cout << "Going to sleep...." << endl;
       sleep(1);
    }
 
    return 0;
}
```

按 Ctrl + C 中断程序:

```out
Going to sleep....
Going to sleep....
Going to sleep....
Interrupt signal (2) received.
```

#### 3.6.2 raise () 函数

```C++
int raise (signal sig);
```

```C++
#include <iostream>
#include <csignal>
#include <unistd.h>
 
using namespace std;
 
void signalHandler( int signum )
{
    cout << "Interrupt signal (" << signum << ") received.\n";
 
    // 清理并关闭
    // 终止程序 
 
   exit(signum);  
 
}
 
int main ()
{
    int i = 0;
    // 注册信号 SIGINT 和信号处理程序
    signal(SIGINT, signalHandler);  
 
    while(++i){
       cout << "Going to sleep...." << endl;
       if( i == 3 ){
          raise(SIGINT);
       }
       sleep(1);
    }
 
    return 0;
}
```

### 3.7 多线程

- 两种类型的多任务处理
	- 基于进程是程序的并发执行
	- 基于线程是同一程序的片段的并发执行

#### 3.7.1 概念说明

##### 3.7.1.1 线程（Thread）

- 线程是程序执行中的单一顺序控制流，多个线程可以在同一个进程中独立运行。
- 线程共享进程的地址空间、文件描述符、堆和全局变量等资源，但每个线程有自己的栈、寄存器和程序计数器。

##### 3.7.1.2 并发（Concurrency）与并行 （Parallelism）

- **并发**：多个任务在时间片段内交替执行，表现出同时进行的效果。
- **并行**：多个任务在多个处理器或处理器核上同时执行。  
C++11 以后有多线程支持:
- [std::thread](https://www.runoob.com/cplusplus/cpp-libs-thread.html)：用于创建和管理线程。
- [std::mutex](https://www.runoob.com/cplusplus/cpp-libs-mutex.html)：用于线程之间的互斥，防止多个线程同时访问共享资源。
- std::lock_guard 和 std::unique_lock：用于管理锁的获取和释放。
- [std::condition_variable](https://www.runoob.com/cplusplus/cpp-libs-condition_variable.html)：用于线程间的条件变量，协调线程间的等待和通知。
- [std::future](https://www.runoob.com/cplusplus/cpp-libs-future.html) 和 std::promise：用于实现线程间的值传递和任务同步。

#### 3.7.2 创建线程

```C++
#include<thread>
std::thread thread_object(callable, args...);
```

##### 3.7.2.1 使用函数指针

```C++
#include <iostream>
#include <thread>

void printMessage(int count) {
    for (int i = 0; i < count; ++i) {
        std::cout << "Hello from thread (function pointer)!\n";
    }
}

int main() {
    std::thread t1(printMessage, 5); // 创建线程，传递函数指针和参数
    t1.join(); // 等待线程完成
    return 0;
}
```

##### 3.7.2.2 使用函数对象

```C++
#include <iostream>
#include <thread>

class PrintTask {
public:
    void operator()(int count) const {
        for (int i = 0; i < count; ++i) {
            std::cout << "Hello from thread (function object)!\n";
        }
    }
};

int main() {
    std::thread t2(PrintTask(), 5); // 创建线程，传递函数对象和参数
    t2.join(); // 等待线程完成
    return 0;
}
```

##### 3.7.2.3 使用 Lambda 表达式

```C++
#include <iostream>
#include <thread>

int main() {
    std::thread t3([](int count) {
        for (int i = 0; i < count; ++i) {
            std::cout << "Hello from thread (lambda)!\n";
        }
    }, 5); // 创建线程，传递 Lambda 表达式和参数
    t3.join(); // 等待线程完成
    return 0;
}
```

##### 3.7.2.4 线程管理

```C++
t.join();
t.detach();
```

##### 3.7.2.5 线程的传参

##### 3.7.2.6 值传递

```C++
std::thread t(funx, arg1, arg2);
```

##### 3.7.2.7 引用传递

```C++
#include <iostream>
#include <thread>

void increment(int& x) {
    ++x;
}

int main() {
    int num = 0;
    std::thread t(increment, std::ref(num)); // 使用 std::ref 传递引用
    t.join();
    std::cout << "Value after increment: " << num << std::endl;
    return 0;
}
```

#### 3.7.3 线程同步与互斥

##### 3.7.3.1 互斥量（Mutex）

```C++
std::mutex mtx;
mtx.lock();   // 锁定互斥锁
// 访问共享资源
mtx.unlock();// 释放互斥锁

std::lock_guard<std::mutex> lock(mtx); // 自动锁定和解锁
// 访问共享资源
```

##### 3.7.3.2 锁（Locks）

- `std::lock_guard` ：作用域锁，当构造时自动锁定互斥量，当析构时自动解锁。
- `std::unique_lock` ：与 `std::lock_guard` 类似，但提供了更多的灵活性，例如可以转移所有权和手动解锁。

```C++ 
#include <mutex>

std::mutex mtx;

void safeFunctionWithLockGuard() {
    std::lock_guard<std::mutex> lk(mtx);
    // 访问或修改共享资源
}

void safeFunctionWithUniqueLock() {
    std::unique_lock<std::mutex> ul(mtx);
    // 访问或修改共享资源
    // ul.unlock(); // 可选：手动解锁
    // ...
}
```

##### 3.7.3.3 条件变量（Condition Variable）

```C++ 
std::condition_variable cv;
std::mutex mtx;
bool ready = false;

std::unique_lock<std::mutex> lock(mtx);
cv.wait(lock, []{ return ready; }); // 等待条件满足
// 条件满足后执行
```

```C++ 
#include <mutex>
#include <condition_variable>

std::mutex mtx;
std::condition_variable cv;
bool ready = false;

void workerThread() {
    std::unique_lock<std::mutex> lk(mtx);
    cv.wait(lk, []{ return ready; }); // 等待条件
    // 当条件满足时执行工作
}

void mainThread() {
    {
        std::lock_guard<std::mutex> lk(mtx);
        // 准备数据
        ready = true;
    } // 离开作用域时解锁
    cv.notify_one(); // 通知一个等待的线程
}
```

TODO

##### 3.7.3.4 原子操作（Atomic Operations）

- 对共享数据的访问不可分割

```C++
#include <atomic>
#include <thread>

std::atomic<int> count(0);

void increment() {
    count.fetch_add(1, std::memory_order_relaxed);
}

int main() {
    std::thread t1(increment);
    std::thread t2(increment);
    t1.join();
    t2.join();
    return count; // 应返回2
}
```

##### 3.7.3.5 线程局部存储（Thread Local Storage，TLS）

- 允许每个线程有自己的数据副本

```C++
#include <iostream>
#include <thread>

thread_local int threadData = 0;

void threadFunction() {
    threadData = 42; // 每个线程都有自己的threadData副本
    std::cout << "Thread data: " << threadData << std::endl;
}

int main() {
    std::thread t1(threadFunction);
    std::thread t2(threadFunction);
    t1.join();
    t2.join();
    return 0;
}
```

##### 3.7.3.6 死锁（Deadlock）和避免策略

- 死锁即多个线程互相等待对方释放资源
	- 总是以相同的顺序请求资源。
	- 使用超时来尝试获取资源。
	- 使用死锁检测算法。

#### 3.7.4 线程间通信

```C++
std::promise<int> p;
std::future<int> f = p.get_future();

std::thread t([&p] {
    p.set_value(10); // 设置值，触发 future
});

int result = f.get(); // 获取值
```

C++17 引入了并行算法库

```C++
#include <algorithm>
#include <vector>
#include <execution>

std::vector<int> vec = {1, 2, 3, 4, 5};
std::for_each(std::execution::par, vec.begin(), vec.end(), [](int &n) {
    n *= 2;
});
```

TODO  
[多线程实例](https://www.runoob.com/w3cnote/cpp-multithread-demo.html)

### 3.8 Web 编程

#### 3.8.1 什么是 CGI？

- 公共网关接口（CGI），是一套标准，定义了信息是如何在 Web 服务器和客户端脚本之间进行交换的。
- CGI 规范目前是由 NCSA 维护的，NCSA 定义 CGI 如下：
	- 公共网关接口（CGI），是一种用于外部网关程序与信息服务器（如 HTTP 服务器）对接的接口标准。

#### 3.8.2 Web 浏览

- 您的浏览器联系上 HTTP Web 服务器，并请求 URL，即文件名。
- Web 服务器将解析 URL，并查找文件名。如果找到请求的文件，Web 服务器会把文件发送回浏览器，否则发送一条错误消息，表明您请求了一个错误的文件。
- Web 浏览器从 Web 服务器获取响应，并根据接收到的响应来显示文件或错误消息。

#### 3.8.3 CGI 架构图

![image.png](https://raw.githubusercontent.com/WncFht/picture/main/picture/20240917120115.png)

#### 3.8.4 Web 服务器配置

TODO
