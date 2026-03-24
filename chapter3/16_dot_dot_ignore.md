# 第三章第 16 集：`..` 忽略多個值

## 本集目標
學會用 `..` 一次忽略 struct 或 tuple 中多個不關心的值。

## 概念說明

上一集學了用 `_` 忽略一個值。但如果一個 struct 有很多欄位，而你只關心其中一兩個呢？每個不要的都寫 `_` 太麻煩了。

Rust 提供了 `..`（兩個點），意思是「剩下的我都不要了」：

```rust
struct Point {
    x: i32,
    y: i32,
}

let p = Point { x: 5, y: 10 };
let Point { x, .. } = p;  // 只取 x，忽略其他所有欄位
println!("{}", x);  // 5
```

`..` 也可以用在 tuple 上：

```rust
let t = (1, 2, 3, 4, 5);
let (first, ..) = t;      // 只取第一個
let (.., last) = t;        // 只取最後一個
let (first, .., last) = t; // 取第一個和最後一個
```

### 陣列和切片也能用

第 13 集學過 slice pattern，`..` 在陣列和切片裡也一樣好用：

```rust
let data: &[i32] = &[10, 20, 30, 40, 50];

match data {
    [first, ..] => println!("第一個是 {}", first),
    [] => println!("空的"),
}
```

也可以同時取頭和尾：

```rust
match data {
    [first, .., last] => println!("頭 = {}，尾 = {}", first, last),
    [only] => println!("只有一個：{}", only),
    [] => println!("空的"),
}
```

注意：`..` 在一個模式裡只能出現一次，因為如果出現兩次，Rust 會不知道中間的值怎麼分配。

## 範例程式碼

```rust
struct Player {
    id: i32,
    hp: i32,
    mp: i32,
    level: i32,
}

fn main() {
    let p = Player { id: 1, hp: 100, mp: 50, level: 10 };

    // 只取 hp，忽略其他欄位
    let Player { hp, .. } = p;
    println!("HP = {}", hp);

    // 在 match 裡也可以用
    let p2 = Player { id: 2, hp: 0, mp: 30, level: 5 };

    match p2 {
        Player { hp: 0, .. } => println!("這個玩家已經倒下了！"),
        Player { level, .. } => println!("等級 {}", level),
    }

    // tuple 上使用 ..
    let scores = (90, 85, 78, 92, 88);

    let (first, ..) = scores;
    println!("第一科：{}", first);

    let (.., last) = scores;
    println!("最後一科：{}", last);

    let (first, .., last) = scores;
    println!("第一科 {}，最後一科 {}", first, last);

    // 切片上使用 ..
    let data: &[i32] = &[10, 20, 30, 40, 50];

    match data {
        [first, .., last] => println!("頭 = {}，尾 = {}", first, last),
        [only] => println!("只有一個：{}", only),
        [] => println!("空的"),
    }
}
```

## 重點整理
- `..` 用來一次忽略多個欄位或值
- struct 裡：`Point { x, .. }` 只取 x，其他全部忽略
- tuple 裡：`(first, ..)` 只取第一個，`(.., last)` 只取最後一個
- 陣列和切片裡：`[first, ..]` 取第一個，`[first, .., last]` 取頭和尾
- `..` 在一個模式裡只能出現一次
- match 分支裡也可以用 `..`
