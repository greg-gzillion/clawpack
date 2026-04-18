# CodeClaw - Python Reference

## Overview
Python is a high-level, interpreted, general-purpose programming language known for its readability and versatility.

| Attribute | Value |
|-----------|-------|
| **First Released** | 1991 |
| **Designed By** | Guido van Rossum |
| **Typing** | Dynamic, Strong, Duck typing |
| **Paradigm** | Multi-paradigm (OOP, Functional, Procedural) |
| **File Extensions** | `.py`, `.pyc`, `.pyo`, `.pyd` |
| **Official Website** | https://www.python.org |
| **Package Manager** | pip, conda, poetry |
| **Current Stable** | Python 3.12+ |

## Key Features
- **Readable Syntax**: Uses indentation for code blocks
- **Interpreted**: No compilation step required
- **Dynamically Typed**: Variables don't need type declarations
- **Extensive Standard Library**: "Batteries included"
- **Garbage Collected**: Automatic memory management
- **Cross-Platform**: Runs on Windows, macOS, Linux

## Basic Syntax

### Variables and Data Types
```python
# Numbers
age = 25                # int
price = 19.99           # float
complex_num = 3 + 4j    # complex

# Strings
name = "Alice"          # str
multi = """Multiple
lines"""                # multiline str

# Booleans
is_valid = True         # bool
is_empty = False

# Collections
numbers = [1, 2, 3]     # list (mutable)
point = (10, 20)        # tuple (immutable)
unique = {1, 2, 3}      # set
person = {"name": "Alice", "age": 25}  # dict

# Type checking
print(type(age))        # <class 'int'>
# If-elif-else
if age >= 18:
    print("Adult")
elif age >= 13:
    print("Teen")
else:
    print("Child")

# Loops
for item in numbers:           # for loop
    print(item)

while age > 0:                 # while loop
    print(age)
    age -= 1

# List comprehension
squares = [x**2 for x in range(10)]  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# Match-case (Python 3.10+)
match status:
    case 200:
        print("OK")
    case 404:
        print("Not Found")
    case _:
        print("Unknown")
# Basic function
def greet(name):
    return f"Hello, {name}!"

# Default parameters
def power(base, exponent=2):
    return base ** exponent

# Variable arguments
def sum_all(*args):
    return sum(args)

# Keyword arguments
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

# Lambda functions
square = lambda x: x ** 2

# Type hints (Python 3.5+)
def add(a: int, b: int) -> int:
    return a + b
class Person:
    # Class attribute
    species = "Homo sapiens"
    
    # Constructor
    def __init__(self, name: str, age: int):
        self.name = name      # Instance attribute
        self.age = age
        self._protected = 0   # Protected (convention)
        self.__private = 0    # Private (name mangling)
    
    # Instance method
    def greet(self) -> str:
        return f"Hello, I'm {self.name}"
    
    # Class method
    @classmethod
    def create_anonymous(cls):
        return cls("Anonymous", 0)
    
    # Static method
    @staticmethod
    def is_adult(age: int) -> bool:
        return age >= 18
    
    # Property decorator
    @property
    def info(self) -> str:
        return f"{self.name}, {self.age}"
    
    # Dunder methods
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f"Person(name='{self.name}', age={self.age})"

# Inheritance
class Student(Person):
    def __init__(self, name: str, age: int, student_id: str):
        super().__init__(name, age)
        self.student_id = student_id
    
    def greet(self) -> str:  # Override
        return f"{super().greet()} (Student #{self.student_id})"
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")
except (ValueError, TypeError) as e:
    print(f"Multiple errors: {e}")
except Exception as e:
    print(f"Catch all: {e}")
else:
    print("No error occurred")
finally:
    print("Always executes")

# Custom exception
class CustomError(Exception):
    pass

# Raise exception
raise CustomError("Something went wrong")

# Context manager (with statement)
with open("file.txt", "r") as f:
    content = f.read()
# Reading
with open("file.txt", "r") as f:
    content = f.read()          # Read entire file
    lines = f.readlines()       # Read all lines

with open("file.txt", "r") as f:
    for line in f:              # Iterate lines
        print(line.strip())

# Writing
with open("output.txt", "w") as f:
    f.write("Hello, World!\n")
    f.writelines(["Line 1\n", "Line 2\n"])

# Appending
with open("output.txt", "a") as f:
    f.write("Appended line\n")

# Binary mode
with open("image.jpg", "rb") as f:
    data = f.read()
# OS operations
import os
os.path.exists("file.txt")
os.listdir(".")
os.mkdir("new_dir")

# System
import sys
print(sys.argv)          # Command line arguments
sys.exit(0)              # Exit program

# JSON
import json
data = {"name": "Alice", "age": 25}
json_str = json.dumps(data)
parsed = json.loads(json_str)

with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

# DateTime
from datetime import datetime, timedelta
now = datetime.now()
future = now + timedelta(days=7)
print(now.strftime("%Y-%m-%d %H:%M:%S"))

# Regular Expressions
import re
pattern = r"\d+"
match = re.search(pattern, "Age: 25")
if match:
    print(match.group())  # 25

# Math
import math
math.sqrt(16)    # 4.0
math.pi          # 3.14159...

# Random
import random
random.randint(1, 10)
random.choice(["a", "b", "c"])
# Threading
import threading
import time

def worker(name):
    print(f"Thread {name} starting")
    time.sleep(2)
    print(f"Thread {name} done")

threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# Async/Await (Python 3.5+)
import asyncio

async def fetch_data():
    await asyncio.sleep(1)
    return "data"

async def main():
    result = await fetch_data()
    print(result)
    
    # Concurrent execution
    results = await asyncio.gather(
        fetch_data(),
        fetch_data(),
        fetch_data()
    )

asyncio.run(main())

# Multiprocessing
from multiprocessing import Pool

def square(x):
    return x ** 2

with Pool(4) as p:
    results = p.map(square, [1, 2, 3, 4, 5])
# pip (standard)
pip install requests
pip install -r requirements.txt
pip freeze > requirements.txt
pip uninstall requests

# virtual environment
python -m venv myenv
source myenv/bin/activate  # Linux/Mac
myenv\Scripts\activate     # Windows
deactivate

# poetry (modern)
poetry new myproject
poetry add requests
poetry install
poetry shell
// Variable declarations
var oldWay = "avoid";           // Function-scoped, hoisted
let mutable = "can change";     // Block-scoped
const constant = "cannot change"; // Block-scoped, immutable reference

// Primitives
let num = 42;                   // number
let str = "Hello";              // string (also 'Hello' or `Hello`)
let bool = true;                // boolean
let nothing = null;             // null (intentional absence)
let notDefined = undefined;     // undefined (unintentional)
let bigInt = 9007199254740991n; // BigInt (ES2020)
let sym = Symbol("unique");     // Symbol (ES6)

// Objects
let obj = { name: "Alice", age: 25 };
let arr = [1, 2, 3, 4, 5];
let date = new Date();
let regex = /pattern/g;

// Template literals (ES6)
let greeting = `Hello, ${obj.name}! You are ${obj.age} years old.`;

// Type checking
console.log(typeof num);        // "number"
console.log(Array.isArray(arr)); // true
// If-else
if (age >= 18) {
    console.log("Adult");
} else if (age >= 13) {
    console.log("Teen");
} else {
    console.log("Child");
}

// Ternary operator
let status = age >= 18 ? "Adult" : "Minor";

// Switch
switch (day) {
    case 1:
        console.log("Monday");
        break;
    case 2:
        console.log("Tuesday");
        break;
    default:
        console.log("Other day");
}

// Loops
for (let i = 0; i < 5; i++) { }                    // Traditional for
for (let item of arr) { }                           // for...of (values)
for (let key in obj) { }                            // for...in (keys)
while (condition) { }                               // while
do { } while (condition);                           // do...while

// Array methods
arr.forEach(item => console.log(item));
let doubled = arr.map(x => x * 2);
let evens = arr.filter(x => x % 2 === 0);
let sum = arr.reduce((acc, x) => acc + x, 0);
# Continue with more languages...

# 5. JAVA
@'
# CodeClaw - Java Reference

## Overview
Java is a high-level, class-based, object-oriented programming language designed to have as few implementation dependencies as possible.

| Attribute | Value |
|-----------|-------|
| **First Released** | 1995 |
| **Designed By** | James Gosling (Sun Microsystems) |
| **Typing** | Static, Strong, Nominal |
| **Paradigm** | Object-oriented, Concurrent |
| **File Extensions** | `.java`, `.class`, `.jar` |
| **Official Website** | https://www.oracle.com/java/ |
| **Package Manager** | Maven, Gradle |
| **Current LTS** | Java 21 |

## Key Features
- **Platform Independent**: "Write Once, Run Anywhere" (JVM)
- **Object-Oriented**: Everything is a class
- **Robust**: Strong memory management, Exception handling
- **Multithreaded**: Built-in concurrency support
- **Secure**: Bytecode verification, Security manager
- **Large Ecosystem**: Extensive libraries and frameworks

## Basic Syntax

### Hello World
```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
// Primitives
byte b = 127;              // 8-bit
short s = 32767;           // 16-bit
int i = 2147483647;        // 32-bit
long l = 9223372036854775807L; // 64-bit (note L)
float f = 3.14f;           // 32-bit (note f)
double d = 3.14159;        // 64-bit
char c = 'A';              // 16-bit Unicode
boolean bool = true;       // true/false

