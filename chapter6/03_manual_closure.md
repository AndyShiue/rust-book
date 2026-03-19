# 第六章第 3 集：手動實作閉包

## 本集目標
透過手動把閉包拆解成 struct + 方法，理解閉包背後的運作原理以及 FnOnce / FnMut / Fn 的本質差別。

## 概念說明

上一集我們用了閉包，看到它能捕捉外部變數。但閉包到底是怎麼「記住」外部變數的？其實很簡單——編譯器幫你把捕捉的變數收集進一個匿名的 struct 裡。

我們今天來手動做一次，你就會完全懂了。

### 把捕捉的變數放進 struct

假設我們有一個閉包，捕捉了一個 `String`，而且在呼叫時會把它 move 走：

```rust
let name = String::from("Alice");
let greet = || {
    let s = name;  // move name 進來
    println!("Hello, {}!", s);
};
greet();
// greet();  // 編譯錯誤！name 已經被 move 走了，不能再呼叫
```

跟上一集 `Result::map` 的例子一樣——閉包體裡面把捕捉的變數 move 走了，所以只能呼叫一次。編譯器在背後會把被捕捉的變數放進一個匿名的 struct 裡。我們手動來做一次：

```rust
struct Greet {
    name: String,
}
```

### 閉包呼叫的真面目

當你寫 `greet()` 呼叫一個閉包時，編譯器其實是在呼叫那個匿名 struct 上的方法。根據閉包的種類不同，呼叫方式也不同：

- **FnOnce**：`greet.call_once()` — 傳 `self`，消耗 struct
- **FnMut**：`greet.call_mut()` — 傳 `&mut self`，借用但可修改
- **Fn**：`greet.call()` — 傳 `&self`，唯讀借用

上一集介紹了 FnOnce（消耗捕捉的值，只能呼叫一次）和 FnMut（可以修改捕捉的值，多次呼叫）。Fn 是第三種——只讀取捕捉的值，不消耗也不修改，也可以多次呼叫。

看到了嗎？這就是第四章學的 `self` / `&mut self` / `&self` 三種方法——閉包的呼叫就是在呼叫方法！接下來我們分別模擬這三種。

### self → FnOnce（只能呼叫一次）

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

### &mut self → FnMut（可以多次呼叫）

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

### &self → Fn（最寬鬆）

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

閉包就是一個匿名 struct，裡面存著捕捉的變數，然後編譯器幫你 impl 了對應的 Fn / FnMut / FnOnce trait。而你寫在 `||` 後面的閉包體（`{ ... }` 裡的程式碼），就是那個方法的內部實作。當你寫 `f()` 呼叫一個閉包時，編譯器會根據閉包的種類，呼叫 struct 上對應的方法（`self` / `&mut self` / `&self`），執行你寫的閉包體。

你每次寫 `|x| x + 1`，編譯器就在幕後幫你做了「建 struct + impl trait + 呼叫對應方法」這些事。

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
