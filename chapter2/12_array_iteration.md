# 第二章第 12 集：陣列走訪

## 本集目標
用 `for` 迴圈走過陣列裡的每一個元素。

## 正文

上一集我們學了怎麼用 `arr[0]`、`arr[1]` 一個一個取值。但如果陣列有 100 個元素，總不能寫 100 行吧？這時候就要用 `for` 迴圈來**走訪**（iterate）整個陣列。

### 基本語法

```rust
fn main() {
    let arr = [1, 2, 3, 4, 5];

    for x in arr {
        println!("{}", x);
    }
}
```

結果：
```
1
2
3
4
5
```

`for x in arr` 的意思是：「把 arr 裡的元素一個一個拿出來，每次放進 x，然後執行大括號裡的程式碼。」

### 幫元素做運算

```rust
fn main() {
    let scores = [80, 95, 72, 88, 100];

    for score in scores {
        if score >= 90 {
            println!("{} 分 → 優秀！", score);
        } else {
            println!("{} 分 → 加油！", score);
        }
    }
}
```

結果：
```
80 分 → 加油！
95 分 → 優秀！
72 分 → 加油！
88 分 → 加油！
100 分 → 優秀！
```

### 加總所有元素

```rust
fn main() {
    let arr = [1, 2, 3, 4, 5];
    let mut total = 0;

    for x in arr {
        total += x;
    }

    println!("總和：{}", total);
}
```

結果：
```
總和：15
```

先用 `let mut total = 0;` 建立一個可變的累加器，每次迴圈把值加上去。

### for 和 while 的差別

上一章學了 `while` 迴圈。走訪陣列的時候：

```rust
fn main() {
    let arr = [1, 2, 3, 4, 5];

    // 用 while（比較囉嗦，而且容易寫錯索引）
    let mut i = 0;
    while i < 5 {
        println!("{}", arr[i]);
        i += 1;
    }

    // 用 for（簡潔、安全、不會越界）
    for x in arr {
        println!("{}", x);
    }
}
```

走訪陣列的時候，`for` 比 `while` 好太多了——更短、更安全、不用自己管索引。

## 重點整理

- `for x in arr { ... }` 走訪陣列的每個元素
- 可以在迴圈裡對每個元素做運算、判斷、累加
- 走訪陣列時，`for` 比 `while` 更簡潔、更安全
