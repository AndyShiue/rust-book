# 第六章第 11 集：收集

## 本集目標
學會用 `.collect()` 把迭代器收集成各種集合型別，以及用 turbofish 語法指定目標型別。

## 概念說明

平常我們不會花這麼多集數在介紹方法，但迭代器實在太重要了——它是 Rust 日常寫程式碼最常用的工具之一，所以接下來幾集會多花點時間。不過就算介紹了很多方法，一定還是會漏掉不少。有需要的話，請參考[官方文件的 Iterator trait 頁面](https://doc.rust-lang.org/std/iter/trait.Iterator.html)。

### collect() —— 迭代器的終點站

前幾集我們建立了迭代器、做了轉換和過濾，但迭代器本身是**惰性的**（第 15 集會詳細講）——它不會真的執行，直到有人「拉動」它。`.collect()` 就是最常用的拉動方式：把迭代器的所有元素收集成一個集合。

```rust
let v: Vec<i32> = (1..=5).collect();
```

你可能注意到了——`1..=5` 是第一章學的 range 語法，它也實作了 `Iterator`！所以可以直接對它呼叫 `.collect()` 和其他迭代器方法。

### Turbofish 語法

`.collect()` 的回傳型別取決於你要收集成什麼。Rust 通常需要你告訴它目標型別。有兩種方式：

**方式一：型別標註**
```rust
let v: Vec<i32> = (1..=5).collect();
```

**方式二：Turbofish `::<>`**
```rust
let v = (1..=5).collect::<Vec<i32>>();
```

兩種寫法效果一樣，看個人偏好。鏈式呼叫的時候 turbofish 比較方便，因為不用另外宣告變數。

### 收集成 String

`collect()` 不只能收集成 Vec。如果迭代器產出的是 `char` 或 `&str`，可以直接收集成 `String`：

```rust
let chars = vec!['R', 'u', 's', 't'];
let word: String = chars.into_iter().collect();
println!("{}", word);  // "Rust"
```

### .last() —— 取最後一個元素

`.last()` 會消耗整個迭代器，回傳最後一個元素（`Option<T>`）：

```rust
let v = vec![10, 20, 30];
let last = v.iter().last();
println!("{:?}", last);  // Some(&30)
```

注意它需要走完整個迭代器才能知道最後一個是什麼。

## 範例程式碼

```rust
fn main() {
    // 基本 collect —— Range 轉 Vec
    let numbers: Vec<i32> = (1..=10).collect();
    println!("1 到 10：{:?}", numbers);

    // turbofish 語法
    let numbers2 = (1..=5).collect::<Vec<i32>>();
    println!("turbofish：{:?}", numbers2);

    // 收集成 String
    let greeting: String = vec!['你', '好', '世', '界'].into_iter().collect();
    println!("字串：{}", greeting);

    // .last()
    let last_num = (1..=100).last();
    println!("\n1..=100 的最後一個：{:?}", last_num);

    let empty: Vec<i32> = vec![];
    let last_empty = empty.iter().last();
    println!("空 Vec 的 last：{:?}", last_empty);
}
```

## 重點整理
- `.collect()` 把迭代器的元素收集成目標集合型別
- 用型別標註 `let v: Vec<i32>` 或 turbofish `.collect::<Vec<i32>>()` 告訴 Rust 目標型別
- 可以收集成 `Vec`、`String` 等多種型別
- `.last()` 消耗整個迭代器，回傳 `Option` 包裝的最後一個元素
