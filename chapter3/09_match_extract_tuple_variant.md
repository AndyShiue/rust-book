# 第三章第 9 集：match 取出 tuple variant 資料

## 本集目標
學會用 match 取出 enum tuple variant 裡面攜帶的資料。

## 概念說明

第 7 集我們學了怎麼建立帶資料的 enum variant，但一直沒辦法取出裡面的資料。現在終於可以了！

在 match 的模式裡，你可以用變數名來「接住」variant 裡的資料：

```rust
match s {
    Shape::Circle(r) => println!("半徑是 {}", r),
    Shape::Rectangle(w, h) => println!("寬 {}，高 {}", w, h),
}
```

`Shape::Circle(r)` 裡的 `r` 不是固定的名字——你可以取任何名字。它的意思是「如果 s 是 Circle，就把裡面的那個 f64 值取出來，叫做 r」。

這就是所謂的**模式比對**（pattern matching）：match 不只是比對「是哪個 variant」，還能同時把裡面的資料取出來給你用。

## 範例程式碼

```rust
enum Shape {
    Circle(f64),
    Rectangle(i32, i32),
}

fn main() {
    let s = Shape::Circle(5.0);

    match s {
        Shape::Circle(r) => {
            println!("這是一個圓形");
            println!("半徑是 {}", r);
            let area = r * r * 3.14159;
            println!("面積大約是 {}", area);
        }
        Shape::Rectangle(w, h) => {
            println!("這是一個長方形");
            println!("寬 {}，高 {}", w, h);
            let area = w * h;
            println!("面積是 {}", area);
        }
    }

    // 再一個例子
    let action = Action::Move(3, -2);

    match action {
        Action::Stop => println!("停止不動"),
        Action::Move(dx, dy) => {
            println!("往 x 方向移動 {}，往 y 方向移動 {}", dx, dy);
        }
    }
}

enum Action {
    Stop,
    Move(i32, i32),
}
```

## 重點整理
- 在 match 模式裡，可以用變數名接住 tuple variant 的資料
- `Shape::Circle(r)` → 把 Circle 裡的值取出來叫做 `r`
- `Shape::Rectangle(w, h)` → 把 Rectangle 裡的兩個值分別叫做 `w` 和 `h`
- 變數名可以自己取，不需要和定義時一樣
- match 依然要窮舉所有 variant
