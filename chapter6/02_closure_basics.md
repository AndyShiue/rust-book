# 第六章第 2 集：閉包用法展示

## 本集目標
學會閉包的基本語法，了解閉包如何捕捉外部變數，並看到標準庫中使用閉包的實際案例。

## 概念說明

### 閉包的語法

上一集的函數指標很好用，但有個限制：它不能「記住」外部的東西。閉包（closure）就是為了解決這個問題而存在的。

閉包的基本語法用 `|` 來包參數：

```rust
let add_one = |x| x + 1;
```

你也可以加上型別標註，跟函數一樣明確：

```rust
let add_one = |x: i32| -> i32 { x + 1 };
```

兩種寫法效果一樣，Rust 通常能自動推導型別，所以短的寫法更常見。

### 閉包能捕捉外部變數

這是閉包和函數指標最大的差別：

```rust
let offset = 10;
let add_offset = |x| x + offset;  // 捕捉了 offset
println!("{}", add_offset(5));     // 15
```

`add_offset` 這個閉包「記住」了外部的 `offset`，每次呼叫都會用到它。普通函數做不到這件事。

### Result::map —— FnOnce 的例子

標準庫很多方法都接受閉包。還記得第五章的 `Result<T, E>` 嗎？它有一個 `map` 方法，可以把 `Ok` 裡的值做轉換：

```rust
let result: Result<i32, String> = Ok(5);
let doubled = result.map(|x| x * 2);  // Ok(10)
```

`map` 只需要呼叫閉包一次（對 `Ok` 裡的值），所以它要求的是 `FnOnce`——「至少能呼叫一次」。關於 FnOnce 的細節，我們第 4 集會深入。

### Vec::retain —— FnMut 的例子

`Vec` 的 `retain` 方法會保留符合條件的元素，移除不符合的：

```rust
let mut numbers = vec![1, 2, 3, 4, 5, 6];
numbers.retain(|x| x % 2 == 0);
// numbers 現在是 [2, 4, 6]
```

`retain` 要對每個元素都呼叫閉包，而且過程中會修改 Vec，所以它要求 `FnMut`——「可以多次呼叫，而且可以修改狀態」。

### 如果把 FnOnce 傳給 retain？

假設你有一個閉包用了 `String`，而且會消耗（move）它：

```rust
let mut items = vec![1, 2, 3];
let message = String::from("keeping");
// items.retain(|x| { drop(message); *x > 1 });  // 編譯錯誤！
```

這個閉包在第一次呼叫時就 `drop` 了 `message`，第二次就沒得 drop 了。它只能呼叫一次（FnOnce），但 `retain` 需要 FnMut（多次呼叫）。所以編譯器會報錯。

### 不捕捉變數的閉包 → 可以轉成函數指標

如果一個閉包沒有捕捉任何外部變數，它就跟普通函數沒什麼差別。Rust 允許它自動轉型成函數指標 `fn`：

```rust
let add_one: fn(i32) -> i32 = |x| x + 1;  // 沒有捕捉，可以轉成 fn
```

但如果捕捉了外部變數，就不能這樣轉了。

## 範例程式碼

```rust
fn apply_fn_pointer(f: fn(i32) -> i32, value: i32) -> i32 {
    f(value)
}

fn main() {
    // 基本閉包語法
    let square = |x: i32| -> i32 { x * x };
    println!("square(4) = {}", square(4));

    // 捕捉外部變數
    let base = 100;
    let add_base = |x| x + base;
    println!("add_base(7) = {}", add_base(7));

    // Result::map（FnOnce）
    let result: Result<i32, String> = Ok(21);
    let doubled = result.map(|x| x * 2);
    println!("doubled = {:?}", doubled);

    let err_result: Result<i32, String> = Err(String::from("oops"));
    let still_err = err_result.map(|x| x * 2);
    println!("still_err = {:?}", still_err);

    // Vec::retain（FnMut）
    let mut scores = vec![55, 72, 88, 43, 91, 60];
    scores.retain(|s| *s >= 60);
    println!("及格分數：{:?}", scores);

    // 不捕捉變數的閉包可以轉成函數指標
    let triple: fn(i32) -> i32 = |x| x * 3;
    println!("apply_fn_pointer(triple, 5) = {}", apply_fn_pointer(triple, 5));

    // 捕捉了變數的閉包不能轉成函數指標
    // let offset = 10;
    // let bad: fn(i32) -> i32 = |x| x + offset;  // 編譯錯誤！
}
```

## 重點整理
- 閉包用 `|參數| 表達式` 語法，可以省略型別標註讓 Rust 推導
- 閉包最大的特色是能**捕捉外部變數**，這是函數指標做不到的
- `Result::map` 接受 `FnOnce` 閉包——只需呼叫一次
- `Vec::retain` 接受 `FnMut` 閉包——需要多次呼叫
- 如果閉包只能呼叫一次（FnOnce），就不能傳給需要多次呼叫的方法
- 不捕捉外部變數的閉包可以自動轉型成函數指標 `fn`
