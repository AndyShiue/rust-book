# 第三章第 23 集：函數參數解構

## 本集目標
學會在函數的參數位置直接解構 tuple 或 struct。

## 概念說明

我們已經學了在 `let` 和 `match` 裡解構。其實**函數的參數也可以解構**！

假設你有一個函數，接收一個 tuple `(i32, i32)` 代表座標。與其在函數內再拆開，不如直接在參數位置就拆好：

```rust
fn print_point((x, y): (i32, i32)) {
    println!("({}, {})", x, y);
}
```

注意語法：`(x, y)` 是模式（pattern），`: (i32, i32)` 是型別標註。模式和型別之間用 `:` 分隔。

呼叫的時候和平常一樣，傳一個 tuple 進去：

```rust
print_point((3, 7));
```

struct 也可以在參數位置解構：

```rust
fn print_point_struct(Point { x, y }: Point) {
    println!("({}, {})", x, y);
}
```

## 範例程式碼

```rust
struct Point {
    x: i32,
    y: i32,
}

// 函數參數解構 tuple
fn add_coordinates((x1, y1): (i32, i32), (x2, y2): (i32, i32)) -> (i32, i32) {
    (x1 + x2, y1 + y2)
}

// 函數參數解構 struct
fn describe_point(Point { x, y }: Point) {
    if x == 0 && y == 0 {
        println!("原點");
    } else if x == 0 {
        println!("在 y 軸上，y = {}", y);
    } else if y == 0 {
        println!("在 x 軸上，x = {}", x);
    } else {
        println!("一般的點 ({}, {})", x, y);
    }
}

fn main() {
    // 傳 tuple 給函數
    let a = (1, 2);
    let b = (3, 4);
    let result = add_coordinates(a, b);
    println!("({}, {}) + ({}, {}) = ({}, {})", a.0, a.1, b.0, b.1, result.0, result.1);

    // 傳 struct 給函數
    let p = Point { x: 0, y: 5 };
    describe_point(p);

    let origin = Point { x: 0, y: 0 };
    describe_point(origin);
}
```

## 為什麼 tuple 和 struct 能用 let 解構？

你可能會好奇：為什麼 tuple 和 struct 可以在 `let` 和函數參數裡直接解構，但 enum 不行？

```rust
let (x, y) = (1, 2);             // OK
let Point { x, y } = p;          // OK
// let Color::Red = c;           // 不行！
```

答案是：**tuple 和 struct 的解構不會失敗**。一個 `(i32, i32)` 一定有兩個值，一個 `Point` 一定有 `x` 和 `y`——沒有其他可能。

但 enum 不一樣。一個 `Color` 可能是 `Red`、`Green`、或 `Blue`。如果你寫 `let Color::Red = c`，但 `c` 其實是 `Green` 呢？這就失敗了。Rust 不允許 `let` 裡出現可能失敗的模式。

這種一定會成功的模式叫做 **irrefutable pattern**（不可反駁的模式），可能失敗的叫做 **refutable pattern**（可反駁的模式）。`let` 和函數參數只接受 irrefutable pattern。

想處理可能失敗的模式？下一集會教 `if let`。

## 重點整理
- 函數參數可以直接用模式解構：`fn foo((x, y): (i32, i32))`
- 語法是 `模式: 型別`，模式在前，型別在後
- tuple 和 struct 都可以在參數位置解構
- 呼叫時和平常一樣傳值，解構是函數內部的事
- 當函數只需要 struct/tuple 裡的某些欄位時，參數解構很方便
- `let` 和函數參數只接受不會失敗的模式（irrefutable pattern），所以 tuple 和 struct 可以，enum 不行
