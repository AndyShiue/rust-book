# 第六章第 13 集：組合與截取

## 本集目標
學會用 `.zip()`、`.chain()`、`.take()`、`.skip()`、`.flatten()`、`.flat_map()` 來組合和截取迭代器。

## 概念說明

### .zip() —— 把兩個迭代器配對

`zip` 把兩個迭代器「拉鍊式」地配對起來，產出 tuple：

```rust
let names = vec!["Alice", "Bob", "Charlie"];
let scores = vec![90, 85, 92];
let paired: Vec<_> = names.iter().zip(scores.iter()).collect();
// [("Alice", 90), ("Bob", 85), ("Charlie", 92)]
```

如果兩個迭代器長度不同，`zip` 在較短的那個結束時就停止。

### .chain() —— 串接兩個迭代器

`chain` 把兩個迭代器首尾相接：

```rust
let first = vec![1, 2, 3];
let second = vec![4, 5, 6];
let all: Vec<i32> = first.into_iter().chain(second.into_iter()).collect();
// [1, 2, 3, 4, 5, 6]
```

### .take(n) —— 只取前 n 個

```rust
let first_three: Vec<i32> = (1..=100).take(3).collect();
// [1, 2, 3]
```

`take` 特別適合用在無限迭代器上——沒有 `take`，無限迭代器永遠不會結束。

### .skip(n) —— 跳過前 n 個

```rust
let after_skip: Vec<i32> = (1..=10).skip(7).collect();
// [8, 9, 10]
```

### .flatten() —— 把巢狀結構攤平

如果迭代器的元素本身也是迭代器（或 `Option`、`Vec` 等），`flatten` 可以把它攤平一層：

```rust
let nested = vec![vec![1, 2], vec![3, 4], vec![5]];
let flat: Vec<i32> = nested.into_iter().flatten().collect();
// [1, 2, 3, 4, 5]
```

`Option` 也可以 flatten——`Some(value)` 被取出，`None` 被忽略：

```rust
let options = vec![Some(1), None, Some(3), None, Some(5)];
let values: Vec<i32> = options.into_iter().flatten().collect();
// [1, 3, 5]
```

### .flat_map() —— map + flatten

`flat_map` 等於先 `map` 再 `flatten`。每個元素經過閉包轉換成一個迭代器（或 Option/Result），然後全部攤平：

```rust
let words = vec!["hello world", "foo bar"];
let chars: Vec<char> = words.iter().flat_map(|s| s.chars()).collect();
// ['h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd', ' ', 'f', 'o', 'o', ' ', 'b', 'a', 'r']
```

還記得第 6 集的 `Option::and_then` 和 `Result::and_then` 嗎？`flat_map` 在迭代器上做的事情本質上一樣——「轉換，但如果轉換結果本身是容器，就攤平它」。

## 範例程式碼

```rust
fn main() {
    // .zip() —— 名字和分數配對
    let students = vec!["小明", "小華", "小美"];
    let grades = vec![88, 95, 72];
    println!("--- zip ---");
    for (name, grade) in students.iter().zip(grades.iter()) {
        println!("{}：{} 分", name, grade);
    }

    // .chain() —— 串接兩個 Vec
    let morning = vec!["開會", "寫報告"];
    let afternoon = vec!["寫程式", "code review"];
    let all_tasks: Vec<&&str> = morning.iter().chain(afternoon.iter()).collect();
    println!("\n今日行程：{:?}", all_tasks);

    // .take() 和 .skip()
    let numbers: Vec<i32> = (1..=20).collect();
    let first_five: Vec<&i32> = numbers.iter().take(5).collect();
    let last_five: Vec<&i32> = numbers.iter().skip(15).collect();
    println!("\n前 5 個：{:?}", first_five);
    println!("跳過 15 個後：{:?}", last_five);

    // .take() + .skip() 組合：取中間的
    let middle: Vec<&i32> = numbers.iter().skip(5).take(5).collect();
    println!("第 6~10 個：{:?}", middle);

    // .flatten() —— 攤平巢狀 Vec
    let matrix = vec![
        vec![1, 2, 3],
        vec![4, 5, 6],
        vec![7, 8, 9],
    ];
    let flat: Vec<i32> = matrix.into_iter().flatten().collect();
    println!("\n攤平矩陣：{:?}", flat);

    // .flatten() —— 過濾 Option
    let maybe_values = vec![Some(10), None, Some(30), None, Some(50)];
    let real_values: Vec<i32> = maybe_values.into_iter().flatten().collect();
    println!("有值的：{:?}", real_values);

    // .flat_map() —— 每個字拆成字元
    let words = vec!["Rust", "好棒"];
    let all_chars: Vec<char> = words.iter().flat_map(|w| w.chars()).collect();
    println!("\n所有字元：{:?}", all_chars);

    // .flat_map() 類似 and_then
    let inputs = vec!["42", "not_a_number", "7"];
    let parsed: Vec<i32> = inputs
        .iter()
        .flat_map(|s| s.parse::<i32>())
        .collect();
    println!("成功解析的：{:?}", parsed);

    // .zip() + .map() 組合
    println!("\n--- zip + map ---");
    let prices = vec![100, 200, 300];
    let quantities = vec![2, 1, 4];
    let grand_total: i32 = prices.iter()
        .zip(quantities.iter())
        .map(|(p, q)| p * q)
        .sum();
    println!("總計：{}", grand_total);
}
```

## 重點整理
- `.zip()` 把兩個迭代器配對成 tuple，以較短的為準
- `.chain()` 把兩個迭代器首尾串接
- `.take(n)` 只取前 n 個元素，`.skip(n)` 跳過前 n 個
- `.flatten()` 把巢狀結構攤平一層（Vec<Vec<T>> → Vec<T>，也適用於 Option）
- `.flat_map()` = `.map()` + `.flatten()`，概念上跟 Option/Result 的 `and_then` 類似
- 這些方法可以自由組合，打造出強大的資料處理管道
