---
number headings: auto, first-level 1, max 6, contents ^toc, skip ^ski, start-at 0, _.1.1
---

# Accelerated C++

## 0 开始学习 C++

```C++
#include <iostream>

int main()
{
	std::cout << "Hello, World!" << std::endl;
	return 0;
}
```

### 0.1 注释

### 0.2 $\displaystyle \#$include 指令

- 输入、输出不属于语言核心，而是标准库的一部分
- iostream 代表 C++库的标准头文件

### 0.3 主函数 main

### 0.4 花括号

### 0.5 使用标准库进行输出

- std:: cout 指标准输出流

### 0.6 返回语句

### 0.7 一些较为深入的观察

- 表达式
	- 运算会产生一个结果，可能会具有副作用
- 每个操作数都具有一个类型
- <<是左结合的，所以我们可以使用两个<<运算符和三个操作数

```C++
(std::cout << "Hello, World!") << std::endl
```

- std:: cout 的类型是 std::ostream
- std:: endl 是一个控制器（manipulator）
- 第一种作用域: 名字空间
- :: 是作用域运算符，std:: cout 是一个限定名称
- 花括号是另一种作用域

### 0.8 小结

- main 可以没有 return 语句

## 1 使用字符串

### 1.1 输入

```C++
#include <iostream>
#include <string>

int main() 
{
	std::cout << "Please enter your first name:";

	std::string name;
	std::cin >> name;

	std::cout << "Hello" << name << "!" << std::endl;
	return 0;
}
```

- 变量是一个对象，但有些对象可能没有名称
- 局部变量有限的生存期是区分变量和对象的一个重要依据
- 隐藏在对象类型中的还有其接口
	- 接口是可实现操作的集合
- 缓冲区来保存输出
- 何时刷新缓冲区:
	- 缓冲区满了
	- 输入流读数据
	- 明确要求刷新

### 1.2 为姓名装框

- 运算符被重载了
- 运算符一个永远不会改变的性质是结合律，+是左结合的

```C++
std::string stars(10, '*')
```

### 1.3 小结

## 2 循环和计数

### 2.1 问题

### 2.2 程序的整体结构

### 2.3 输出数目未知的行

#### 2.3.1 while 语句

- ++是一个增量运算符

#### 2.3.2 设计 while 语句

- 循环不变式（Loop invariant）
	- **初始化**：在循环开始之前，循环不变式应该被确立为真。
	- **保持**：循环的每次迭代都必须保持循环不变式为真，即如果进入某次迭代时循环不变式为真，那么在该次迭代结束时，循环不变式仍然为真。
	- **终止**：当循环结束时，循环不变式应该能够用来证明循环的终止条件成立，或者用来证明循环的输出或结果满足特定的属性。
	- 循环不变式的一个典型例子是在排序算法中，例如冒泡排序。在冒泡排序中，一个可能的循环不变式是：“每次循环迭代后，数组的最后n个元素是排序好的”，其中n是循环迭代的次数。

### 2.4 输出一行

```C++
const std::string::size_type cols = greeting.size() + pad * 2 + 2;
```

#### 2.4.1 输出边界字符

##### 2.4.1.1 if 语句

##### 2.4.1.2 逻辑运算符

- ||是左结合，会有短路求值（short-circuit evaluation）

#### 2.4.2 输出非边界字符

- +=复合赋值运算符

### 2.5 完整的框架程序

#### 2.5.1 略去重复使用的 std::

#### 2.5.2 使用 for 语句来缩短程序

- 区间的越界值（off-the-end value）

```C++
for (int r = 0; r != rows; ++r) {

}
```

- 这是半开区间

```C++
for (init-statement condition; expression)
	statement

#equals to

{
	inti-statement
	while (condition) {
		statement
		expression;
	}
}
```

#### 2.5.3 压缩检测

- 就是把 if 语句合并一下

#### 2.5.4 完整的框架程序

### 2.6 计数

- 不对成区间可以直接看出有多少个元素
	- $\displaystyle [m, n]$ 有 m - n 个元素
- 而且可以表示空区间 $\displaystyle [n, n]$ 

### 2.7 小结

