# 第五章第 14 集：use 基礎

## 本集目標
學會用 `use` 把長路徑縮短，並理解為什麼之前不用 `use` 就能用 `Option`、`Vec` 等型別。

## 概念說明

你可能已經注意到，我們一直在用 `Vec`、`String`、`Option`、`Result` 這些型別，從來沒有寫過完整路徑。但 Rust 的標準庫其實有很深的模組結構，這些型別的完整路徑像是 `std::vec::Vec`、`std::string::String`、`std::option::Option`。

為什麼不用寫完整路徑？因為 Rust 有一個叫 **prelude** 的機制——Rust 預設就把最常用的型別和 trait 引入到每個檔案裡。`Vec`、`String`、`Option`、`Result`、`Some`、`None`、`Ok`、`Err`，還有 `Clone`、`Copy` 等常用 trait，都在 prelude 裡面。

但不是所有東西都在 prelude 裡。比如 `std::fmt::Display` 這個 trait，就不在 prelude 裡。如果你想用它，就要寫完整路徑——或者用 `use` 把它引入。

### use 的語法

```rust
use std::fmt::Display;
```

這行的意思是：「把 `std::fmt::Display` 引入到當前的作用域，之後直接寫 `Display` 就好。」

`use` 不會引入新功能，它只是讓長路徑變短。沒有 `use`，你寫 `std::fmt::Display`；有了 `use`，你只需要寫 `Display`。

### 為什麼之前不需要 use？

因為我們用的東西幾乎都在 prelude 裡——`Vec`、`String`、`Option`、`Clone` 等等。從下一集開始，我們會用到不在 prelude 裡的東西（像是 `Display`），所以現在學 `use` 剛好。

## 範例程式碼

```rust
use std::mem::size_of;

fn main() {
    // 沒有 use 的話，要寫完整路徑：
    println!("i32 的大小：{} bytes", std::mem::size_of::<i32>());

    // 有了 use，直接寫 size_of 就好：
    println!("bool 的大小：{} bytes", size_of::<bool>());
    println!("f64 的大小：{} bytes", size_of::<f64>());
    println!("char 的大小：{} bytes", size_of::<char>());
}
```

## 重點整理
- `use std::fmt::Display;` 把長路徑縮短，之後直接寫 `Display`
- `use` 只是路徑的簡寫，不引入新功能
- **prelude** 是 Rust 預設引入的常用型別和 trait（Vec、String、Option、Clone 等）
- 不在 prelude 裡的東西（如 Display）需要寫完整路徑或用 `use` 引入
