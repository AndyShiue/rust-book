# 第六章第 7 集：Option / Result 的閉包方法

## 本集目標
用閉包方法重寫第五章的 Option 和 Result 操作，體會閉包如何讓程式碼更簡潔流暢。

## 概念說明

第五章我們用 `match` 處理 `Option` 和 `Result`，每次都要展開兩個分支。現在學了閉包，很多操作可以一行搞定。

### Option 的閉包方法

#### map —— 轉換 Some 裡的值

```rust
let x: Option<i32> = Some(5);
let y = x.map(|v| v * 2);  // Some(10)
```

如果是 `None`，`map` 什麼都不做，直接回傳 `None`。不用寫 match。

#### and_then —— 鏈式操作（可能失敗）

`map` 的閉包回傳普通值，但如果你的轉換本身也可能回傳 `None` 呢？用 `and_then`：

```rust
let x: Option<i32> = Some(5);
let y = x.and_then(|v| if v > 3 { Some(v * 2) } else { None });
```

`and_then` 的閉包回傳 `Option`，避免了 `Option<Option<T>>` 的巢狀問題。

#### unwrap_or_else —— 給一個計算 default 的閉包

```rust
let x: Option<i32> = None;
let y = x.unwrap_or_else(|| {
    println!("沒有值，計算預設值...");
    42
});
```

跟 `unwrap_or` 不同，`unwrap_or_else` 的預設值是**懶惰計算**的——只有在真的是 None 的時候才會執行閉包。

#### filter —— 條件過濾

```rust
let x: Option<i32> = Some(4);
let y = x.filter(|v| v % 2 == 0);  // Some(4)，因為 4 是偶數
let z = x.filter(|v| v % 2 != 0);  // None，因為 4 不是奇數
```

### Result 的閉包方法

Result 也有類似的一套方法。

#### map —— 轉換 Ok 的值

```rust
let r: Result<i32, String> = Ok(10);
let doubled = r.map(|v| v * 2);  // Ok(20)
```

#### map_err —— 轉換 Err 的值

```rust
let r: Result<i32, String> = Err(String::from("not found"));
let r2 = r.map_err(|e| format!("錯誤：{}", e));
```

#### and_then —— 鏈式操作

```rust
let r: Result<i32, String> = Ok(5);
let r2 = r.and_then(|v| {
    if v > 0 {
        Ok(v * 10)
    } else {
        Err(String::from("必須是正數"))
    }
});
```

#### unwrap_or_else —— 從 Err 計算 default

```rust
let r: Result<i32, String> = Err(String::from("oops"));
let value = r.unwrap_or_else(|e| {
    println!("發生錯誤：{}，使用預設值", e);
    0
});
```

### 跟 match 的比較

用 match：
```rust
let result = match opt {
    Some(v) => Some(v * 2),
    None => None,
};
```

用閉包方法：
```rust
let result = opt.map(|v| v * 2);
```

一行搞定，而且意圖更清晰——「對 Some 裡的值做轉換」。

## 範例程式碼

```rust
fn parse_and_double(input: &str) -> Result<i32, String> {
    input
        .parse::<i32>()
        .map_err(|e| format!("解析失敗：{}", e))
        .and_then(|n| {
            if n >= 0 {
                Ok(n * 2)
            } else {
                Err(String::from("不接受負數"))
            }
        })
}

fn find_even(numbers: &[i32]) -> Option<i32> {
    numbers.iter().find(|&&n| n % 2 == 0).copied()
}

fn main() {
    // Option::map
    let maybe_num: Option<i32> = Some(21);
    let doubled = maybe_num.map(|n| n * 2);
    println!("map: {:?}", doubled);

    // Option::and_then
    let result = maybe_num.and_then(|n| {
        if n > 10 { Some(n - 10) } else { None }
    });
    println!("and_then: {:?}", result);

    // Option::filter
    let even = maybe_num.filter(|n| n % 2 == 0);
    println!("filter(偶數): {:?}", even);

    // Option::unwrap_or_else
    let none_value: Option<i32> = None;
    let default = none_value.unwrap_or_else(|| {
        println!("計算預設值中...");
        99
    });
    println!("unwrap_or_else: {}", default);

    // Result 鏈式操作
    println!("\n--- Result 鏈式操作 ---");
    let good = parse_and_double("21");
    println!("parse_and_double(\"21\") = {:?}", good);

    let bad_parse = parse_and_double("abc");
    println!("parse_and_double(\"abc\") = {:?}", bad_parse);

    let negative = parse_and_double("-5");
    println!("parse_and_double(\"-5\") = {:?}", negative);

    // Result::unwrap_or_else
    let safe_value = parse_and_double("oops").unwrap_or_else(|e| {
        println!("錯誤處理：{}", e);
        0
    });
    println!("安全取值：{}", safe_value);

    // 組合 Option 方法
    println!("\n--- Option 鏈式操作 ---");
    let numbers = vec![1, 3, 5, 8, 11];
    let result = find_even(&numbers)
        .filter(|n| *n > 5)
        .map(|n| n * 10);
    println!("找偶數 > 5 再乘 10：{:?}", result);
}
```

## 重點整理
- `Option::map` / `Result::map` 對內部值做轉換，None / Err 時不執行
- `and_then` 用於閉包本身也回傳 Option / Result 的情況，避免巢狀
- `unwrap_or_else` 懶惰計算預設值，只在 None / Err 時才執行閉包
- `Option::filter` 根據條件決定保留 Some 或轉成 None
- `Result::map_err` 可以轉換錯誤型別，方便錯誤處理鏈
- 這些方法可以鏈式呼叫，比層層 match 更簡潔易讀
