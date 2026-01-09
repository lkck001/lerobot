#!/usr/bin/env python
"""
详细解释两个关键问题：
1. 为什么 @RobotConfig.register_subclass("so101") 要写在类上面？
2. subclass 是什么？
"""

print("="*70)
print("问题1: 为什么装饰器要写在类上面？")
print("="*70)

# ============================================
# 装饰器的本质
# ============================================
print("\n【装饰器的本质】")
print("-" * 70)

def my_decorator(something):
    print(f"  🎁 装饰器收到: {something}")
    return something

# 方式1：使用 @ 语法
@my_decorator
class MyClass1:
    pass

print("\n上面的代码等价于：")
print("""
class MyClass1:
    pass
MyClass1 = my_decorator(MyClass1)  # ← 装饰器就是函数调用
""")

# ============================================
# 位置为什么重要
# ============================================
print("\n【为什么位置重要】")
print("-" * 70)
print("""
Python 从上往下执行代码：

第1步：读到装饰器
@my_decorator        ← Python: "哦，有个装饰器"
                     ← Python: "我先记住它"

第2步：读到类定义
class MyClass:       ← Python: "创建这个类"
    pass             ← Python: "创建完成"

第3步：应用装饰器
                     ← Python: "现在用装饰器包装这个类"
                     ← 执行: MyClass = my_decorator(MyClass)

所以装饰器必须在上面，因为 Python 需要先知道要用什么装饰器！
""")

# 错误示例
print("❌ 错误示例（不能这样写）：")
print("""
class MyClass:        # 如果类在上面
    pass
@my_decorator         # 装饰器在下面

这不是有效的 Python 语法！
""")

input("\n按回车继续...")

# ============================================
print("\n\n" + "="*70)
print("问题2: subclass 是什么？")
print("="*70)

print("\n【subclass = 子类】")
print("-" * 70)
print("""
subclass 是英文，中文叫\"子类\"
这是面向对象编程中的继承关系

继承关系示例：

    Animal          ← 父类 (Parent Class / Super Class / Base Class)
      ↓ 继承
    ┌─┴─┐
    │   │
   Dog Cat          ← 子类 (Child Class / Sub Class / Derived Class)

说法：
  - Dog 是 Animal 的子类 (Dog is a subclass of Animal)
  - Animal 是 Dog 的父类 (Animal is a superclass of Dog)
""")

# ============================================
# 代码示例
# ============================================
print("\n【代码示例】")
print("-" * 70)

# 父类
class Animal:
    def eat(self):
        return "吃东西"

# 子类1
class Dog(Animal):  # ← Dog 继承 Animal，所以 Dog 是 Animal 的子类
    def bark(self):
        return "汪汪"

# 子类2
class Cat(Animal):  # ← Cat 继承 Animal，所以 Cat 是 Animal 的子类
    def meow(self):
        return "喵喵"

print("继承关系图：")
print("""
    Animal (父类)
      ↓
    ┌─┴─┐
    │   │
   Dog Cat (子类)
""")

# 验证
print("\n验证继承关系：")
print(f"  Dog 是 Animal 的子类吗？ {issubclass(Dog, Animal)}")  # True
print(f"  Cat 是 Animal 的子类吗？ {issubclass(Cat, Animal)}")  # True
print(f"  Dog 是 Cat 的子类吗？ {issubclass(Dog, Cat)}")  # False

input("\n按回车继续...")

# ============================================
print("\n\n" + "="*70)
print("把两个概念结合起来")
print("="*70)

print("\n【register_subclass 的含义】")
print("-" * 70)
print("""
register_subclass 拆分：
  register  = 注册
  subclass  = 子类

完整含义：注册子类

为什么叫\"注册子类\"？
因为我们要注册的是 RobotConfig 的子类！
""")

# ============================================
# 完整示例
# ============================================
print("\n【完整示例】")
print("-" * 70)

class RobotConfig:
    """父类"""
    _registry = {}
    
    @classmethod
    def register_subclass(cls, name):
        """注册子类的装饰器"""
        print(f"\n  📝 准备注册子类，名字='{name}'")
        
        def decorator(subclass):
            # subclass 参数就是被装饰的类
            print(f"     收到类: {subclass.__name__}")
            print(f"     这个类是 RobotConfig 的子类吗？ {issubclass(subclass, RobotConfig)}")
            
            cls._registry[name] = subclass
            print(f"     ✅ 注册成功")
            return subclass
        return decorator

print("\n现在注册子类：")

# 注册子类1
@RobotConfig.register_subclass("so101")  # ← 装饰器在上面
class SO101Config(RobotConfig):           # ← 子类在下面
    """SO101 机器人配置 - 这是 RobotConfig 的子类"""
    pass

# 注册子类2
@RobotConfig.register_subclass("so100")
class SO100Config(RobotConfig):
    """SO100 机器人配置 - 这是 RobotConfig 的子类"""
    pass

print("\n" + "-" * 70)
print("注册表内容：")
for name, cls in RobotConfig._registry.items():
    print(f"  '{name}' -> {cls.__name__}")

input("\n按回车继续...")

# ============================================
print("\n\n" + "="*70)
print("图解说明")
print("="*70)

print("""
代码：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    @RobotConfig.register_subclass("so101")  ← 装饰器（必须在上）
    class SO101Config(RobotConfig):          ← 类定义（必须在下）
        pass

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

执行过程：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

步骤1: Python 读到装饰器
    @RobotConfig.register_subclass("so101")
    ↓
    调用 register_subclass("so101")
    ↓
    返回 decorator 函数
    ↓
    Python: "好的，我记住了这个装饰器"

步骤2: Python 读到类定义
    class SO101Config(RobotConfig):
        pass
    ↓
    创建类 SO101Config
    ↓
    注意：SO101Config 继承 RobotConfig
    ↓
    所以 SO101Config 是 RobotConfig 的子类 ✓

步骤3: Python 应用装饰器
    decorator(SO101Config)
    ↓
    检查：SO101Config 是 RobotConfig 的子类吗？ ✓
    ↓
    注册：_registry["so101"] = SO101Config
    ↓
    返回 SO101Config

步骤4: 完成
    SO101Config 已经注册到注册表中

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

继承关系：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    RobotConfig                 ← 父类 (Parent/Super/Base Class)
         ↓
    ┌────┼────┐
    │    │    │
SO101  SO100  Koch              ← 子类 (Child/Sub/Derived Class)
Config Config Config

每个子类都通过 register_subclass 注册到父类的注册表中

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print("\n" + "="*70)
print("关键总结")
print("="*70)
print("""
1️⃣ 装饰器位置
   ✅ 必须写在类上面
   ❌ 不能写在类下面
   原因：Python 从上往下执行，需要先知道装饰器

2️⃣ subclass 的含义
   subclass = 子类
   是继承关系中的概念
   SO101Config(RobotConfig) ← SO101Config 是子类
                            ← RobotConfig 是父类

3️⃣ register_subclass
   register = 注册
   subclass = 子类
   完整含义：注册子类到注册表中

4️⃣ 位置关系
   @RobotConfig.register_subclass("so101")  ← 装饰器在上
   class SO101Config(RobotConfig):          ← 被装饰的类在下
       pass

   这是 Python 的语法规则，必须这样写！
""")

print("="*70)

