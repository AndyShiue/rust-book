# 附錄第 k 集：DST 簡介

## 本集目標

理解什麼是動態大小型別（DST），以及 `Sized`、`?Sized` 在泛型中的意義。

> 本集是**第五章**的補充。

## 概念說明

在 Rust 的型別系統裡，大部分型別的大小在編譯期就已知——`i32` 是 4 bytes、`bool` 是 1 byte、`(i32, i32)` 是 8 bytes。但有些型別的大小**在編譯期是未知的**，這就是 **DST（Dynamically Sized Types）**，動態大小型別。

### 常見的 DST

你其實已經見過它們了：

- **`str`**：字串切片的「內容」型別。`"hello"` 是 5 bytes，`"哈囉"` 是 6 bytes，長度不固定。
- **`[T]`**：陣列切片的「內容」型別。`[i32]` 可能是 3 個元素也可能是 100 個。

因為大小不固定，你**不能**直接把它們當作值使用：

```rust
// let s: str = "hello";        // 編譯錯誤！
// let arr: [i32] = [1, 2, 3];  // 編譯錯誤！
```

### 怎麼用？靠指標！

DST 必須藏在某種指標後面：

- `&str`、`&[T]` — 參考
- `Box<str>`、`Box<[T]>` — 堆積上的指標

這些指標是所謂的**胖指標（fat pointer）**——它們不只存一個位址，還多存了一個長度資訊：

```
一般指標：[位址]           （8 bytes）
胖指標：  [位址][長度]      （16 bytes）
```

所以 `&str` 實際上佔 16 bytes：8 bytes 指向字串資料，8 bytes 記錄長度。

### `Sized` trait

Rust 有一個特殊的 trait 叫 `Sized`，表示「這個型別的大小在編譯期已知」。**絕大多數型別都自動實作了 `Sized`**。

而且——這是很多人不知道的——**泛型參數預設有 `Sized` bound**：

```rust
fn print_it<T>(val: T) { ... }
// 其實等同於
fn print_it<T: Sized>(val: T) { ... }
```

這很合理，因為如果 `T` 的大小未知，函式根本不知道要在 stack 上分配多少空間。

### `?Sized`：放寬限制

有時候你希望泛型參數可以接受 DST，這時候用 `?Sized` 來放寬限制：

```rust
fn print_it<T: ?Sized>(val: &T) { ... }
//                     ^^^^^^^ 注意：必須透過參考
```

`?Sized` 的意思是「`T` 可以是 `Sized`，也可以不是」。但因為大小可能未知，你只能透過參考或指標來使用 `T`。

### 回頭看第五章的 Cow

第五章最後一集教 `Cow` 的時候，我們用的是簡化版的定義：

```rust
// 第五章提供的簡化版
pub enum Cow<'a, B>
where
    B: 'a + ToOwned,
{
    Borrowed(&'a B),
    Owned(B::Owned),
}
```

如果你試過要把 `str` 或 `[T]` 放進 `Cow`——例如寫 `Cow<str>`——你會發現編譯不過。因為泛型參數 `B` 預設要求 `Sized`，而 `str` 不是 `Sized`。

加上 `?Sized` 就能解決：

```rust
pub enum Cow<'a, B>
where
    B: 'a + ToOwned + ?Sized,
{
    Borrowed(&'a B),
    Owned(B::Owned),
}
```

`Borrowed(&'a B)` 裡的 `B` 已經在參考後面，所以即使 `B` 是 DST 也沒問題——胖指標會幫你搞定。

### `&mut [T]` 與 `&mut str`

DST 也可以拿可變參考。`&mut [T]` 很實用——你可以修改切片裡的元素：

```rust
let mut arr = [1, 2, 3, 4, 5];
let slice: &mut [i32] = &mut arr[1..4];
slice[0] = 99;  // arr 變成 [1, 99, 3, 4, 5]
```

但 `&mut str` 就很沒用了。雖然語法上合法，但你幾乎做不了什麼。原因是 UTF-8 編碼裡，一個字元可能佔 1~4 bytes：

- `'a'` → 1 byte
- `'é'` → 2 bytes
- `'哈'` → 3 bytes

假設你有 `"哈囉"`（6 bytes），想把 `'哈'` 改成 `'a'`——`'a'` 只有 1 byte，但 `'哈'` 佔了 3 bytes，你沒辦法就地替換，因為長度不同。如果硬改了第一個 byte 卻沒處理後面的，UTF-8 的多 byte 序列就斷了。而 Rust 的 `str` 保證內容一定是合法的 UTF-8，破壞這個保證會導致未定義行為。

所以標準庫裡 `&mut str` 上的方法少得可憐，基本上只有 `make_ascii_uppercase()` 和 `make_ascii_lowercase()` 這類「不會改變 byte 長度」的操作（ASCII 字母的大小寫轉換剛好是 1 byte 對 1 byte）。要修改字串，還是用 `String` 吧。

## 範例程式碼

```rust
use std::fmt::Display;

// 預設：T 必須是 Sized
fn print_sized<T: Display>(val: T) {
    println!("Sized 值：{}", val);
}

// 放寬：T 可以是 DST，但必須透過參考
fn print_unsized<T: Display + ?Sized>(val: &T) {
    println!("可能是 DST：{}", val);
}

// 展示胖指標大小
fn show_pointer_sizes() {
    use std::mem::size_of;

    println!("--- 指標大小比較 ---");
    println!("&i32      = {} bytes", size_of::<&i32>());     // 8
    println!("&[i32]    = {} bytes", size_of::<&[i32]>());   // 16（胖指標）
    println!("&str      = {} bytes", size_of::<&str>());     // 16（胖指標）
    println!("Box<i32>  = {} bytes", size_of::<Box<i32>>()); // 8
    println!("Box<str>  = {} bytes", size_of::<Box<str>>()); // 16（胖指標）
}

fn main() {
    // Sized 值：一般型別
    print_sized(42);
    print_sized(String::from("hello"));

    // ?Sized：可以接受 &str（str 是 DST）
    print_unsized("hello");       // T = str（DST）
    print_unsized(&42);           // T = i32（Sized，也可以）
    print_unsized(&String::from("world"));  // T = String（Sized）

    // &str 和 &[T] 是胖指標
    show_pointer_sizes();

    // str 和 [T] 不能直接當值用
    // let s: str = *"hello";    // 編譯錯誤！
    // let a: [i32] = *&[1,2,3]; // 編譯錯誤！

    // 但透過參考就沒問題
    let s: &str = "hello";
    let a: &[i32] = &[1, 2, 3];
    println!("\n&str = {}", s);
    println!("&[i32] 長度 = {}", a.len());

    // Box<str> 也可以
    let boxed: Box<str> = String::from("boxed string").into_boxed_str();
    println!("Box<str> = {}", boxed);
}
```

## 重點整理

- **DST（Dynamically Sized Types）**：大小在編譯期未知的型別，如 `str`、`[T]`
- DST 不能直接當值使用，必須透過指標：`&str`、`&[T]`、`Box<str>` 等
- 指向 DST 的指標是**胖指標（fat pointer）**：位址 + 長度，佔 16 bytes
- **`Sized`**：表示型別大小在編譯期已知；泛型參數預設有 `T: Sized` bound
- **`?Sized`**：放寬限制，讓泛型參數可以接受 DST（但必須透過參考使用）
- `Cow<'a, B>` 中的 `B: ?Sized` 就是為了讓 `B` 可以是 `str` 等 DST
