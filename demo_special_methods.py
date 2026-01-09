"""
Python 特殊方法（魔术方法）详解
================================
演示 __repr__, __eq__ 等特殊方法的作用
"""

print("\n" + "="*70)
print("【核心概念】Python 的特殊方法")
print("="*70)
print("""
特殊方法是 Python 中以双下划线开头和结尾的方法，例如 __init__, __repr__, __eq__
它们被 Python 解释器在特定情况下自动调用
""")

print("\n" + "="*70)
print("【实验1】__init__() - 这才是初始化方法")
print("="*70)

class Person:
    def __init__(self, name: str, age: int):
        """当你创建对象时，这个方法会被自动调用"""
        print(f"  ⚙️ __init__ 被调用了！正在初始化对象...")
        self.name = name
        self.age = age
        print(f"  ✓ 初始化完成：name={name}, age={age}")

print("创建 Person 对象：")
p = Person("张三", 25)
print(f"对象创建完毕\n")


print("="*70)
print("【实验2】__repr__() - 对象的字符串表示")
print("="*70)
print("""
__repr__() 决定了当你打印对象或在交互式环境中查看对象时显示什么内容
""")

# 没有 __repr__ 的类
class PersonWithoutRepr:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

# 有 __repr__ 的类
class PersonWithRepr:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def __repr__(self):
        """这个方法返回对象的字符串表示"""
        return f"PersonWithRepr(name={self.name}, age={self.age})"

p1 = PersonWithoutRepr("李四", 30)
p2 = PersonWithRepr("李四", 30)

print(f"没有 __repr__: {p1}")
print(f"  ❌ 输出像 <__main__.PersonWithoutRepr object at 0x...>，不友好")
print()
print(f"有 __repr__:   {p2}")
print(f"  ✅ 输出清晰易读的信息")


print("\n" + "="*70)
print("【实验3】__eq__() - 对象的相等性比较")
print("="*70)
print("""
__eq__() 决定了两个对象如何比较是否相等（使用 == 运算符时）
""")

# 没有 __eq__ 的类
class PersonWithoutEq:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def __repr__(self):
        return f"PersonWithoutEq(name={self.name}, age={self.age})"

# 有 __eq__ 的类
class PersonWithEq:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def __repr__(self):
        return f"PersonWithEq(name={self.name}, age={self.age})"
    
    def __eq__(self, other):
        """这个方法定义了如何比较两个对象是否相等"""
        if not isinstance(other, PersonWithEq):
            return False
        return self.name == other.name and self.age == other.age

# 测试没有 __eq__ 的类
p3 = PersonWithoutEq("王五", 28)
p4 = PersonWithoutEq("王五", 28)

print(f"p3 = {p3}")
print(f"p4 = {p4}")
print(f"p3 == p4: {p3 == p4}")
print(f"  ❌ 虽然内容相同，但返回 False（因为是不同的对象）")
print(f"  默认比较的是对象的内存地址: id(p3)={id(p3)}, id(p4)={id(p4)}")
print()

# 测试有 __eq__ 的类
p5 = PersonWithEq("王五", 28)
p6 = PersonWithEq("王五", 28)

print(f"p5 = {p5}")
print(f"p6 = {p6}")
print(f"p5 == p6: {p5 == p6}")
print(f"  ✅ 返回 True（因为我们定义了比较规则：比较 name 和 age）")


print("\n" + "="*70)
print("【实验4】__eq__() 的内部逻辑详解")
print("="*70)

class PersonDetailed:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def __repr__(self):
        return f"Person(name='{self.name}', age={self.age})"
    
    def __eq__(self, other):
        """带详细输出的 __eq__ 方法"""
        print(f"    🔍 __eq__ 被调用: 比较 {self} 和 {other}")
        
        # 第1步：检查类型
        if not isinstance(other, PersonDetailed):
            print(f"    ❌ 类型不同，返回 False")
            return False
        
        # 第2步：比较属性
        name_match = self.name == other.name
        age_match = self.age == other.age
        
        print(f"    - name 匹配: {name_match} ({self.name} == {other.name})")
        print(f"    - age 匹配: {age_match} ({self.age} == {other.age})")
        
        result = name_match and age_match
        print(f"    ✓ 最终结果: {result}")
        return result

