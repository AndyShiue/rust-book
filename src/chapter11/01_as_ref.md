# AsRef / AsMut

## 本集目標

學會用 `AsRef` 和 `AsMut` 讓函數接受多種型別。

## 概念說明

### 動機

假設你寫了一個函數接受 `&str`：

```rust,noplayground
fn print_length(s: &str) {
    println!("長度：{}", s.len());
}
#
# fn main() {}
```

呼叫者手上有 `String`，因為 Deref 的關係，`&String` 會自動轉成 `&str`，所以沒問題。但如果你想寫一個函數，讓它同時接受 `String`、`&str`、甚至其他型別呢？

### AsRef

`AsRef<T>` trait 表示「我能便宜地借用成 `&T`」：

```rust
fn print_length(s: impl AsRef<str>) {
    println!("長度：{}", s.as_ref().len());
}

fn main() {
    print_length("hello");            // &str
    print_length(String::from("hi")); // String
}
```

標準庫已經幫很多型別實作了 `AsRef`：

- `String: AsRef<str>`
- `String: AsRef<[u8]>`
- `Vec<T>: AsRef<[T]>`

### AsMut

`AsMut<T>` 是可變版本，借用成 `&mut T`：

```rust
fn fill_zeros(buf: &mut impl AsMut<[u8]>) {
    for byte in buf.as_mut() {
        *byte = 0;
    }
}

fn main() {
    let mut v = vec![1, 2, 3];
    fill_zeros(&mut v);
    println!("{:?}", v); // [0, 0, 0]
}
```

### 跟 Deref 的差別

Deref 是自動的——編譯器幫你加 `*`，你不用寫任何東西。AsRef 是手動呼叫 `.as_ref()`。

更重要的差別：每個型別只能有一個 Deref 目標（`String` deref 成 `str`），但可以實作多個 AsRef（`String` 同時是 `AsRef<str>` 和 `AsRef<[u8]>`）。

### 什麼時候用

寫函數參數想泛化接受多種型別的時候，用 `impl AsRef<T>`。標準庫到處都在用。

## 範例程式碼

```rust
fn describe(s: impl AsRef<str>) {
    let s = s.as_ref();
    println!("「{}」有 {} 個字元", s, s.chars().count());
}

fn count_bytes(data: impl AsRef<[u8]>) {
    println!("共 {} bytes", data.as_ref().len());
}

fn main() {
    // AsRef<str>：接受 &str 和 String
    describe("hello");
    describe(String::from("你好"));

    // AsRef<[u8]>：接受 Vec<u8>、String 等
    count_bytes(vec![1, 2, 3]);
    count_bytes(String::from("hi"));
}
```

## 重點整理

- `AsRef<T>`：便宜地借用成 `&T`，用 `.as_ref()` 呼叫
- `AsMut<T>`：便宜地借用成 `&mut T`，用 `.as_mut()` 呼叫
- 一個型別可以實作多個 `AsRef`（Deref 只能一個目標）
- 函數參數寫 `impl AsRef<T>` 可以接受多種型別
- 標準庫大量使用
