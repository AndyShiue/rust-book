# 第三章第 28 集：method

## 本集目標
學會用 `self` 定義 method（方法），讓函數可以用 `.` 在值上面呼叫。

## 概念說明

上一集學了 associated function，它是用 `::` 呼叫的，和「型別」相關。但有時候我們想對一個**已經存在的值**做操作，比如「算出這個 Point 的 x + y」。

這就是 **method**（方法）——參數列表的第一個位置放 `self`，代表「呼叫這個方法的那個值本身」：

```rust
impl Point {
    fn sum(self) -> i32 {
        self.x + self.y
    }
}
```

呼叫的時候用 `.`（點）而不是 `::`：

```rust
let p = Point::new(3, 7);
let s = p.sum();  // 用 . 呼叫 method
```

注意：呼叫 `p.sum()` 的時候，**不需要再手動傳入 `self`**。`.` 前面的 `p` 會自動變成方法裡的 `self`。所以雖然定義時寫了 `fn sum(self)`，呼叫時只要寫 `p.sum()` 而不是 `p.sum(p)`。

### associated function vs method 的差別：
- associated function：沒有 `self`，用 `::` 呼叫 → `Point::new(3, 7)`
- method：第一個參數是 `self`，用 `.` 呼叫 → `p.sum()`

## 範例程式碼

```rust
struct Point {
    x: i32,
    y: i32,
}

impl Point {
    // associated function（沒有 self）
    fn new(x: i32, y: i32) -> Point {
        Point { x, y }
    }

    // method（第一個參數是 self）
    fn sum(self) -> i32 {
        self.x + self.y
    }

    // 另一個 method
    fn is_origin(self) -> bool {
        self.x == 0 && self.y == 0
    }
}

enum Direction {
    Up,
    Down,
    Left,
    Right,
}

impl Direction {
    // enum 也可以有 method
    fn is_horizontal(self) -> bool {
        match self {
            Direction::Left => true,
            Direction::Right => true,
            Direction::Up => false,
            Direction::Down => false,
        }
    }
}

fn main() {
    let p = Point::new(3, 7);       // :: 呼叫 associated function
    let s = p.sum();                 // . 呼叫 method
    println!("3 + 7 = {}", s);

    let p2 = Point::new(0, 0);
    let is_origin = p2.is_origin();
    println!("是原點嗎？{}", is_origin);

    // enum 的 method
    let dir = Direction::Left;
    let horizontal = dir.is_horizontal();
    println!("是水平方向嗎？{}", horizontal);
}
```

## 重點整理
- method 的第一個參數是 `self`，代表值本身
- method 用 `.` 呼叫：`p.sum()`，`.` 前面的值自動成為 `self`，不需要手動傳入
- struct 和 enum 都可以有 method