// Reference types
String str = "Hello";
Integer num = 42;          // Wrapper class
int[] arr = {1, 2, 3, 4, 5};
int[][] matrix = {{1, 2}, {3, 4}};

// Type casting
double d2 = 42.5;
int i2 = (int) d2;         // Explicit casting

// Constants (final)
final double PI = 3.14159;
// If-else
if (age >= 18) {
    System.out.println("Adult");
} else if (age >= 13) {
    System.out.println("Teen");
} else {
    System.out.println("Child");
}

// Switch (traditional)
switch (day) {
    case 1:
        System.out.println("Monday");
        break;
    default:
        System.out.println("Other");
}

// Switch expression (Java 14+)
String result = switch (day) {
    case 1 -> "Monday";
    case 2 -> "Tuesday";
    default -> "Other";
};

// Loops
for (int j = 0; j < 5; j++) { }
for (int num : arr) { }          // Enhanced for
while (condition) { }
do { } while (condition);
public class Calculator {
    // Basic method
    public int add(int a, int b) {
        return a + b;
    }
    
    // Method overloading
    public double add(double a, double b) {
        return a + b;
    }
    
    // Varargs
    public int sum(int... numbers) {
        int total = 0;
        for (int n : numbers) total += n;
        return total;
    }
    
    // Static method
    public static void print(String msg) {
        System.out.println(msg);
    }
}
// Class
public class Person {
    // Fields
    private String name;
    private int age;
    
    // Static field
    public static String species = "Homo sapiens";
    
    // Constructor
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    // Default constructor
    public Person() {
        this("Unknown", 0);
    }
    
    // Getters and Setters
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }
    
    // Method
    public void greet() {
        System.out.println("Hello, I'm " + name);
    }
    
    // toString override
    @Override
    public String toString() {
        return "Person{name='" + name + "', age=" + age + "}";
    }
}

// Inheritance
public class Student extends Person {
    private String studentId;
    
    public Student(String name, int age, String studentId) {
        super(name, age);
        this.studentId = studentId;
    }
    
    @Override
    public void greet() {
        System.out.println("Hello, I'm " + getName() + 
                          " (Student #" + studentId + ")");
    }
}

// Abstract class
public abstract class Shape {
    public abstract double getArea();
}

// Interface
public interface Drawable {
    void draw();
    
    // Default method (Java 8+)
    default void print() {
        System.out.println("Printing...");
    }
    
    // Static method (Java 8+)
    static void info() {
        System.out.println("Drawable interface");
    }
}

// Record (Java 14+)
public record Point(int x, int y) {
    // Compact constructor
    public Point {
        if (x < 0 || y < 0) {
            throw new IllegalArgumentException("Negative coordinates");
        }
    }
}
try {
    int result = 10 / 0;
} catch (ArithmeticException e) {
    System.out.println("Error: " + e.getMessage());
} catch (Exception e) {
    System.out.println("Catch all");
} finally {
    System.out.println("Always executes");
}

// Try-with-resources (Java 7+)
try (FileReader fr = new FileReader("file.txt");
     BufferedReader br = new BufferedReader(fr)) {
    String line = br.readLine();
} catch (IOException e) {
    e.printStackTrace();
}

// Custom exception
public class CustomException extends Exception {
    public CustomException(String message) {
        super(message);
    }
}

// Throw exception
throw new CustomException("Something went wrong");
import java.util.*;

// List
List<String> list = new ArrayList<>();
list.add("Apple");
list.add("Banana");
list.get(0);
list.remove(1);
for (String item : list) { }

// Set
Set<Integer> set = new HashSet<>();
set.add(1);
set.add(2);
set.contains(1);

