# 第五章第 16 集：多個 trait bound 與 where

## 本集目標
學會用 `+` 組合多個 trait bound，以及用 `where` 子句讓複雜的 bound 更好讀。

## 概念說明

第 13 集我們學了 `T: Clone`，要求 T 必須實作 Clone。但如果你想同時要求 T 實作多個 trait 呢？

### 多個 Trait Bound

用 `+` 把多個 trait bound 串起來：

```rust
fn show_clone<T: Clone + std::fmt::Display>(x: &T) {
    let cloned = x.clone();
    println!("原始：{}", x);
    println!("克隆：{}", cloned);
}
```

`T: Clone + Display` 表示 T 必須同時實作 Clone 和 Display。

### where 子句

當 trait bound 很長的時候，寫在 `<>` 裡面會很擠。Rust 提供 `where` 子句，放在函數簽名後面：

```rust
fn show_clone<T>(x: &T)
where
    T: Clone + std::fmt::Display,
{
    let cloned = x.clone();
    println!("原始：{}", x);
    println!("克隆：{}", cloned);
}
```

兩種寫法完全等價，只是 `where` 比較好讀。

### where 比角括號更靈活

`where` 子句的冒號前面不只能放 `T`，還能放更複雜的東西。比如一個 tuple 型別：

```rust
fn clone_pair<T, U>(a: &T, b: &U) -> (T, U)
where
    // 編譯器知道 (T, U): Clone 代表 T: Clone 和 U: Clone
    // 所以我們也能呼叫 a.clone() 和 b.clone()
    (T, U): Clone,
{
    let pair = (a.clone(), b.clone());
    pair
}
```

`(T, U): Clone` 這種寫法只能出現在 `where` 子句裡，不能放在 `<>` 裡。

當你寫 `(T, U): Clone` 時，編譯器知道這隱含了 `T: Clone` 和 `U: Clone`——因為 tuple 要能 clone，裡面的每個元素都必須能 clone。

## 範例程式碼

```rust
use std::fmt::Display;

// 多個 trait bound：Clone + Display
// clone 一份，印出原始值，然後回傳複製品
fn clone_and_show<T: Clone + Display>(x: &T) -> T {
    println!("複製了：{}", x);
    x.clone()
}

// 用 where 子句：有時候比較好讀
fn show_pair<T, U>(a: &T, b: &U)
where
    T: Display,
    U: Display,
{
    println!("a = {}, b = {}", a, b);
}

fn main() {
    // 多個 trait bound
    let cloned = clone_and_show(&42);
    println!("拿到的複製品：{}", cloned);

    let cloned2 = clone_and_show(&String::from("hello"));
    println!("拿到的複製品：{}", cloned2);

    // where 子句
    show_pair(&10, &"world");
}
```

## 重點整理
- 用 `+` 組合多個 trait bound：`T: Clone + Display`
- `where` 子句是另一種寫 trait bound 的方式，更好讀
- `where` 比角括號更靈活，冒號前面可以放 tuple 等複雜型別（如 `(T, U): Clone`）