- 表达式
	- 操作数的组合方式
	- 操作数如何被转换
	- 操作数的运算次序

## 3 使用批量数据

### 3.1 计算学生成绩

```C++
#include <iomanip>
#include <ios>
#include <iostream>
#include <string>

using std::cin;
using std::cout;
using std::endl;
using std::precision;

int main() {
	cout << "Please enter your first name:";
	string name;
	cin >> name;
	cout << "Hello, " << name << "!" << endl;
	
	cout << "Please enter your midterm and final exam grades:";
	double midterm, final;
	cin >> midterm >> final;

	cout << "Enter all your homework grades, " 
			"followed by end-of-file:";

	int count = 0;
	double sum = 0;

	double x;

	while (cin >> x) {
		++ count;
		sum += x;
	}

	streamsize prec = cout.precision();
	cout << "Your final grade is " << setprecision(3)
		 << 0.2 * midterm + 0.4 * final + 0.4 * sum / count
		 << setprecision(prec) << endl; //重置有效位数 或写成cout.precision(prec);
	return 0;
}
```

- 输入运算符返回它的左操作数作为结果
- 却省初始化
- setprecision 也是一个控制器: 为流的后继输出设置了一个特定的有效位数

#### 3.1.1 检测输出

- istream 可以被转换成 bool 值
- 有三种情况条件会变假:
	- 达到输入文件的结尾
	- 输入和我们试图读取的变量类型不一致
	- 检测到一个硬件问题

#### 3.1.2 循环不变式

不是很懂

### 3.2 用中值代替平均值

那么就要排序了

#### 3.2.1 把数据集合存储在向量中

```C++
double x;
vector<double> homework;

while(cin >> x)
	homework.push_back(x);
```

- 我们使用了一种名为模板类的语言特征

#### 3.2.2 产生输出

```C++
typedef vector<double>::size_type vec_sz;
vec_sz size = homework.size();
```

- 我们希望保持系统环境的独立性

```C++
if (size  == 0) {
	cout << endl << "You must enter your grades. "
					"Please try again." << endl;
	return 1;
}

sort (homework.begin(), homework.end());

vec_sz mid = size / 2;
double median;
median = size % 2 == 0 ? (homework[mid] + homework[mid - 1]) / 2
					   : homework[mid];
```

#### 3.2.3 一些更为深入的观察

- size_type 是无符号整数类型

### 3.3 小结

## 4 组织程序和数据

- 这些库工具有几个同样的特性:
	- 能解决某些特定类型的问题
	- 与其他的大多数工具都相互独立
	- 都具有一个名称
- 两种方法来组织大型的程序
	- 函数
	- 数据结构

### 4.1 组织计算

- 参数的初始值是相应参数值的复制，即按值调用（call by value）

#### 4.1.1 查找中值

```C++
double median(vector<double> vec)
{
	typedef vector<double>::size_type vec_sz;
	vec_sz size = vec.size();
	if (size == 0)
		throw domain_error("median of an empty vector");
	sort(vec.begin(), vec.end());
	vec_sz mid = size / 2;
	return size % 2 == 0 ? (vec[mid] + vec[mid - 1]) / 2 : vec[mid];
}
```

- 抛出异常

#### 4.1.2 重新制定计算成绩的策略

- 只能把不是常量的引用给常量的，即条件只能加强
- 有好几个同样函数名的函数时，会发生重载

#### 4.1.3 读家庭作业成绩

- 左值参数: 非临时对象

```C++
istream read_hw(istream& in, vector<double>& hw)
{
	if (in) {
		hw.clear();
		double x;
		while (in >> x) 
			hw.push_back(x);
		in.clear();
	}
	return in;
}
```

#### 4.1.4 三种函数参数

- 一般而言，我们没有必要为了 int 或 double 这样见到你的内部类型的参数而去使用 const 引用
- 如果传入 read_hw () 的不是一个左值，那么我们会把输入存到一个我们无妨访问的对象中（改对象会在 read_hw() 返回时立即消失）

#### 4.1.5 使用函数来计算学生的成绩

- 不要让一条语句中的副作用个数超过一个

### 4.2 组织数据

