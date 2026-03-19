# 第六章第 3 集：手動實作閉包

## 本集目標
透過手動把閉包拆解成 struct + 方法，理解閉包背後的運作原理以及 FnOnce / FnMut / Fn 的本質差別。

## 概念說明

上一集我們用了閉包，看到它能捕捉外部變數。但閉包到底是怎麼「記住」外部變數的？其實很簡單——編譯器幫你把捕捉的變數收集進一個匿名的 struct 裡。

我們今天來手動做一次，你就會完全懂了。

### 第一步：把捕捉的變數放進 struct

假設我們有一個閉包，捕捉了一個 `String`：

```rust
let name = String::from("Alice");
let greet = move || {
    let msg = format!("Hello, {}!", name);
    println!("{}", msg);
    name  // 把 name 移出去（消耗了它）
};
```

這個閉包捕捉了 `name`（String），而且在呼叫的時候會**消耗** name（把它移出去）。要模擬它，我們可以寫一個 struct：

```rust
struct Greet {
    name: String,
}
```

### 第二步：self → FnOnce（只能呼叫一次）

如果方法接受 `self`（by value），那呼叫一次之後 struct 就被消耗了，不能再用：

```rust
impl Greet {
    fn call(self) -> String {
        println!("Hello, {}!", self.name);
        self.name  // name 被移出，struct 被消耗
    }
}
```

這就對應 `FnOnce`——**只能呼叫一次**。因為 `self.name` 被 move 走了，第二次就沒有東西可以 move 了。

### 第三步：&mut self → FnMut（可以多次呼叫）

如果改成 `&mut self`，struct 不會被消耗，可以多次呼叫：

```rust
impl Greet {
    fn call_mut(&mut self) {
        self.name.push_str("!");
        println!("Hello, {}", self.name);
    }
}
```

但注意，`&mut self` 不能把 `self.name` move 走——你只是借用了它，不能搬走主人的東西。這就對應 `FnMut`——**可以多次呼叫，可以修改捕捉的變數，但不能消耗它們**。

### 第四步：&self → Fn（最寬鬆）

如果改成 `&self`，連修改都不行，只能讀取：

```rust
impl Greet {
    fn call_ref(&self) {
        println!("Hello, {}!", self.name);
    }
}
```

這對應 `Fn`——**可以多次呼叫，不會修改也不會消耗任何東西**。

### 對照表

| self 類型 | 對應 trait | 能做什麼 |
|----------|----------|---------|
| `self` | FnOnce | 消耗捕捉的值，只能呼叫一次 |
| `&mut self` | FnMut | 修改捕捉的值，可以多次呼叫 |
| `&self` | Fn | 只讀取，可以多次呼叫 |

### 所以閉包到底是什麼？

閉包就是一個匿名 struct，裡面存著捕捉的變數，然後編譯器幫你 impl 了對應的 Fn / FnMut / FnOnce trait。你每次寫 `|x| x + 1`，編譯器就在幕後幫你做了上面這些事。

## 範例程式碼

```rust
// 模擬一個捕捉 String 的閉包
struct MyClosure {
    captured: String,
}

impl MyClosure {
    fn new(value: String) -> MyClosure {
        MyClosure { captured: value }
    }

    // 類似 FnOnce：消耗 self，只能呼叫一次
    fn call_once(self) -> String {
        println!("消耗模式：{}", self.captured);
        self.captured
    }
}

// 模擬一個 FnMut 版本
struct MyCounter {
    count: i32,
}

impl MyCounter {
    fn new() -> MyCounter {
        MyCounter { count: 0 }
    }

    // 類似 FnMut：可以多次呼叫，每次修改內部狀態
    fn call_mut(&mut self) -> i32 {
        self.count += 1;
        self.count
    }
}

// 模擬一個 Fn 版本
struct MyGreeter {
    greeting: String,
}

impl MyGreeter {
    fn new(greeting: String) -> MyGreeter {
        MyGreeter { greeting }
    }

    // 類似 Fn：只讀取，可以無限次呼叫
    fn call_ref(&self, name: &str) -> String {
        format!("{}, {}!", self.greeting, name)
    }
}

fn main() {
    // FnOnce 模擬：呼叫一次就被消耗
    let closure = MyClosure::new(String::from("珍貴資料"));
    let result = closure.call_once();
    println!("拿回來了：{}", result);
    // closure.call_once();  // 編譯錯誤！closure 已經被消耗了

    // FnMut 模擬：可以多次呼叫，每次修改狀態
    let mut counter = MyCounter::new();
    println!("第 {} 次", counter.call_mut());
    println!("第 {} 次", counter.call_mut());
    println!("第 {} 次", counter.call_mut());

    // Fn 模擬：只讀取，隨便呼叫幾次都行
    let greeter = MyGreeter::new(String::from("你好"));
    println!("{}", greeter.call_ref("Alice"));
    println!("{}", greeter.call_ref("Bob"));
    println!("{}", greeter.call_ref("Charlie"));
}
```

## 重點整理
- 閉包背後其實是一個匿名 struct，捕捉的變數就是 struct 的欄位
- 方法接受 `self`（by value）→ 對應 `FnOnce`，呼叫一次就消耗
- 方法接受 `&mut self` → 對應 `FnMut`，可以多次呼叫並修改狀態
- 方法接受 `&self` → 對應 `Fn`，只讀取，可以無限次呼叫
- 每次你寫一個閉包，編譯器就在幕後做了「建 struct + impl trait」這些事