// Map
Map<String, Integer> map = new HashMap<>();
map.put("Alice", 25);
map.get("Alice");
for (Map.Entry<String, Integer> entry : map.entrySet()) {
    System.out.println(entry.getKey() + ": " + entry.getValue());
}

// Queue
Queue<String> queue = new LinkedList<>();
queue.offer("First");
queue.poll();

// Stack (use Deque instead)
Deque<String> stack = new ArrayDeque<>();
stack.push("Bottom");
stack.push("Top");
stack.pop();
import java.util.stream.*;

// Creating streams
Stream<Integer> stream = list.stream();
IntStream intStream = IntStream.range(1, 10);

// Operations
List<String> filtered = list.stream()
    .filter(s -> s.startsWith("A"))
    .map(String::toUpperCase)
    .sorted()
    .collect(Collectors.toList());

// Reduction
int sum = IntStream.range(1, 101).sum();
Optional<Integer> max = list.stream().max(Integer::compare);

// Parallel streams
list.parallelStream().forEach(System.out::println);
// Thread
Thread thread = new Thread(() -> {
    System.out.println("Running");
});
thread.start();
thread.join(); // Wait for completion

// ExecutorService
ExecutorService executor = Executors.newFixedThreadPool(4);
Future<String> future = executor.submit(() -> "Result");
String result = future.get();
executor.shutdown();

// CompletableFuture
CompletableFuture<String> cf = CompletableFuture
    .supplyAsync(() -> "Hello")
    .thenApply(s -> s + " World")
    .thenAccept(System.out::println);
import java.nio.file.*;

// Reading
String content = Files.readString(Path.of("file.txt"));
List<String> lines = Files.readAllLines(Path.of("file.txt"));

// Writing
Files.writeString(Path.of("output.txt"), "Hello, World!");
Files.write(Path.of("output.txt"), lines);

// Directory operations
Files.createDirectory(Path.of("newdir"));
Files.list(Path.of(".")).forEach(System.out::println);
Files.walk(Path.of(".")).forEach(System.out::println);
<project>
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0.0</version>
    
    <properties>
        <maven.compiler.source>21</maven.compiler.source>
        <maven.compiler.target>21</maven.compiler.target>
    </properties>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>3.2.0</version>
        </dependency>
    </dependencies>
</project>
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
package main

import "fmt"

func main() {
    // Variable declarations
    var name string = "Alice"
    var age int = 25
    var height float64 = 5.8
    var isStudent bool = true
    
    // Type inference
    city := "New York"        // Short declaration
    count := 42
    
    // Multiple declarations
    var x, y int = 10, 20
    a, b := "hello", 123
    
    // Constants
    const PI = 3.14159
    const (
        StatusOK = 200
        StatusNotFound = 404
    )
    
    // Basic types
    var (
        b bool = true
        s string = "hello"
        i int = 42
        i8 int8 = 127
        i16 int16 = 32767
        i32 int32 = 2147483647
        i64 int64 = 9223372036854775807
        u uint = 42
        f32 float32 = 3.14
        f64 float64 = 3.14159
        c byte = 'A'           // alias for uint8
        r rune = '?'          // alias for int32 (Unicode)
    )
    
    // Zero values
    var defaultInt int         // 0
    var defaultString string   // ""
    var defaultBool bool       // false
    
    // Type conversion
    var f float64 = float64(i)
    var u uint = uint(f)
    
    fmt.Println(name, age, city)
}
// If-else
if age >= 18 {
    fmt.Println("Adult")
} else if age >= 13 {
    fmt.Println("Teen")
} else {
    fmt.Println("Child")
}

// If with short statement
if err := process(); err != nil {
    fmt.Println("Error:", err)
}

// Switch (no fallthrough by default)
switch day {
case 1:
    fmt.Println("Monday")
case 2, 3, 4, 5:
    fmt.Println("Weekday")
default:
    fmt.Println("Weekend")
}

// Switch without expression
switch {
case age < 13:
    fmt.Println("Child")
case age < 18:
    fmt.Println("Teen")
default:
    fmt.Println("Adult")
}

// Type switch
var i interface{} = "hello"
switch v := i.(type) {
case int:
    fmt.Printf("Integer: %d\n", v)
case string:
    fmt.Printf("String: %s\n", v)
default:
    fmt.Printf("Unknown type\n")
}

// Loops (only for in Go)
// Traditional for
for i := 0; i < 5; i++ {
    fmt.Println(i)
}

// While-style
sum := 0
for sum < 100 {
    sum += 10
}

// Infinite loop
for {
    break
}

// Range loop
numbers := []int{1, 2, 3, 4, 5}
for i, v := range numbers {
    fmt.Printf("Index: %d, Value: %d\n", i, v)
}

// Range over string (Unicode aware)
for i, r := range "Hello, ??" {
    fmt.Printf("%d: %c\n", i, r)
}
// Basic function
func greet(name string) string {
    return "Hello, " + name + "!"
}

// Multiple return values
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, fmt.Errorf("division by zero")
    }
    return a / b, nil
}

// Named return values
func split(sum int) (x, y int) {
    x = sum * 4 / 9
    y = sum - x
    return // naked return
}

// Variadic functions
func sum(numbers ...int) int {
    total := 0
    for _, n := range numbers {
        total += n
    }
    return total
}

// Defer (executed after function returns)
func readFile() {
    f, err := os.Open("file.txt")
    if err != nil {
        return
    }
    defer f.Close() // Close when function exits
    
    // Use file...
}

// Function as value
var fn func(int) int = func(x int) int {
    return x * 2
}

// Closure
func adder() func(int) int {
    sum := 0
    return func(x int) int {
        sum += x
        return sum
    }
}

// Method (receiver)
type Person struct {
    Name string
    Age  int
}

func (p Person) greet() string {
    return "Hello, I'm " + p.Name
}

// Pointer receiver (can modify)
func (p *Person) birthday() {
    p.Age++
}
// Struct
type Person struct {
    Name string
    Age  int
    email string  // private (lowercase)
}

// Constructor pattern
func NewPerson(name string, age int) *Person {
    return &Person{Name: name, Age: age}
}

// Embedded struct (composition)
type Employee struct {
    Person      // Embedded (promoted fields)
    Company string
    Salary  float64
}

// Interface
type Greeter interface {
    Greet() string
}

func (p Person) Greet() string {
    return "Hello, I'm " + p.Name
}

// Empty interface (any type)
var anything interface{} = "hello"

// Type assertion
value, ok := anything.(string)
if ok {
    fmt.Println("String:", value)
}

// Interface satisfaction (implicit)
var g Greeter = Person{Name: "Alice", Age: 25}
// Error interface
type error interface {
    Error() string
}