#### 4.2.1 把一个学生的所有数据放置在一起

```C++
struct Student_info {
	string name;
	double midterm, final;
	vector<double> homework;
}
```

#### 4.2.2 处理学生记录

```C++
istream& read(istream& is, Student_info& s)
{
	is >> s.name >> s.midterm >> s.final;
	read_hw(is, s.homework);
	return is;
}

double grade(const Student_info& s) 
{
	return grade(s.midterm, s.final, s.homework);
}

bool compare(const Student_info& x, const Studeng_info& y)
{
	return x.name < y.name;
}

sort(students.begin(), students.end(), compare;
```

#### 4.2.3 生成报表

```C++
cout << setw(maxlen + 1) << student[i].name;
```

### 4.3 把各部分代码连接到一起

```median.h
#ifndef GUARD_median_h
#define GUARD_median_h //预处理程序

#include <vector>
double median(vector<double>);

#endif
```

### 4.4 把计算成绩的程序分块

### 4.5 修正后的计算成绩的程序

### 4.6 小结

- 用户定义的头文件一般以 .h 结尾
- 不应该在头文件中使用 using 声明
- 用 $\displaystyle \#$ ifndef 指令来防止对头文件的重复包含
- 内联子过程通常时在头文件而不是在源文件中定义 inline
	- 为了比卖你函数调用的额外开销，编译器会用函数体的一个复制来替换对函数的每一个调用并根据需要进行修正
- 异常处理

```C++
try{
} catch (t) { }
```

- 异常类

## 5 使用顺序容器并分析字符串

### 5.1 按类别来区分学生

```C++
vector<Student_info> extract_fails(vector<Student_info>& students)
{
	vector<Student_info> pass, fail;
	for (vector<Student_info>::size_type i = 0; i != students.size(); ++i;)
	if (fgrade(student[i]))
		fail.push_back(student[i]);
	else
		pass.push_back(student[i]);
	students = pass;
	return fail;
}
```

#### 5.1.1 就地删除函数

```C++
vector<Student_info> extract_fails(vector<Student_info>& students)
{
	vector<Student_info> fail;
	vector<Student_info>::size_type i =  0;
	while (i != students.size()) {
		if (fgrade(studentp[i])) {
			fail.push_back(students[i]);
			students.erase(students.begin() + i);
		} else
			++i;
	}
	return fail;
}
```

#### 5.1.2 顺序存取与随机存取

- 访问容器时所采取的次序会导致不同的性能特性
- 于是便有了 iterator

### 5.2 迭代器

- iterator
	- 识别一个容器以及容器中的一个元素
	- 让我们检查存储在这个元素中的值
	- 提供操作来移动在容易中的元素
	- 采用对应于容器所能够有效处理的方式对可用的操作进行约束

```C++
for (vector<Student_info>::size_type i = 0; i != students.end(); ++i)
	cout << students[i].name << endl;
for (vector<Student_info>::const_iterator iter = students.begin();
	iter != students.end(); ++iter) {
	cout << (*iter).name << endl; }
```

#### 5.2.1 迭代器类型

#### 5.2.2 迭代器操作

- end 紧接在容器最后一个元素后面的位置
- ++iter 用了迭代器类型重载
- 当我们用间接引用运算符 $\displaystyle *$ 来访问这个元素，那么他会返回一个左值（迭代器所指向的元素）
- $\displaystyle .$ 的优先级比 $\displaystyle *$ 高

#### 5.2.3 一点语法知识

```C++
(*iter).name
iter->name
//both are ok
```

#### 5.2.4 students. erase (students. begin () + i) 的含义

- students 不支持随机访问索引操作的容器，但是仍会允许迭代器的随机访问

### 5.3 用迭代器来代替索引

```C++
vecotr<Student_info> extract_fails(vector<Student_info>& students)
{
	vector<Student_info> fail;
	vector<Student_info>::iterator iter = students.begin();
	while (iter != students.end()) {
		if (fgrade(*iter)) {
			fail.push_back(*iter);
			iter = students.erase(iter); //important
		} else
			++iter;
	}
	return fail;
}
```

### 5.4 重新思考数据结构以实现更好的性能

