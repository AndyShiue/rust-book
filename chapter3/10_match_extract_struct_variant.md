# 第三章第 10 集：match 取出 struct variant 資料

## 本集目標
學會用 match 取出 enum struct variant 裡面攜帶的有名字欄位。

## 概念說明

第 9 集學了怎麼取出 tuple variant 的資料（用位置），現在來學取出 **struct variant** 的資料（用欄位名）。

語法是在模式裡用 `欄位名: 變數名` 的寫法：

```rust
match s {
    Shape::Circle { radius: r } => println!("半徑 {}", r),
    Shape::Rectangle { width: w, height: h } => println!("{}x{}", w, h),
}
```

`radius: r` 的意思是「把 radius 這個欄位的值取出來，叫做 r」。冒號左邊是欄位名，右邊是你自己取的變數名。

這和建立 struct variant 的語法很像，只是方向相反：建立是「把值放進去」，match 是「把值拿出來」。

## 範例程式碼

```rust
enum Shape {
    Circle { radius: f64 },
    Rectangle { width: i32, height: i32 },
}

fn main() {
    let s = Shape::Rectangle { width: 10, height: 5 };

    match s {
        Shape::Circle { radius: r } => {
            println!("這是圓形，半徑 = {}", r);
            let area = r * r * 3.14159;
            println!("面積大約 {}", area);
        }
        Shape::Rectangle { width: w, height: h } => {
            println!("這是長方形");
            println!("寬 = {}，高 = {}", w, h);
            let area = w * h;
            println!("面積 = {}", area);
            let perimeter = 2 * (w + h);
            println!("周長 = {}", perimeter);
        }
    }
}
```

## 一般的 struct 也能用同樣的方式

不只 enum 的 struct variant，一般的 named field struct 也可以在 match 裡解構：

```rust
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let p = Point { x: 3, y: 0 };

    match p {
        Point { x: 0, y: 0 } => println!("原點"),
        Point { x: a, y: 0 } => println!("在 x 軸上，x = {}", a),
        Point { x: 0, y: b } => println!("在 y 軸上，y = {}", b),
        Point { x: a, y: b } => println!("在 ({}, {})", a, b),
    }
}
```

語法完全一樣——`型別名 { 欄位名: 變數名 }`。

## 重點整理
- struct variant 在 match 裡用 `欄位名: 變數名` 來取出資料
- `Shape::Circle { radius: r }` → 把 radius 欄位取出來叫做 `r`
- 冒號左邊是欄位名（必須和定義一樣），右邊是你自己取的變數名
- 所有欄位都要寫出來（目前是這樣，之後會學怎麼忽略）
- 一般的 named field struct 也能用同樣的方式在 match 裡解構
