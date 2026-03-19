# 第六章第 7 集：Iterator trait

## 本集目標
認識 `Iterator` trait 的核心——只要實作 `next()` 方法，就能免費獲得數十個好用的方法。

## 概念說明

### Iterator 的定義

`Iterator` trait 的核心簡單到不行：

```rust
trait Iterator {
    type Item;
    fn next(&mut self) -> Option<Self::Item>;
}
```

就這樣。只有一個必須實作的方法 `next()`，它每次被呼叫就回傳：
- `Some(值)` —— 還有下一個元素
- `None` —— 迭代結束了

還記得第五章學的 associated type 嗎？`type Item` 就是一個 associated type，代表「這個迭代器產出的元素型別」。

### 手動呼叫 next

你可以直接手動呼叫 `next()` 來逐一取得元素：

```rust
let v = vec![10, 20, 30];
let mut iter = v.iter();

println!("{:?}", iter.next());  // Some(&10)
println!("{:?}", iter.next());  // Some(&20)
println!("{:?}", iter.next());  // Some(&30)
println!("{:?}", iter.next());  // None
```

注意 `iter` 必須是 `mut` 的，因為每次呼叫 `next()` 都會推進內部狀態。

### 只需實作 next，其他方法免費送

`Iterator` trait 提供了大量的 **default method**（還記得第五章嗎？）。因為所有的迭代操作本質上都是「不斷呼叫 next 直到 None」，所以只要你實作了 `next()`，像 `map`、`filter`、`count`、`sum` 等幾十個方法全部自動可用。

這就是 trait default method 的威力！

### 自訂 Iterator

讓我們自己做一個迭代器。假設我們想要一個「倒數計時器」：

```rust
struct Countdown {
    value: i32,
}

impl Iterator for Countdown {
    type Item = i32;

    fn next(&mut self) -> Option<i32> {
        if self.value > 0 {
            let current = self.value;
            self.value -= 1;
            Some(current)
        } else {
            None
        }
    }
}
```

只要實作了 `next()`，就能用 for 迴圈、用 `collect()`、用 `map()`——全部都行。

### 標準庫的迭代器工廠

標準庫提供了一些方便的函數來建立迭代器：

- `std::iter::repeat(value)` —— 無限重複同一個值
- `std::iter::from_fn(closure)` —— 用閉包來決定每次 `next()` 回傳什麼

```rust
use std::iter;

// 無限產生 42
let mut repeater = iter::repeat(42);
println!("{:?}", repeater.next());  // Some(42)
println!("{:?}", repeater.next());  // Some(42)（永遠不會 None）

// 用閉包產生遞增數字
let mut n = 0;
let mut counter = iter::from_fn(move || {
    n += 1;
    Some(n)
});
println!("{:?}", counter.next());  // Some(1)
println!("{:?}", counter.next());  // Some(2)
```

注意 `repeat` 和 `from_fn` 產生的迭代器可能是**無限的**——永遠不會回傳 None。第 14 集會深入討論這個特性。

## 範例程式碼

```rust
use std::iter;

// 自訂迭代器：產生費氏數列
struct Fibonacci {
    a: u64,
    b: u64,
}

impl Fibonacci {
    fn new() -> Fibonacci {
        Fibonacci { a: 0, b: 1 }
    }
}

impl Iterator for Fibonacci {
    type Item = u64;

    fn next(&mut self) -> Option<u64> {
        let current = self.a;
        let new_b = self.a + self.b;
        self.a = self.b;
        self.b = new_b;
        Some(current)  // 費氏數列永遠不結束
    }
}

fn main() {
    // 手動呼叫 next
    let names = vec!["Alice", "Bob", "Charlie"];
    let mut name_iter = names.iter();
    println!("第一個：{:?}", name_iter.next());
    println!("第二個：{:?}", name_iter.next());
    println!("第三個：{:?}", name_iter.next());
    println!("結束了：{:?}", name_iter.next());

    // 自訂 Iterator：費氏數列（取前 10 個）
    println!("\n費氏數列前 10 個：");
    let fib = Fibonacci::new();
    for n in fib.take(10) {
        print!("{} ", n);
    }
    println!();

    // std::iter::repeat
    let threes: Vec<i32> = iter::repeat(3).take(5).collect();
    println!("\n重複 5 個 3：{:?}", threes);

    // std::iter::from_fn
    let mut count = 0;
    let squares: Vec<i32> = iter::from_fn(|| {
        count += 1;
        if count <= 5 {
            Some(count * count)
        } else {
            None
        }
    }).collect();
    println!("前 5 個平方數：{:?}", squares);

    // 自訂 Iterator 自動獲得所有 default method
    let fib_sum: u64 = Fibonacci::new().take(10).sum();
    println!("\n費氏前 10 項的和：{}", fib_sum);

    let fib_count = Fibonacci::new().take(20).filter(|n| n % 2 == 0).count();
    println!("費氏前 20 項中偶數的個數：{}", fib_count);
}
```

## 重點整理
- `Iterator` trait 的核心是 `next(&mut self) -> Option<Self::Item>`
- 只需實作 `next()`，就能免費獲得 `map`、`filter`、`sum`、`count` 等數十個方法（trait default method 的威力）
- 自訂 struct 實作 `Iterator` 很簡單——定義 `type Item` 和 `next()` 就好
- `std::iter::repeat(value)` 建立無限重複的迭代器
- `std::iter::from_fn(closure)` 用閉包來控制每次產出的值
- 迭代器可以是無限的（永不回傳 None），用 `.take(n)` 取有限個