print("比较两个相同的人：")
p7 = PersonDetailed("赵六", 35)
p8 = PersonDetailed("赵六", 35)
result1 = (p7 == p8)
print(f"结果: {result1}\n")

print("比较两个不同的人：")
p9 = PersonDetailed("赵六", 35)
p10 = PersonDetailed("赵六", 36)  # 年龄不同
result2 = (p9 == p10)
print(f"结果: {result2}\n")

print("与字符串比较：")
p11 = PersonDetailed("孙七", 40)
result3 = (p11 == "孙七")
print(f"结果: {result3}")


print("\n" + "="*70)
print("【实验5】@dataclass 自动生成这些方法")
print("="*70)

from dataclasses import dataclass

@dataclass
class PersonDataclass:
    name: str
    age: int
    # @dataclass 自动生成了：
    # - __init__(self, name, age)
    # - __repr__(self)
    # - __eq__(self, other)
    # 不需要手动编写！

print("使用 @dataclass 创建的类自动拥有这些方法：")
p12 = PersonDataclass("周八", 45)
p13 = PersonDataclass("周八", 45)

print(f"\n自动的 __repr__: {p12}")
print(f"自动的 __eq__: p12 == p13 = {p12 == p13}")


print("\n" + "="*70)
print("【实验6】其他常用特殊方法")
print("="*70)

class Money:
    def __init__(self, amount: float):
        self.amount = amount
    
    def __repr__(self):
        return f"Money({self.amount}元)"
    
    def __add__(self, other):
        """定义 + 运算符的行为"""
        if isinstance(other, Money):
            return Money(self.amount + other.amount)
        return NotImplemented
    
    def __lt__(self, other):
        """定义 < 运算符的行为"""
        if isinstance(other, Money):
            return self.amount < other.amount
        return NotImplemented
    
    def __len__(self):
        """定义 len() 函数的行为（这里演示用，返回金额的整数部分）"""
        return int(self.amount)

m1 = Money(100)
m2 = Money(50)

print(f"m1 = {m1}")
print(f"m2 = {m2}")
print(f"m1 + m2 = {m1 + m2}  # 调用 __add__")
print(f"m1 < m2 = {m1 < m2}  # 调用 __lt__")
print(f"len(m1) = {len(m1)}  # 调用 __len__")


print("\n" + "="*70)
print("【总结】特殊方法的作用")
print("="*70)
print("""
┌──────────────┬────────────────────────┬─────────────────────────┐
│ 特殊方法     │ 何时被调用             │ 作用                    │
├──────────────┼────────────────────────┼─────────────────────────┤
│ __init__     │ 创建对象时             │ 初始化对象属性          │
│ __repr__     │ print(obj) 或 str(obj) │ 返回对象的字符串表示    │
│ __eq__       │ obj1 == obj2           │ 比较两个对象是否相等    │
│ __lt__       │ obj1 < obj2            │ 比较对象大小            │
│ __add__      │ obj1 + obj2            │ 定义加法运算            │
│ __len__      │ len(obj)               │ 返回对象的长度          │
│ __getitem__  │ obj[key]               │ 支持索引访问            │
│ __call__     │ obj()                  │ 让对象可以像函数调用    │
└──────────────┴────────────────────────┴─────────────────────────┘

🎯 关键理解：
1. __init__() 是初始化方法，创建对象时调用
2. __repr__() 和 __eq__() 不是初始化方法，是其他功能的方法
3. 这些特殊方法让你的类可以使用 Python 的内置操作符和函数
4. @dataclass 自动帮你生成最常用的特殊方法，省去手工编写
""")

print("\n" + "="*70)
print("实验完成！")
print("="*70)