### 5.5 list 类型

- 直接把所有的 vector 换成 list 就可以了

#### 5.5.1 一些重要的差别

- list 类的迭代器并不支持完全随机的访问
	- 所以我们不能用 sort 函数
	- 但是 list 有自己成员函数

#### 5.5.2 一个恼人的话题

### 5.6 分割字符串

```C++
vector<string> split(const string& s)
{
	vector<string> ret;
	typedef string::size_def string_size;
	string_size i = 0;
	while (i != s.size()) {
		while (i != s.size() && isspace(s[i])) // is from <cctype>
			++i;
		string_size j = i;
		while (j != s.size() && !isspace(s[i]))
			++j;
		if (i != j) {
			ret.push_back(s.substr(i, j - i));
			i = j;
		}
	}
	return ret;
}
```

### 5.7 测试 split 函数

### 5.8 连接字符串

#### 5.8.1 为图案装框

#### 5.8.2 纵向连接

#### 5.8.3 横向连接

TODO

### 5.9 小结

## 6 使用库算法

- 利用公用接口来提供一个标准算法集合

### 6.1 分析字符串

```C++
for (vector<string>::const_iterator it = bottom.begin(); it != bottom.end(); ++i)
	ret.push_back(*it);

ret.insert(ret.end(), bottom.begin(), bottom.end());

copy(bottom.begin(), bottom.end(), back_inserter(ret));
```

- copy 是一个泛型 (generic) 算法的例子
- back_inserter 是一个迭代器适配器的例子

```C++
copy(begin, end, out);
//equals to
while (begin != end)
	*out++ = *begin++;
	// equals to 
	// *out = *begin; ++out; ++begin;

it = begin++;
//equals to
it = begin;
++begin;
```

- 迭代器适配器是一个产生迭代器的东西

#### 6.1.1 另一个实现 split 的方法

```C++
bool space(char c) {
	return isspace(c);
}
bool not_space(char c) {
	return !isspace(c);
}
vector<string> split(const string& str) {
	typedef string::const_iterator iter;
	vector<string> ret;
	iter i = str.begin();
	while(i != str.end()) {
		i = find_if(i, str.end(), not_space);
		iter j = find_if(i, str.end(), space);
		if (i != str.end()) ret.push_back(string(i, j));
		i = j;	
	}
	return ret;
}
```

- 我们需要编写我们 space 和 not_space 是用来解释我们所指的是哪个版本的 isspace

#### 6.1.2 回文

```C++
bool is_palindrome(const string& s) {
	return equal(s.begin(), s.end(), s.rbegin());
}
```

#### 6.1.3 查找 URL

- protocol://resource-name

```C++
vector<string> find_urls(const string& s) {
	vector<string> ret;
	typedef string::const_iterator iter;
	iter b = s.begin(), e = s.end();
	while (b != e) {
		b = url_beg(b, e);
		if (b != e) {
			iter after = url_end(b, e);
			ret.push_back(string(b, after));
			b = after;
		}
	}
	return ret;
}

string::const_iterator url_end(string::const_iterator b, string::const_iterator e) {
	return find_if(b, e, not_url_char);
}

bool not_url_char(char c) {
	static const string url_ch = "~;/?@=&$-_.+!*{},'";
	return !(isalnum(c)) || find(url_ch.begin(), url_ch.end(), c) != url_end());
	//static声明的局部变量具有全局寿命，生存期贯穿整个函数调用过程
}

string::const_iterator url_beg(string::const_iterator b, string::const_iterator e) {
	static const string sep = "://";
	typedef string::const_iterator iter;
	iter i = b;
	while ((i = search(i, e, sep.begin(), sep.end())) != e) {
		if (i != b && i + sep.size() != e) {
			iter beg = i;
			while (beg != b && isalpha(beg[-1]))
				--beg;
			if (beg != i && i + sep.size() != e && !not_url_char(i[sep.size()])) return beg;
		}
		if (i != e) i += sep.size();
	}
	return e;
}
```

![QQ_1725714637254.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202409072110286.png)

### 6.2 对计算成绩的方案进行比较

