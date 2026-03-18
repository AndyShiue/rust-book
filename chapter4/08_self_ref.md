# 第四章第 8 集：self vs &self vs &mut self

## 本集目標
學會在 method 中選擇 `self`、`&self`、`&mut self`，以及函數參數的 `T` / `&T` / `&mut T` 怎麼選。

## 概念說明

### 回顧：第三章的 self

在第三章，我們學了 `impl` 和 method，當時所有的 method 都用 `self` 傳值：

```rust
impl Cat {
    fn meow(self) {
        println!("喵～");
    }
}
```

但 `self` 傳值會**消耗**這個值——呼叫完之後，原本的變數就不能再用了（因為被 move 了）。

現在我們學了借用，就可以用更聰明的方式了！

### 三種 self

| 寫法 | 意思 | 效果 |
|---|---|---|
| `self` | 取得所有權 | 呼叫後原本的變數不能再用（move） |
| `&self` | 唯讀借用自己 | 呼叫後原本的變數還能用，但不能改 |
| `&mut self` | 可變借用自己 | 呼叫後原本的變數還能用，而且可以改 |

### 怎麼選？

- **只是要讀取資料** → 用 `&self`（最常用！）
- **要修改自己的欄位** → 用 `&mut self`
- **要轉移所有權（呼叫後原本的變數不能再用）** → 用 `self`

大部分的 method 都用 `&self`，因為你通常只是想「看看這個東西的狀態」，不需要消耗它。

### 函數參數也一樣

不只是 method 的 self，一般函數參數也是同樣的邏輯：

| 參數型別 | 意思 |
|---|---|
| `p: Point` | 拿走所有權（move） |
| `p: &Point` | 唯讀借用 |
| `p: &mut Point` | 可變借用 |

選擇的原則一樣：
- 只讀 → `&T`
- 要改 → `&mut T`
- 要消耗 → `T`

## 範例程式碼

```rust
#[derive(Debug)]
struct Counter {
    id: i32,
    count: i32,
}

impl Counter {
    // associated function：建立新的 Counter
    fn new(id: i32) -> Self {
        Counter { id, count: 0 }
    }

    // &self：只讀
    fn get_count(&self) -> i32 {
        self.count
    }

    // &self：只讀，印出資訊
    fn display(&self) {
        println!("計數器 {}：目前計數 = {}", self.id, self.count);
    }

    // &mut self：可變借用，修改 count
    fn increment(&mut self) {
        self.count += 1;
    }

    // self：取得所有權，回傳最終結果
    fn finish(self) -> i32 {
        println!("計數器 {} 結束！最終計數 = {}", self.id, self.count);
        self.count
    }
}

// 一般函數也一樣的邏輯
fn print_counter(c: &Counter) {
    println!("（函數版）計數器 {}：{}", c.id, c.count);
}

fn reset_counter(c: &mut Counter) {
    c.count = 0;
}

fn main() {
    let mut c = Counter::new(1);

    // &self：只讀
    c.display();
    println!("目前：{}", c.get_count());

    // &mut self：修改
    c.increment();
    c.increment();
    c.increment();
    c.display();

    // 一般函數的 &T 和 &mut T
    print_counter(&c);
    reset_counter(&mut c);
    c.display();
    c.increment();
    c.increment();

    // self：取得所有權
    let final_count = c.finish();
    println!("回傳的最終計數：{}", final_count);
    // c 的所有權已經被 finish 拿走了，下面這行會編譯錯誤：
    // c.display();
}
```

## 重點整理
- `&self`：唯讀借用，最常用，呼叫後還能繼續用
- `&mut self`：可變借用，可以修改欄位，呼叫後還能繼續用
- `self`：消耗所有權，呼叫後變數就不能再用了
- 選擇原則：**只讀 → `&self`，要改 → `&mut self`，要消耗 → `self`**
- 一般函數參數也一樣：**只讀 → `&T`，要改 → `&mut T`，要消耗 → `T`**
