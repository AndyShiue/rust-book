# 第六章第 10 集：收集

## 本集目標
學會用 `.collect()` 把迭代器收集成各種集合型別，以及用 turbofish 語法指定目標型別。

## 概念說明

### collect() —— 迭代器的終點站

前幾集我們建立了迭代器、做了轉換和過濾，但迭代器本身是**惰性的**（第 14 集會詳細講）——它不會真的執行，直到有人「拉動」它。`.collect()` 就是最常用的拉動方式：把迭代器的所有元素收集成一個集合。

```rust
let v: Vec<i32> = (1..=5).collect();
```

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

Turbofish（`::<>`）是直接在方法呼叫上標註泛型參數，寫在方法名和括號之間。看起來像一隻魚：`::<>`。

兩種寫法效果一樣，看個人偏好。鏈式呼叫的時候 turbofish 比較方便，因為不用另外宣告變數。

### 收集成 String

`collect()` 不只能收集成 Vec。如果迭代器產出的是 `char` 或 `&str`，可以直接收集成 `String`：

```rust
let chars = vec!['R', 'u', 's', 't'];
let word: String = chars.into_iter().collect();
println!("{}", word);  // "Rust"
```

### 收集 Result

一個很酷的用法：如果迭代器的元素是 `Result<T, E>`，你可以 collect 成 `Result<Vec<T>, E>`。只要有任何一個 `Err`，整個結果就是 `Err`：

```rust
let inputs = vec!["1", "2", "three", "4"];
let parsed: Result<Vec<i32>, _> = inputs.iter().map(|s| s.parse::<i32>()).collect();
println!("{:?}", parsed);  // Err(...)，因為 "three" 無法解析
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
    let evens = (1..=10).filter(|n| n % 2 == 0).collect::<Vec<i32>>();
    println!("偶數：{:?}", evens);

    // 收集成 String
    let greeting: String = vec!['你', '好', '世', '界'].into_iter().collect();
    println!("字串：{}", greeting);

    // 用 map + collect 做轉換
    let names = vec!["alice", "bob", "charlie"];
    let uppercased: Vec<String> = names.iter().map(|s| s.to_uppercase()).collect();
    println!("大寫：{:?}", uppercased);

    // collect Result<Vec<T>, E> —— 全部成功
    let inputs_ok = vec!["1", "2", "3", "4"];
    let parsed_ok: Result<Vec<i32>, _> = inputs_ok
        .iter()
        .map(|s| s.parse::<i32>())
        .collect();
    println!("\n全部成功：{:?}", parsed_ok);

    // collect Result<Vec<T>, E> —— 有一個失敗
    let inputs_bad = vec!["1", "two", "3"];
    let parsed_bad: Result<Vec<i32>, _> = inputs_bad
        .iter()
        .map(|s| s.parse::<i32>())
        .collect();
    println!("有失敗：{:?}", parsed_bad);

    // .last()
    let last_num = (1..=100).last();
    println!("\n1..=100 的最後一個：{:?}", last_num);

    let empty: Vec<i32> = vec![];
    let last_empty = empty.iter().last();
    println!("空 Vec 的 last：{:?}", last_empty);

    // 鏈式操作 + collect
    let sentence = "hello world foo bar";
    let long_words: Vec<&str> = sentence
        .split_whitespace()
        .filter(|w| w.len() > 3)
        .collect();
    println!("\n超過 3 字母的單字：{:?}", long_words);
}
```

## 重點整理
- `.collect()` 把迭代器的元素收集成目標集合型別
- 用型別標註 `let v: Vec<i32>` 或 turbofish `.collect::<Vec<i32>>()` 告訴 Rust 目標型別
- 可以收集成 `Vec`、`String`、`Result<Vec<T>, E>` 等多種型別
- 收集 `Result` 時，任何一個 `Err` 就會讓整個結果變成 `Err`
- `.last()` 消耗整個迭代器，回傳 `Option` 包裝的最後一個元素