1. 读所有的学生记录，把做了全部家庭作业的学生与其他的学生分隔开。
2. 对每一组中的所有学生分别使用每一个的计算成绩的方案，报告每一组的中值成绩。

#### 6.2.1 处理学生记录

```C++
bool did_all_hw(const Student_info& s) {
	reutrn ((fint(s.homework.begin(), s.homework.end(), 0)) == s.homework.end());
}

vector<Student_info> did, didnt;
Student_info student;

while (read(cin, student)) {
	if (did_all_hw(student))
		did.push_back(student);
	else
		didnt.push_back(student);
}
if (did.empty()) {
	cout << "No student did all the homework!" << endl;
	return 1;
}
if (didnt.empty()) {
	cout << "Every student did all the homework!" << endl;
	return 1;
}
```

#### 6.2.2 分析成绩

```C++
write_analysis(cout, "median", median_analysis, did, didn't);

double grade_aux(const Student_info& s) {
	tru {
		return grade(s);
	} catch (domain_error) {
		return grade(s.midterm, s.final, 0);
	}
}

double median_analysis(const vector<Student_info>& students) {
	vector<double> grades;
	transdorm(students.begin(), students.end(), back_inserter(grades), grade_aux);
	return medina(grades);
}

void write_analysis(ostream& out, const string& name, double analysis(const vector<Student_info>&), const vector<Student_info>& did, const vector<Student_info>& didnt) {
	out << name << ": median(did) = " << analysis(did) << ", median(didnt) = " << analysis(didnt) << endl; 
}

int main() {
	vector<Student_info> did, didnt;
	Student_info student;
	while (read(cin, student)) {
		if (did_all_hw(student))
			did.push_back(student);
		else 
			didnt.push_back(student);
	}
	if (did.empty()) {
 		cout << "No student did all the homework!" << endl;
 		return 1;
 	}
 	if (didnt.empty()) {
 		cout << "Every student did all the homework!" << endl;
 		return 1;
 	}
 	write_analysis(cout, "median", median_analysis, did, didnt);
 	write_analysis(cout, "average", average_analysis, did, didnt);
 	write_analysis(cout, "medina of homework turned in", optimistic_median_analysis, did, didnt);
 	return 0;
}
```

#### 6.2.3 计算基于家庭作业平均成绩的总成绩

```C++
double average(const vector<double>& v) {
	return accumulate(v.begin(), v.end(), 0.0) / v.size();
}

double average_analysis(const Student_info& s) {
	return grade(s.midterm, s.final, average(s.homework));
}

double average_analysis(const vector<Student_info>& students) {
	vector<double> grades;
	transform(students.begin(), students.end(), back_inserter(grades), average_grade);
	return median(grades);
}
```

#### 6.2.4 上交的家庭作业的中值

```C++
double optimistic_median(const Student_info& s) {
	vector<double> nonzero;
	remove_copy(s.homework.begin(), s.homework.end(), back_inserter(nonzero), 0);
	if (nonzero.empty())
		return grade(s.midterm, s.final, 0);
	else 
		return grade(s.midterm, s.final, median(nonzero));
}
```

### 6.3 对学生进行分类并回顾一下我们的问题

- 使用一些算法库来解决问题

#### 6.3.1 一种两次传递的解决方案

```C++
vector<Student_info> extract_fails(vector<Student_info>& students) {
	vector<Student_info> fail;
	remove_copy_if(students.begin(), students.end(), back_inserter(fail), pgrade);
	students.earse(remove_if(students.begin(), students.end(), fgrade), student.end());
	return fail;
}

bool pgrade(const Student_info& s) {
	return !fgrade(s);
}
```

### 6.4 一种一次传递的解决方案

```C++
vector<Student_info> extract_fails(vector<Student_info>& students) {
	vector<Student_info>::iterator iter = stable_partition(students.begin(), students.end(), pgrade);
	vector<Student_info> fail(iter, students.end());
	students.erase(iter, students.end());
	return fail;
}
```

### 6.5 算法、容器以及迭代器

- 算法作用于容器的元素，而不是作用于容器

## 7 使用关联容器

### 7.1 支持高效查找的容器

