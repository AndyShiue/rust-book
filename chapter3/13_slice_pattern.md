# 第三章第 13 集：slice Pattern

## 本集目標
學會在 match 裡解構陣列和切片，用 slice pattern 取出元素。

## 概念說明

### 在 match 裡解構陣列

上一集我們學了在 match 裡解構 tuple，其實陣列和切片也可以！語法就是用 `[a, b, c]` 來比對陣列的每個元素：

```rust
let rgb = [255, 128, 0];

match rgb {
    [255, 0, 0] => println!("純紅色"),
    [0, 255, 0] => println!("純綠色"),
    [0, 0, 255] => println!("純藍色"),
    [r, g, b] => println!("自訂顏色：R={}, G={}, B={}", r, g, b),
}
```

跟 tuple pattern 很像，你可以在模式裡混用「固定的值」和「變數」。固定的值用來比對，變數用來接住資料。

### 部分位置用固定值

你可以只固定某些位置，其餘用變數接住：

```rust
let point = [0, 5, 3];

match point {
    [0, y, z] => println!("在 YZ 平面上：y={}, z={}", y, z),
    [x, 0, z] => println!("在 XZ 平面上：x={}, z={}", x, z),
    [x, y, 0] => println!("在 XY 平面上：x={}, y={}", x, y),
    [x, y, z] => println!("一般的點：({}, {}, {})", x, y, z),
}
```

### 切片也能用

不只固定長度的陣列，切片（`&[T]`）也能用 slice pattern。差別在於切片的長度在編譯期是未知的，所以你可以用不同長度的模式來匹配：

```rust
fn describe(numbers: &[i32]) {
    match numbers {
        [] => println!("空的"),
        [x] => println!("只有一個元素：{}", x),
        [x, y] => println!("兩個元素：{} 和 {}", x, y),
        [x, y, z] => println!("三個元素：{}, {}, {}", x, y, z),
        _ => println!("超過三個元素"),
    }
}
```

固定長度的陣列（例如 `[i32; 3]`）永遠是那個長度，所以 `[]` 或 `[x]` 的分支永遠不會匹配到。切片才需要考慮不同長度的情況。

## 範例程式碼

```rust
fn describe(data: &[i32]) {
    match data {
        [] => println!("空的切片"),
        [only] => println!("只有一個元素：{}", only),
        [first, second] => println!("兩個元素：{} 和 {}", first, second),
        _ => println!("有很多元素，第一個是 {}", data[0]),
    }
}

fn main() {
    // 固定長度陣列的 slice pattern
    let rgb = [255, 128, 0];

    match rgb {
        [255, 0, 0] => println!("純紅色"),
        [0, 255, 0] => println!("純綠色"),
        [0, 0, 255] => println!("純藍色"),
        [r, g, b] => println!("自訂顏色：R={}, G={}, B={}", r, g, b),
    }

    println!("---");

    // 切片的 slice pattern——可以匹配不同長度
    describe(&[]);
    describe(&[42]);
    describe(&[1, 2]);
    describe(&[10, 20, 30, 40, 50]);
}
```

## 重點整理
- 陣列可以在 match 裡用 `[a, b, c]` 解構，跟 tuple pattern 類似
- 模式裡可以混用固定值和變數
- 切片 `&[T]` 長度不固定，可以用不同長度的模式來匹配（`[]`、`[x]`、`[x, y]`……）