// Custom error
type ValidationError struct {
    Field string
    Value interface{}
}

func (e ValidationError) Error() string {
    return fmt.Sprintf("invalid %s: %v", e.Field, e.Value)
}

// Panic and recover
func mayPanic() {
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("Recovered:", r)
        }
    }()
    panic("something went wrong")
}

// Idiomatic error handling
result, err := divide(10, 0)
if err != nil {
    fmt.Println("Error:", err)
    return
}
fmt.Println("Result:", result)
// Goroutine
go func() {
    fmt.Println("Running concurrently")
}()

// Wait for goroutine
var wg sync.WaitGroup
for i := 0; i < 5; i++ {
    wg.Add(1)
    go func(id int) {
        defer wg.Done()
        fmt.Printf("Worker %d\n", id)
    }(i)
}
wg.Wait()

// Channels
ch := make(chan int)

// Send
go func() {
    ch <- 42
}()

// Receive
value := <-ch

// Buffered channel
ch := make(chan string, 3)
ch <- "a"
ch <- "b"
ch <- "c"

// Close channel
close(ch)

// Range over channel
for v := range ch {
    fmt.Println(v)
}

// Select
select {
case msg1 := <-ch1:
    fmt.Println("Received from ch1:", msg1)
case msg2 := <-ch2:
    fmt.Println("Received from ch2:", msg2)
case <-time.After(1 * time.Second):
    fmt.Println("Timeout")
default:
    fmt.Println("No channels ready")
}

// Mutex
var mu sync.Mutex
mu.Lock()
// Critical section
mu.Unlock()

// RWMutex
var rw sync.RWMutex
rw.RLock()  // Multiple readers
rw.RUnlock()
rw.Lock()   // Single writer
rw.Unlock()
import (
    "fmt"
    "os"
    "io"
    "strings"
    "strconv"
    "encoding/json"
    "net/http"
    "time"
    "context"
)

// String operations
strings.Contains("hello", "ll")    // true
strings.Split("a,b,c", ",")        // ["a", "b", "c"]
strings.Join([]string{"a", "b"}, "-") // "a-b"

// Conversion
i, _ := strconv.Atoi("42")         // 42
s := strconv.Itoa(42)              // "42"

// JSON
type User struct {
    Name string `json:"name"`
    Age  int    `json:"age"`
}
data, _ := json.Marshal(User{"Alice", 25})
var user User
json.Unmarshal(data, &user)

// HTTP Client
resp, err := http.Get("https://api.example.com/data")
defer resp.Body.Close()
body, _ := io.ReadAll(resp.Body)

// HTTP Server
http.HandleFunc("/hello", func(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hello, %s!", r.URL.Path[1:])
})
http.ListenAndServe(":8080", nil)

// Time
now := time.Now()
future := now.Add(24 * time.Hour)
time.Sleep(2 * time.Second)

// Context
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

select {
case <-doWork(ctx):
    fmt.Println("Work completed")
case <-ctx.Done():
    fmt.Println("Timeout:", ctx.Err())
}

module github.com/username/myproject

go 1.23

require (
    github.com/gorilla/mux v1.8.1
    github.com/lib/pq v1.10.9
)
fn main() {
    println!("Hello, World!");
}
fn main() {
    // Immutable by default
    let x = 5;
    // x = 6;  // Error!
    
    // Mutable
    let mut y = 10;
    y = 11;
    
    // Constants
    const PI: f64 = 3.14159;
    
    // Shadowing
    let z = 5;
    let z = z + 1;  // New variable, can change type
    
    // Basic types
    let b: bool = true;
    let c: char = 'A';
    let i: i32 = 42;           // Signed 32-bit
    let u: u64 = 100;          // Unsigned 64-bit
    let f: f64 = 3.14;         // Float 64-bit
    let s: &str = "hello";     // String slice
    let string: String = String::from("hello");
    
    // Compound types
    let tup: (i32, f64, char) = (42, 3.14, 'A');
    let (a, b, c) = tup;       // Destructuring
    let first = tup.0;         // Index access
    
    let arr: [i32; 5] = [1, 2, 3, 4, 5];
    let arr = [0; 10];         // [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    let slice = &arr[1..4];    // Slice [2, 3, 4]
    
    // Vectors (heap-allocated)
    let mut vec: Vec<i32> = Vec::new();
    vec.push(1);
    vec.push(2);
    let vec = vec![1, 2, 3, 4, 5];
}
fn main() {
    // Ownership
    let s1 = String::from("hello");
    let s2 = s1;  // s1 moved, no longer valid
    // println!("{}", s1);  // Error!
    
    let s3 = s2.clone();  // Deep copy
    
    // Borrowing (references)
    let s = String::from("hello");
    let len = calculate_length(&s);  // Borrow, s still valid
    
    // Mutable borrow
    let mut s = String::from("hello");
    change(&mut s);
    
    // Only ONE mutable borrow OR multiple immutable borrows
    let r1 = &s;
    let r2 = &s;
    // let r3 = &mut s;  // Error! Cannot borrow as mutable while immutable borrows exist
}

fn calculate_length(s: &String) -> usize {
    s.len()
}

fn change(s: &mut String) {
    s.push_str(", world");
}
// If-else (expression)
let condition = true;
let number = if condition { 5 } else { 6 };

// Loop
let mut counter = 0;
let result = loop {
    counter += 1;
    if counter == 10 {
        break counter * 2;  // Returns value
    }
};

// While
let mut n = 3;
while n > 0 {
    println!("{}", n);
    n -= 1;
}

// For loop
let arr = [10, 20, 30, 40, 50];
for element in arr {
    println!("{}", element);
}

// Range
for i in 0..5 {      // 0, 1, 2, 3, 4
    println!("{}", i);
}

for i in 0..=5 {     // 0, 1, 2, 3, 4, 5
    println!("{}", i);
}

// Match (pattern matching)
let value = 42;
match value {
    0 => println!("Zero"),
    1..=10 => println!("Small"),
    n if n % 2 == 0 => println!("Even"),
    _ => println!("Other"),
}

// If let
let optional = Some(5);
if let Some(x) = optional {
    println!("Value: {}", x);
}
// Basic function
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

// Return expression (no semicolon)
fn add(a: i32, b: i32) -> i32 {
    a + b
}

// Generic function
fn largest<T: PartialOrd>(list: &[T]) -> &T {
    let mut largest = &list[0];
    for item in list {
        if item > largest {
            largest = item;
        }
    }
    largest
}

// Closure
let add_one = |x| x + 1;
let result = add_one(5);  // 6