- 关联容器会对插入的元素进行排序来提高查找的速度
- 关联数组就是有 key-value 的数组
	- map: 映射表的索引不一定是整数

### 7.2 计算单词数

```C++
int main() {
	string s;
	map<string, int> counters;
	while (cin >> s) ++counters[s];
	for (map<string, int>::const_iterator it = counters.begin(); it != couners.end(); ++it) {
		cout << it->first << "\t" << it->second << endl;
	}
	return 0;
}
```

- 数对（pair）

### 7.3 产生一个交叉引用表

```C++
map<string, vector<int> > xref(istream& in, vector<string> find_words(const string&) = split) {
	string line;
	int line_number = 0'
	map<string, vector<int>> ret;
	while (getline(in, line)) {
		++line_number;
		vector<string> words = find_words(line);
		for (vector<string>::const_iterator it = words.begin(); it != words.end(); ++it)
			ret(*it).push_back(line_number);
	}
	return ret;
}


int main() {
	map<string, vector<int> > ret = cref(cin);
	for (map<string, vector<int> >::const_iterator it = ret.begin(); it != ret.end(); ++it) {
		cout << it->first << " occurs on line(s): ";
		vector<int>::const_iterator line_it = it->second.begin();
		cout << *lint_it;
		++line_it;
		while (line_it != it->second.end()) {
			cout << ", " << *line_it;
			++line_it;
		}
		cout << endl;
	}
	return 0;
}
```

### 7.4 生成句子

#### 7.4.1 表示规则

```C++
typedef vector<string> Rule;
typedef vector<Rule> Rule_collection;
typedef map<string, Rule_collection> Grammer;
```

#### 7.4.2 读入文法

```C++
Grammer read_grammer(istream& in) {
	Grammer ret;
	string line;
	while (getline(in, line)) {
		vector<string> entry = split(line);
		if (!entry.empty())
			ret[entry[0]].push_back(Rule(entry.begin() + 1, entry.end()));
	}
	return ret;
}
```

#### 7.4.3 生成句子

```C++
vector<string> gen_sentence(const Grammar& g) {
	vector<string> ret;
	gen_aux(g, "<sentence>", ret);
	return ret;
}

bool bracketed(const string& s) {
	return s.size() > 1 && s[0] == '<' && s[s.size() - 1] == '>';
}

void gen_aux(const Grammar& g, const string& word, vector<string>& ret) {
	if (!bracketed(word)) {
		ret.push_back(word);
	} else {
		Grammar::const_iterator it = g.find(word);
		if (it == g.end())
			throw logic_error("empty rule");
		const Rule_collection& c = it->seond;
		const Rule& r = c[nrand(c.size())];
		for (Rule::const_iterator i = r.begin(); i != r.end(); ++i)
			gen_aux(g, *i, ret);
	}
}

int main() {
	vector<string> sentence = gen_sentence(read_grammar(cin));
	vector<string>::const_iterator it = sentence.begin();
	if (!sentence.empty()) {
		cout << *it;
		++it;	
	}
	while (it != sentence.end()) {
		cout << " " << *it;
		++it;
	}
	cout << endl;
	return 0;
}
```

#### 7.4.4 选择一个随机函数

```C++
int nrand(int n) {
	if (n <= 0 || n > RAND_MAX)
		throw domain_error("Argument to nrand is out of range");
	const int bucket_size = RAND_MAX / n;
	int r;
	do r = rand() / bucket_size;
	while (r >= n);
	return r;
}
```

### 7.5 关于性能的一点说明

- 用散列表实现关联数组在 C++中的是很困难的  
没搞懂  
![QQ_1725724878262.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202409080002875.png)

### 7.6 小结

## 8 编写泛型函数

### 8.1 泛型函数是什么

- 在使用函数之前不知道参数或者返回类型是什么

#### 8.1.1 未知类型的中值

- 实现了泛型函数的语言特征被称作模板函数

## 9 定义新类型

## 10 管理内存和低级数据结构

## 11 定义抽象数据类型

## 12 使类对象像一个数值一样工作

## 13 使用继承与动态绑定

## 14 近乎自动地管理内存

## 15 再谈字符图形

## 16 今后如何学习 C++
