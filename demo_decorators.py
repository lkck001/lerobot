#!/usr/bin/env python
"""
演示 @classmethod 和 @property 的区别
"""

print("="*60)
print("演示1：普通方法 vs @classmethod vs @property")
print("="*60)

class Person:
    # 类变量（所有实例共享）
    total_count = 0
    
    def __init__(self, name, birth_year):
        self.name = name
        self.birth_year = birth_year
        Person.total_count += 1
    
    # ========================================
    # 普通方法：需要实例 + 括号
    # ========================================
    def say_hello(self):
        """普通方法：需要 self，操作实例数据"""
        return f"你好，我是 {self.name}"
    
    # ========================================
    # @property：像访问变量一样，不需要括号
    # ========================================
    @property
    def age(self):
        """动态属性：每次访问时计算"""
        return 2025 - self.birth_year
    
    @property
    def info(self):
        """动态属性：组合多个信息"""
        return f"{self.name}，{self.age}岁"
    
    # ========================================
    # @classmethod：不需要实例，可以直接用类调用
    # ========================================
    @classmethod
    def get_total_count(cls):
        """类方法：访问类级别的数据"""
        return cls.total_count
    
    @classmethod
    def create_baby(cls, name):
        """类方法：工厂方法，创建特定实例"""
        return cls(name, 2025)


# ============================================
# 测试普通方法
# ============================================
print("\n【普通方法】")
person1 = Person("张三", 1990)

# 需要实例 + 括号
result = person1.say_hello()
print(f"调用: person1.say_hello()")
print(f"结果: {result}")

# 错误示例：
try:
    Person.say_hello()  # ❌ 不能直接用类调用
except TypeError as e:
    print(f"❌ Person.say_hello() 报错: {e}")


# ============================================
# 测试 @property
# ============================================
print("\n【@property 动态属性】")

# 像访问变量一样，不需要括号
print(f"访问: person1.age")
print(f"结果: {person1.age}")  # 不需要 ()

print(f"\n访问: person1.info")
print(f"结果: {person1.info}")  # 不需要 ()

# 对比：如果没有 @property
print("\n如果没有 @property，需要这样：")
print(f"person1.age()  ← 需要括号")
print(f"但有了 @property：")
print(f"person1.age    ← 不需要括号，像变量一样")


# ============================================
# 测试 @classmethod
# ============================================
print("\n【@classmethod 类方法】")

# 不需要实例，直接用类调用
print(f"调用: Person.get_total_count()")
print(f"结果: {Person.get_total_count()}")

# 也可以用实例调用（但通常不这么做）
print(f"\n也可以用实例调用: person1.get_total_count()")
print(f"结果: {person1.get_total_count()}")

# 工厂方法示例
print("\n使用类方法创建实例：")
baby = Person.create_baby("小明")
print(f"调用: Person.create_baby('小明')")
print(f"结果: {baby.info}")


# ============================================
# 在 draccus 中的应用
# ============================================
print("\n" + "="*60)
print("在 draccus/RobotConfig 中的应用")
print("="*60)

class RobotConfig:
    _registry = {}  # 注册表（类级别）
    
    # @classmethod：因为要访问类级别的 _registry
    @classmethod
    def register_subclass(cls, name):
        """类方法：不需要实例就能注册"""
        def decorator(subclass):
            cls._registry[name] = subclass
            subclass._choice_name = name
            return subclass
        return decorator
    
    # @classmethod：因为要查找类级别的 _registry
    @classmethod
    def get_subclass_by_name(cls, name):
        """类方法：不需要实例就能查找"""
        return cls._registry.get(name)
    
    def __init__(self, port):
        self.port = port
    
    # @property：因为想让 type 像普通属性一样访问
    @property
    def type(self):
        """动态属性：不需要括号就能访问"""
        return self.__class__._choice_name


@RobotConfig.register_subclass("so101")
class SO101Config(RobotConfig):
    pass


print("\n为什么用 @classmethod？")
print("-" * 40)
print("1. register_subclass() 需要访问 _registry（类变量）")
print("   → 不需要实例，直接用类调用")
print("   → RobotConfig.register_subclass('so101')")

print("\n2. get_subclass_by_name() 需要查找 _registry")
print("   → 不需要实例，直接用类调用")
print("   → RobotConfig.get_subclass_by_name('so101')")

print("\n为什么用 @property？")
print("-" * 40)
print("1. type 是一个计算出来的值，不是存储的变量")
print("2. 但我们希望像访问变量一样使用它")
print("   → robot.type（不需要括号）")
print("   → 而不是 robot.get_type()（需要括号）")

# 演示
robot = SO101Config(port="COM24")
print("\n实际使用：")
print(f"robot.type = '{robot.type}'  ← 像访问变量")
print(f"不是: robot.type() ← 不需要括号")


# ============================================
# 总结
# ============================================
print("\n" + "="*60)
print("总结")
print("="*60)
print("""
1. 普通方法：
   - 需要实例才能调用
   - 需要括号: obj.method()
   
2. @classmethod：
   - 不需要实例，直接用类调用
   - 第一个参数是 cls（类本身）
   - 用于访问/修改类级别的数据
   - 调用: MyClass.class_method()
   
3. @property：
   - 让方法变成属性
   - 不需要括号: obj.property
   - 用于动态计算的值
   - 让代码更简洁易读
""")