let calculate = |a, b| {
    let sum = a + b;
    sum * 2
};

// Closure capturing environment
let x = 4;
let equal_to_x = |z| z == x;  // Borrows x
// Struct
struct Person {
    name: String,
    age: u32,
}

impl Person {
    // Associated function (constructor)
    fn new(name: String, age: u32) -> Person {
        Person { name, age }
    }
    
    // Method
    fn greet(&self) -> String {
        format!("Hello, I'm {}", self.name)
    }
    
    // Mutating method
    fn birthday(&mut self) {
        self.age += 1;
    }
    
    // Consuming method
    fn into_name(self) -> String {
        self.name
    }
}

// Tuple struct
struct Color(u8, u8, u8);
let red = Color(255, 0, 0);

// Unit struct
struct AlwaysEqual;

// Enum
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(u8, u8, u8),
}

impl Message {
    fn call(&self) {
        match self {
            Message::Quit => println!("Quit"),
            Message::Move { x, y } => println!("Move to {}, {}", x, y),
            Message::Write(s) => println!("Write: {}", s),
            Message::ChangeColor(r, g, b) => println!("Color: {}, {}, {}", r, g, b),
        }
    }
}

// Option enum
let some_number: Option<i32> = Some(5);
let absent: Option<i32> = None;

// Result enum
fn divide(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        Err(String::from("Division by zero"))
    } else {
        Ok(a / b)
    }
}

// Error propagation with ?
fn read_file() -> Result<String, std::io::Error> {
    std::fs::read_to_string("file.txt")
}
// Trait definition
trait Greeter {
    fn greet(&self) -> String;
    
    // Default implementation
    fn greet_formal(&self) -> String {
        format!("Greetings, {}", self.name())
    }
    
    fn name(&self) -> &str;
}

// Trait implementation
impl Greeter for Person {
    fn greet(&self) -> String {
        format!("Hello, I'm {}", self.name)
    }
    
    fn name(&self) -> &str {
        &self.name
    }
}

// Trait bounds
fn say_hello<T: Greeter>(item: &T) {
    println!("{}", item.greet());
}

// Where clause
fn complex<T, U>(t: &T, u: &U) -> String
where
    T: Greeter + Clone,
    U: std::fmt::Display,
{
    format!("{} {}", t.greet(), u)
}

// Trait objects (dynamic dispatch)
let greeters: Vec<Box<dyn Greeter>> = vec![
    Box::new(Person::new("Alice".to_string(), 25)),
];

// Derivable traits
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Point {
    x: i32,
    y: i32,
}
use std::fs::File;
use std::io::{self, Read};

// panic! (unrecoverable)
// panic!("crash and burn");

// Result (recoverable)
fn read_username() -> Result<String, io::Error> {
    let f = File::open("username.txt");
    
    let mut f = match f {
        Ok(file) => file,
        Err(e) => return Err(e),
    };
    
    let mut s = String::new();
    match f.read_to_string(&mut s) {
        Ok(_) => Ok(s),
        Err(e) => Err(e),
    }
}

// Using ? operator (propagates error)
fn read_username_short() -> Result<String, io::Error> {
    let mut s = String::new();
    File::open("username.txt")?.read_to_string(&mut s)?;
    Ok(s)
}

// Custom error type
#[derive(Debug)]
enum MyError {
    Io(io::Error),
    Parse(std::num::ParseIntError),
}

impl std::fmt::Display for MyError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            MyError::Io(e) => write!(f, "IO error: {}", e),
            MyError::Parse(e) => write!(f, "Parse error: {}", e),
        }
    }
}

impl std::error::Error for MyError {}

impl From<io::Error> for MyError {
    fn from(err: io::Error) -> MyError {
        MyError::Io(err)
    }
}

impl From<std::num::ParseIntError> for MyError {
    fn from(err: std::num::ParseIntError) -> MyError {
        MyError::Parse(err)
    }
}
use std::thread;
use std::sync::{Arc, Mutex};
use std::time::Duration;

// Spawn thread
let handle = thread::spawn(|| {
    for i in 1..10 {
        println!("Thread: {}", i);
        thread::sleep(Duration::from_millis(1));
    }
});

// Wait for thread
handle.join().unwrap();

// Move ownership into thread
let v = vec![1, 2, 3];
let handle = thread::spawn(move || {
    println!("{:?}", v);
});

// Shared state with Mutex
let counter = Arc::new(Mutex::new(0));
let mut handles = vec![];

for _ in 0..10 {
    let counter = Arc::clone(&counter);
    let handle = thread::spawn(move || {
        let mut num = counter.lock().unwrap();
        *num += 1;
    });
    handles.push(handle);
}

for handle in handles {
    handle.join().unwrap();
}

println!("Result: {}", *counter.lock().unwrap());  // 10

// Message passing (channels)
use std::sync::mpsc;

let (tx, rx) = mpsc::channel();

thread::spawn(move || {
    let val = String::from("hello");
    tx.send(val).unwrap();
    // val is moved, cannot use here
});

let received = rx.recv().unwrap();
println!("Got: {}", received);
use std::collections::HashMap;
use std::collections::HashSet;

// Vector
let mut v: Vec<i32> = Vec::new();
v.push(1);
v.push(2);
let third = &v[2];
match v.get(2) {
    Some(third) => println!("Third: {}", third),
    None => println!("No third element"),
}

for i in &v {
    println!("{}", i);
}

for i in &mut v {
    *i += 50;
}

// String
let mut s = String::new();
s.push_str("hello");
s.push('!');
let hello = &s[0..5];  // Slice

// Concatenation
let s1 = String::from("Hello, ");
let s2 = String::from("world!");
let s3 = s1 + &s2;  // s1 moved
let s4 = format!("{}-{}", s3, s2);

// HashMap
let mut scores = HashMap::new();
scores.insert(String::from("Blue"), 10);
scores.insert(String::from("Yellow"), 50);

