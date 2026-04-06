# 第八章第 6 集：Deref 與自動解參考

## 本集目標
理解 Rust 的自動解參考機制，以及智慧指標為什麼能直接呼叫內部型別的方法。

## 概念說明

### 從 `.` 自動加 `&` 說起

前面學過，呼叫方法的時候 Rust 會自動幫你加 `&`。也就是說 `(&a).method()` 其實能簡寫成 `a.method()`。

這其實是一個更廣泛機制的一部分：當你用 `.` 呼叫方法時，Rust 會**自動解參考**。

### 智慧指標的自動解參考

這個機制讓智慧指標用起來非常方便：

```rust
let boxed = Box::new(String::from("hello"));
println!("{}", boxed.len()); // 直接呼叫 String 的 len()
```

`boxed` 是 `Box<String>`，但 `len()` 是 `String` 的方法。Rust 自動幫你解參考了——先從 `Box<String>` 取出 `String`，再呼叫 `len()`。

`Arc`、`Rc` 也一樣：

```rust
use std::sync::Arc;

let arc = Arc::new(vec![1, 2, 3]);
println!("{}", arc.len()); // 直接呼叫 Vec 的 len()
```

### Deref trait

智慧指標之所以能自動解參考，是因為它們實作了 `Deref` trait。`Deref` 告訴 Rust：「當你需要解參考我的時候，你會得到什麼型別的參考。」

- `Box<T>` 實作了 `Deref`，解參考得到 `&T`
- `Rc<T>` 實作了 `Deref`，解參考得到 `&T`
- `Arc<T>` 實作了 `Deref`，解參考得到 `&T`
- `String` 實作了 `Deref`，解參考得到 `&str`
- `Vec<T>` 實作了 `Deref`，解參考得到 `&[T]`

`DerefMut` 是可變版本，讓你能透過智慧指標取得 `&mut T`。

### `&String` → `&str` 的魔法

你可能之前就注意到了：一個接受 `&str` 參數的函數，可以直接傳 `&String` 進去。這背後就是 Deref 在運作：

```rust
fn greet(name: &str) {
    println!("Hello, {}!", name);
}

let s = String::from("Rust");
greet(&s); // &String 自動轉成 &str
```

同理，`&Vec<T>` 可以自動轉成 `&[T]`。

### 方法同名時的優先順序

Rust 從外往內找方法：外層智慧指標自身的方法優先於內層型別的方法。

一個常見的例子是 `clone`。`Arc` 本身有 `clone` 方法（增加引用計數），`T` 可能也有 `clone` 方法（深度複製資料）。直接呼叫 `.clone()` 會拿到 Arc 的 clone：

```rust
use std::sync::Arc;

let a = Arc::new(String::from("hello"));
let b = a.clone(); // Arc::clone，增加引用計數，不複製 String
```

如果你想呼叫內層 String 的 clone，可以明確寫出來：

```rust
let c = (*a).clone(); // String::clone，真的複製了一份 String
```

或者用慣用寫法 `Arc::clone(&a)` 來表示你要的是 Arc 的 clone，讓意圖更清楚。

## 範例程式碼

```rust
use std::sync::Arc;

fn print_len(s: &str) {
    println!("長度：{}", s.len());
}

fn sum_slice(nums: &[i32]) -> i32 {
    nums.iter().sum()
}

fn main() {
    // Box 自動解參考
    let boxed = Box::new(String::from("hello"));
    println!("Box 裡的字串長度：{}", boxed.len());

    // &String → &str（Deref）
    let s = String::from("world");
    print_len(&s);

    // &Vec<T> → &[T]（Deref）
    let v = vec![1, 2, 3, 4, 5];
    println!("總和：{}", sum_slice(&v));

    // Arc 自動解參考
    let arc = Arc::new(vec![10, 20, 30]);
    println!("Arc 裡的 Vec 長度：{}", arc.len());

    // clone 的優先順序
    let a = Arc::new(String::from("shared"));
    let b = a.clone();       // Arc::clone（快，只增加計數）
    let c = (*a).clone();    // String::clone（慢，複製整個 String）
    println!("a = {}, b = {}, c = {}", a, b, c);
    println!("Arc 計數 = {}", Arc::strong_count(&a)); // 2，不是 3
}
```

## 重點整理
- 用 `.` 呼叫方法時，Rust 會自動解參考，智慧指標因此能直接呼叫內部型別的方法
- `Deref` trait 讓智慧指標告訴 Rust「解參考後得到什麼」，`DerefMut` 是可變版本
- `&String` 自動轉成 `&str`、`&Vec<T>` 自動轉成 `&[T]`，都是 Deref 在運作
- 方法同名時外層優先——`Arc::clone` 和 `String::clone` 是不同的操作
