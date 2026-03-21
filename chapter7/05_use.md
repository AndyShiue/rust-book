# 第七章第 5 集：use

## 本集目標

學會用 `use` 簡化路徑，理解 Rust 的路徑解析規則和各種匯入方式。

## 概念說明

在前面我們已經初步接觸過 `use`，這裡要把所有用法和路徑規則講完整。

### 為什麼需要 use

每次呼叫都寫完整路徑很累：

```rust
let sum = crate::math::basic::add(1, 2);
let diff = crate::math::basic::subtract(5, 3);
```

用 `use` 把路徑帶進來，之後就能直接用短名稱：

```rust
use crate::math::basic::add;
use crate::math::basic::subtract;

let sum = add(1, 2);
let diff = subtract(5, 3);
```

### 絕對路徑 vs 相對路徑

Rust 有兩種路徑起點：

**絕對路徑**——從 crate root 開始：

```rust
use crate::math::add;     // 自己這個 crate 裡的 math mod
```

**相對路徑**——從當前 mod 的位置開始：

```rust
use math::add;             // 當前 mod 底下的 math 子 mod
```

### 外部 crate 的路徑

在 Cargo.toml 加了外部 crate 後，直接用 crate 名稱作為路徑開頭：

```rust
use rand::Rng;
use std::collections::HashMap;
```

`std` 是標準函式庫，不需要在 Cargo.toml 加 dependency，但使用時路徑規則一樣。

如果你想明確強調「這是外部 crate」，可以用 `::` 開頭：

```rust
use ::rand::Rng;  // 明確表示 rand 是外部 crate，不是本地 mod
```

這在你的 crate 裡也有一個叫 `rand` 的 mod 時特別有用，可以避免歧義。

### super:: 和 self::

- `super::`：往上一層，指向**父 mod**
- `self::`：指向**當前 mod**（通常省略，但有時在 `use` 中有用）

```rust
mod outer {
    pub fn greet() -> String {
        String::from("Hello from outer")
    }

    pub mod inner {
        pub fn call_parent() -> String {
            super::greet()  // 呼叫父 mod 的 greet
        }
    }
}
```

### 巢狀匯入

匯入同一個路徑底下的多個東西，可以用大括號合併：

```rust
use std::io::{self, Read, Write};
// 等同於：
// use std::io;
// use std::io::Read;
// use std::io::Write;
```

`self` 在這裡代表 `std::io` 本身，所以你既匯入了 `io` 這個 mod，也匯入了裡面的 `Read` 和 `Write`。

### use ... as（別名）

如果兩個不同地方有同名的東西，可以用 `as` 取別名：

```rust
use std::fmt::Result as FmtResult;
use std::io::Result as IoResult;

fn format_something() -> FmtResult {
    Ok(())
}

fn read_something() -> IoResult<()> {
    Ok(())
}
```

### glob import（星號匯入）

`*` 會把 mod 底下所有 pub 的東西全部帶進來：

```rust
use std::collections::*;  // HashMap, BTreeMap, HashSet... 全部可用
```

**一般不推薦**在正式程式碼裡用，因為不清楚到底帶了什麼進來，容易衝突。但在**測試**裡很常見——`use super::*;` 可以把父 mod 的所有東西帶進測試 mod。下一集我們會教怎麼用 `cargo test` 寫測試，到時候就會看到這個用法。

### Prelude：為什麼有些東西不需要 use

你有沒有注意到，`Vec`、`String`、`Option`、`Result`、`println!` 這些東西從來不需要 `use`？

因為 Rust 有一個 **prelude**——一組「預設已經 use 進來」的常用型別和 trait。每個 Rust 檔案開頭都隱含了類似這樣的東西：

```rust
use std::prelude::*;  // 實際的路徑會隨 Rust edition 不同而變
```

這就是為什麼 `Vec`、`Option`、`Some`、`None`、`Ok`、`Err`、`String`、`Clone`、`Copy` 等等可以直接使用。不同的 edition（2021、2024 等）prelude 裡包含的東西可能略有不同。

## 範例程式碼

```rust
mod math {
    pub mod basic {
        pub fn add(a: i32, b: i32) -> i32 {
            a + b
        }

        pub fn subtract(a: i32, b: i32) -> i32 {
            a - b
        }
    }

    pub mod advanced {
        pub fn power(base: i32, exp: u32) -> i32 {
            let mut result = 1;
            let mut i = 0;
            while i < exp {
                result *= base;
                i += 1;
            }
            result
        }

        pub fn factorial(n: u64) -> u64 {
            let mut result: u64 = 1;
            let mut i: u64 = 1;
            while i <= n {
                result *= i;
                i += 1;
            }
            result
        }
    }
}

// 各種 use 的方式
use math::basic::add;
use math::basic::subtract;
use math::advanced::{power, factorial};

fn main() {
    println!("3 + 5 = {}", add(3, 5));
    println!("10 - 4 = {}", subtract(10, 4));
    println!("2^10 = {}", power(2, 10));
    println!("10! = {}", factorial(10));
}
```

## 重點整理

- `use` 將路徑帶入作用域，讓你不必每次寫完整路徑
- 絕對路徑用 `crate::` 開頭，相對路徑從當前 mod 位置開始
- 外部 crate 直接用名稱開頭；加 `::` 前綴可以明確標記為外部 crate
- `super::` 指向父 mod，`self::` 指向當前 mod
- `use a::b::{X, Y, self};` 巢狀匯入多個項目
- `use X as Alias;` 解決名稱衝突
- `use something::*;` 星號匯入——測試裡常用，正式程式碼少用
- 常用型別如 `Vec`、`Option` 透過 prelude 自動可用，不需 `use`