let team = String::from("
# Continue with more language references

# 5. GO
@'
# CodeClaw - Go Reference

## Overview
Go is a statically typed, compiled programming language designed at Google for building simple, reliable, and efficient software.

| Attribute | Value |
|-----------|-------|
| **First Released** | 2009 |
| **Designed By** | Robert Griesemer, Rob Pike, Ken Thompson |
| **Typing** | Static, Strong, Structural |
| **Paradigm** | Concurrent, Imperative, Procedural |
| **File Extensions** | `.go` |
| **Official Website** | https://go.dev |
| **Package Manager** | go modules |
| **Current Stable** | Go 1.22+ |

## Key Features
- **Simplicity**: Small language with orthogonal features
- **Goroutines**: Lightweight concurrent execution
- **Channels**: Communication between goroutines
- **Fast Compilation**: Compiles directly to machine code
- **Garbage Collected**: Automatic memory management
- **Static Binaries**: Single executable deployment

## Basic Syntax

### Variables and Data Types
```go
package main

import "fmt"

func main() {
    // Variable declarations
    var name string = "Alice"
    var age int = 25
    var height float64 = 5.8
    var isStudent bool = true
    
    // Short declaration (type inference)
    city := "New York"
    score := 95
    
    // Multiple declarations
    var x, y int = 10, 20
    a, b := "hello", 42
    
    // Constants
    const Pi = 3.14159
    const (
        StatusOK = 200
        StatusNotFound = 404
    )
    
    // Basic types
    var (
        i int = 42
        f float32 = 3.14
        b bool = true
        s string = "Go"
        r rune = 'G'        // Unicode code point
        by byte = 65        // Alias for uint8
    )
    
    // Zero values (defaults)
    var defaultInt int       // 0
    var defaultString string // ""
    var defaultBool bool     // false
    
    fmt.Printf("Name: %s, Age: %d\n", name, age)
}
// If-else
if age >= 18 {
    fmt.Println("Adult")
} else if age >= 13 {
    fmt.Println("Teen")
} else {
    fmt.Println("Child")
}

// If with short statement
if err := process(); err != nil {
    fmt.Println("Error:", err)
}

// Switch (no break needed, implicit fallthrough with `fallthrough`)
switch day {
case 1:
    fmt.Println("Monday")
case 2:
    fmt.Println("Tuesday")
case 3, 4, 5:
    fmt.Println("Weekday")
default:
    fmt.Println("Weekend")
}

// Switch without expression
switch {
case age < 13:
    fmt.Println("Child")
case age < 18:
    fmt.Println("Teen")
default:
    fmt.Println("Adult")
}

// For loop (only loop construct in Go)
for i := 0; i < 5; i++ {
    fmt.Println(i)
}

// While-style loop
count := 0
for count < 5 {
    fmt.Println(count)
    count++
}

// Infinite loop
for {
    // break to exit
    break
}

// Range loop
numbers := []int{1, 2, 3, 4, 5}
for index, value := range numbers {
    fmt.Printf("Index: %d, Value: %d\n", index, value)
}

// Range over string
for i, ch := range "Hello" {
    fmt.Printf("Index: %d, Char: %c\n", i, ch)
}// Arrays (fixed size)
var arr [5]int
arr[0] = 1
arr2 := [5]int{1, 2, 3, 4, 5}
arr3 := [...]int{1, 2, 3}  // Compiler counts

// Slices (dynamic arrays)
var slice []int
slice = make([]int, 5)        // length 5, capacity 5
slice2 := make([]int, 5, 10)  // length 5, capacity 10
slice3 := []int{1, 2, 3, 4, 5}

// Slice operations
slice = append(slice, 6, 7, 8)
slice = append(slice, slice2...)  // Append another slice
copied := make([]int, len(slice))
copy(copied, slice)

// Slice slicing
sub := slice[1:4]   // elements 1,2,3
start := slice[:3]  // first 3
end := slice[3:]    // from index 3 to end
all := slice[:]     // all elements

// Slice internals
length := len(slice)
capacity := cap(slice)
// Create map
var m map[string]int
m = make(map[string]int)
m2 := map[string]int{
    "apple":  5,
    "banana": 3,
}

// Operations
m["key"] = 42
value := m["key"]
delete(m, "key")

// Check existence
if val, ok := m["key"]; ok {
    fmt.Println("Value:", val)
} else {
    fmt.Println("Key not found")
}

// Iterate
for key, value := range m {
    fmt.Printf("%s: %d\n", key, value)
}
// Struct definition
type Person struct {
    Name string
    Age  int
    email string  // private (lowercase)
}

// Constructor pattern
func NewPerson(name string, age int) *Person {
    return &Person{
        Name: name,
        Age:  age,
    }
}

// Method (value receiver)
func (p Person) Greet() string {
    return fmt.Sprintf("Hello, I'm %s", p.Name)
}

// Method (pointer receiver - can modify)
func (p *Person) Birthday() {
    p.Age++
}

// Stringer interface
func (p Person) String() string {
    return fmt.Sprintf("%s (%d)", p.Name, p.Age)
}

// Embedded struct (composition)
type Employee struct {
    Person      // Embedded
    EmployeeID string
    Department  string
}

// Interface
type Greeter interface {
    Greet() string
}

// Empty interface (any type)
var anything interface{}
anything = 42
anything = "hello"
anything = Person{Name: "Alice"}

// Type assertion
value, ok := anything.(Person)
if ok {
    fmt.Println(value.Name)
}

// Type switch
switch v := anything.(type) {
case int:
    fmt.Println("Integer:", v)
case string:
    fmt.Println("String:", v)
case Person:
    fmt.Println("Person:", v.Name)
}
// Goroutine
go func() {
    fmt.Println("Running concurrently")
}()

// Channel (unbuffered)
ch := make(chan int)

// Send and receive
go func() {
    ch <- 42  // Send
}()
value := <-ch  // Receive

// Buffered channel
ch := make(chan string, 3)
ch <- "first"
ch <- "second"
ch <- "third"

// Close channel
close(ch)

// Range over channel
for msg := range ch {
    fmt.Println(msg)
}

// Select statement
select {
case msg1 := <-ch1:
    fmt.Println("From ch1:", msg1)
case msg2 := <-ch2:
    fmt.Println("From ch2:", msg2)
case <-time.After(1 * time.Second):
    fmt.Println("Timeout")
default:
    fmt.Println("No channels ready")
}

// Worker pool pattern
func worker(id int, jobs <-chan int, results chan<- int) {
    for job := range jobs {
        results <- job * 2
    }
}

// Mutex
var mu sync.Mutex
mu.Lock()
// critical section
mu.Unlock()

// WaitGroup
var wg sync.WaitGroup
for i := 0; i < 5; i++ {
    wg.Add(1)
    go func(id int) {
        defer wg.Done()
        // Do work
    }(i)
}
wg.Wait()// Error interface
type error interface {
    Error() string
}

// Custom error
type ValidationError struct {
    Field string
    Value interface{}
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed for %s: %v", e.Field, e.Value)
}

// Panic and Recover
func mayPanic() {
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("Recovered:", r)
        }
    }()
    panic("something went wrong")
}import (
    "fmt"           // Formatted I/O
    "os"            // Operating system
    "io"            // I/O utilities
    "bufio"         // Buffered I/O
    "encoding/json" // JSON encoding
    "net/http"      // HTTP client/server
    "time"          // Time utilities
    "strings"       // String manipulation
    "strconv"       // String conversion
    "sync"          // Synchronization
    "context"       // Context propagation
)myproject/
+-- cmd/
¦   +-- myapp/
¦       +-- main.go
+-- internal/
¦   +-- mypackage/
+-- pkg/
¦   +-- publicpackage/
+-- go.mod
+-- go.sum
+-- README.md
fn main() {
    // Immutable by default
    let x = 5;
    // x = 6;  // Error!
    
    // Mutable
    let mut y = 10;
    y = 15;
    
    // Type annotations
    let z: i32 = 42;
    let f: f64 = 3.14159;
    let b: bool = true;
    let c: char = 'A';
    let s: &str = "Hello";
    
    // Constants
    const PI: f64 = 3.14159;
    
    // Shadowing
    let x = x + 1;  // New variable shadows old
    
    // Integer types
    let i8: i8 = -128;
    let u8: u8 = 255;
    let i32: i32 = -2_147_483_648;
    let u32: u32 = 4_294_967_295;
    let isize: isize = 42;  // Pointer-sized
    let usize: usize = 42;
    
    // Float types
    let f32: f32 = 3.14;
    let f64: f64 = 3.14159265359;
    
    // Boolean
    let t: bool = true;
    let f: bool = false;
    
    // Character (4 bytes, Unicode)
    let heart_eyed_cat: char = '??';
    
    // Tuple
    let tup: (i32, f64, char) = (500, 6.4, 'A');
    let (a, b, c) = tup;  // Destructuring
    let first = tup.0;     // Index access
    
    // Array (fixed size)
    let arr: [i32; 5] = [1, 2, 3, 4, 5];
    let zeros = [0; 5];    // [0, 0, 0, 0, 0]
    let first = arr[0];
    
    // Vector (dynamic array)
    let mut vec: Vec<i32> = Vec::new();
    vec.push(1);
    vec.push(2);
    let vec2 = vec![1, 2, 3, 4, 5];
    
    // String
    let s1 = String::from("Hello");
    let s2 = "World".to_string();
    let mut s3 = String::new();
    s3.push_str("Rust");
    s3.push('!');
    
    // String slice
    let slice: &str = &s1[0..2];
    
    println!("x: {}, y: {}", x, y);
}
// If expression (returns value)
let condition = true;
let number = if condition { 5 } else { 6 };

// If-else if-else
if number < 5 {
    println!("Less than 5");
} else if number == 5 {
    println!("Equal to 5");
} else {
    println!("Greater than 5");
}

// Loop (infinite)
let mut counter = 0;
loop {
    counter += 1;
    if counter == 10 {
        break;  // Exit loop
    }
}

// Returning value from loop
let result = loop {
    counter += 1;
    if counter == 10 {
        break counter * 2;
    }
};

// While loop
while counter > 0 {
    println!("{}", counter);
    counter -= 1;
}

// For loop
let arr = [10, 20, 30, 40, 50];
for element in arr {
    println!("{}", element);
}

// Range
for number in 1..5 {      // 1, 2, 3, 4
    println!("{}", number);
}
for number in 1..=5 {     // 1, 2, 3, 4, 5
    println!("{}", number);
}

// Match (pattern matching)
let value = 2;
match value {
    1 => println!("One"),
    2 => println!("Two"),
    3 | 4 => println!("Three or Four"),
    5..=10 => println!("Between 5 and 10"),
    _ => println!("Anything else"),
}

// Match with binding
match value {
    n @ 1..=5 => println!("Small: {}", n),
    n => println!("Other: {}", n),
}
// Ownership rules:
// 1. Each value has one owner
// 2. When owner goes out of scope, value is dropped
// 3. Value can have one mutable reference OR any number of immutable references

fn main() {
    // Move semantics
    let s1 = String::from("Hello");
    let s2 = s1;  // s1 moved to s2
    // println!("{}", s1);  // Error! s1 no longer valid
    
    // Clone (deep copy)
    let s3 = String::from("Hello");
    let s4 = s3.clone();  // Both valid
    println!("s3: {}, s4: {}", s3, s4);
    
    // Copy trait (stack-only data)
    let x = 5;
    let y = x;  // x is copied, both valid
    println!("x: {}, y: {}", x, y);
    
    // Borrowing (references)
    let s = String::from("Hello");
    let len = calculate_length(&s);  // Borrow (doesn't take ownership)
    println!("Length of '{}' is {}.", s, len);
    
    // Mutable references
    let mut s = String::from("Hello");
    change(&mut s);
    println!("{}", s);
    
    // Only one mutable reference at a time
    let mut s = String::from("Hello");
    let r1 = &mut s;
    // let r2 = &mut s;  // Error! Cannot borrow twice
    println!("{}", r1);
    
    // Multiple immutable references allowed
    let s = String::from("Hello");
    let r1 = &s;
    let r2 = &s;
    println!("{} and {}", r1, r2);
    
    // Dangling references prevented
    // let reference = dangle();  // Error!
}

fn calculate_length(s: &String) -> usize {
    s.len()
}

fn change(s: &mut String) {
    s.push_str(", World!");
}// Struct
struct User {
    username: String,
    email: String,
    sign_in_count: u64,
    active: bool,
}

// Tuple struct
struct Color(i32, i32, i32);
struct Point(f64, f64, f64);

// Unit-like struct
struct AlwaysEqual;

// Struct methods
impl User {
    // Associated function (constructor)
    fn new(username: String, email: String) -> User {
        User {
            username,
            email,
            sign_in_count: 0,
            active: true,
        }
    }
    
    // Method (takes self)
    fn is_active(&self) -> bool {
        self.active
    }
    
    // Mutable method
    fn increment_sign_in(&mut self) {
        self.sign_in_count += 1;
    }
}

// Enum
enum IpAddrKind {
    V4,
    V6,
}

enum IpAddr {
    V4(u8, u8, u8, u8),
    V6(String),
}

enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}

// Enum methods
impl Message {
    fn call(&self) {
        match self {
            Message::Quit => println!("Quit"),
            Message::Move { x, y } => println!("Move to {}, {}", x, y),
            Message::Write(s) => println!("Write: {}", s),
            Message::ChangeColor(r, g, b) => println!("Color: {}, {}, {}", r, g, b),
        }
    }
}

// Option enum (built-in)
fn divide(numerator: f64, denominator: f64) -> Option<f64> {
    if denominator == 0.0 {
        None
    } else {
        Some(numerator / denominator)
    }
}

// Using Option
let result = divide(10.0, 2.0);
match result {
    Some(x) => println!("Result: {}", x),
    None => println!("Cannot divide by zero"),
}

// If let syntax
if let Some(x) = result {
    println!("Result: {}", x);
}

// Result enum (built-in)
fn read_file(path: &str) -> Result<String, std::io::Error> {
    std::fs::read_to_string(path)
}

// Using Result
match read_file("test.txt") {
    Ok(content) => println!("File content: {}", content),
    Err(e) => println!("Error: {}", e),
}
// Trait definition
trait Summary {
    fn summarize(&self) -> String;
    
    // Default implementation
    fn summarize_default(&self) -> String {
        String::from("(Read more...)")
    }
}

// Implementing trait
struct NewsArticle {
    headline: String,
    location: String,
    author: String,
    content: String,
}

impl Summary for NewsArticle {
    fn summarize(&self) -> String {
        format!("{}, by {} ({})", self.headline, self.author, self.location)
    }
}

// Trait bounds
fn notify<T: Summary>(item: &T) {
    println!("Breaking news! {}", item.summarize());
}

// Multiple trait bounds
fn notify_and_display<T: Summary + std::fmt::Display>(item: &T) {
    println!("{}", item.summarize());
}

// Where clause
fn some_function<T, U>(t: &T, u: &U) -> i32
where
    T: Summary + Clone,
    U: Clone + std::fmt::Debug,
{
    42
}

// Returning types that implement traits
fn returns_summarizable() -> impl Summary {
    NewsArticle {
        headline: String::from("Rust is great!"),
        location: String::from("Internet"),
        author: String::from("Greg"),
        content: String::from("..."),
    }
}

// Generics in structs
struct Point<T> {
    x: T,
    y: T,
}

struct PointMixed<T, U> {
    x: T,
    y: U,
}

// Generics in methods
impl<T> Point<T> {
    fn x(&self) -> &T {
        &self.x
    }
}

// Conditional methods (only for specific types)
impl Point<f32> {
    fn distance_from_origin(&self) -> f32 {
        (self.x.powi(2) + self.y.powi(2)).sqrt()
    }
}use std::collections::HashMap;
use std::collections::HashSet;

fn main() {
    // Vector
    let mut v: Vec<i32> = Vec::new();
    v.push(1);
    v.push(2);
    v.push(3);
    
    let v2 = vec![1, 2, 3, 4, 5];
    
    // Access
    let third: &i32 = &v[2];
    match v.get(2) {
        Some(third) => println!("Third: {}", third),
        None => println!("No third element"),
    }
    
    // Iterate
    for i in &v {
        println!("{}", i);
    }
    
    for i in &mut v {
        *i += 50;  // Dereference to modify
    }
    
    // String
    let mut s = String::new();
    s.push_str("Hello");
    s.push(' ');
    s.push_str("World");
    
    // Concatenation
    let s1 = String::from("Hello");
    let s2 = String::from("World");
    let s3 = s1 + " " + &s2;
    
    // Format macro
    let s = format!("{}-{}-{}", "Hello", "World", "!");
    
    // HashMap
    let mut scores = HashMap::new();
    scores.insert(String::from("Blue"), 10);
    scores.insert(String::from("Yellow"), 50);
    
    // Access
    let team = String::from("Blue");
    let score = scores.get(&team).copied().unwrap_or(0);
    
    // Iterate
    for (key, value) in &scores {
        println!("{}: {}", key, value);
    }
    
    // Update
    scores.entry(String::from("Blue")).or_insert(50);
    
    // HashSet
    let mut set = HashSet::new();
    set.insert(1);
    set.insert(2);
    set.insert(3);
    
    if set.contains(&2) {
        println!("Set contains 2");
    }
}// Panic (unrecoverable)
// panic!("crash and burn");

// Result (recoverable)
use std::fs::File;
use std::io::ErrorKind;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let f = File::open("hello.txt");
    
    let f = match f {
        Ok(file) => file,
        Err(error) => match error.kind() {
            ErrorKind::NotFound => match File::create("hello.txt") {
                Ok(fc) => fc,
                Err(e) => panic!("Problem creating file: {:?}", e),
            },
            other_error => panic!("Problem opening file: {:?}", other_error),
        },
    };
    
    // Unwrap (panics on error)
    let f = File::open("hello.txt").unwrap();
    
    // Expect (panic with custom message)
    let f = File::open("hello.txt").expect("Failed to open hello.txt");
    
    // ? operator (propagates error)
    let content = read_file()?;
    
    Ok(())
}

fn read_file() -> Result<String, std::io::Error> {
    std::fs::read_to_string("hello.txt")
}use std::thread;
use std::time::Duration;
use std::sync::{Arc, Mutex, mpsc};

fn main() {
    // Spawn thread
    let handle = thread::spawn(|| {
        for i in 1..10 {
            println!("Spawned: {}", i);
            thread::sleep(Duration::from_millis(1));
        }
    });
    
    // Wait for thread
    handle.join().unwrap();
    
    // Move closure
    let v = vec![1, 2, 3];
    let handle = thread::spawn(move || {
        println!("Vector: {:?}", v);
    });
    
    // Channels (mpsc - multiple producer, single consumer)
    let (tx, rx) = mpsc::channel();
    
    let tx1 = tx.clone();
    thread::spawn(move || {
        let vals = vec!["hi", "from", "the", "thread"];
        for val in vals {
            tx1.send(val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    });
    
    thread::spawn(move || {
        let vals = vec!["more", "messages"];
        for val in vals {
            tx.send(val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    });
    
    for received in rx {
        println!("Got: {}", received);
    }
    
    // Mutex (mutual exclusion)
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];
    
    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut num = counter.lock().unwrap();
            *num += 1;
        });
        handles.push(handle);
    }
    
    for handle in handles {
        handle.join().unwrap();
    }
    
    println!("Result: {}", *counter.lock().unwrap());
}cargo new project_name          # Create new project
cargo build                     # Debug build
cargo build --release           # Release build
cargo run                       # Build and run
cargo check                     # Check compilation (faster)
cargo test                      # Run tests
cargo doc --open                # Generate and open documentation
cargo add crate_name            # Add dependency
cargo update                    # Update dependencies
cargo fmt                       # Format code
cargo clippy                    # Lint code
Best Practices
Use cargo fmt and cargo clippy regularly

Prefer Option and Result over panicking

Use pattern matching effectively

Keep functions small and focused

Use meaningful variable names

Document public API with ///

Use #[derive] for common traits

Leverage the type system to prevent bugs

Part of Clawpack CodeClaw - Rust Reference
