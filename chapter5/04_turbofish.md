# 第五章第 4 集：Turbofish 語法

## 本集目標
學會用 `::<>` turbofish 語法手動指定型別參數，理解它和泛型定義的關係。

## 概念說明

前幾集我們學了泛型——函數、struct、enum 都可以有型別參數 `<T>`。大部分時候 Rust 能自動推斷 `T` 是什麼，但有時候編譯器推不出來，就需要我們手動告訴它。

### Turbofish 是什麼？

還記得第一章學 `parse` 的時候，我們寫過這樣的程式碼嗎？

```rust
let num = input.trim().parse::<i32>().expect("請輸入數字");
```

當時我們把 `::<i32>` 當黑盒子照抄。現在學了泛型，終於可以理解它了！

`.parse()` 是一個泛型方法——它的定義大概長這樣（簡化版）：

它是一個泛型方法，有一個型別參數 `T`，代表「你想把字串轉成什麼型別」。但光看 `input.trim().parse()` 這段程式碼，編譯器不知道你想轉成 `i32` 還是 `f64` 還是其他東西。

所以我們用 `::<i32>` 手動指定 `T = i32`。這個 `::<>` 語法就叫做 **turbofish**（因為 `::<>` 看起來像一條魚 🐟）。

### Turbofish 的本質

Turbofish 就是「手動填入泛型定義裡角括號的型別參數」：

- 泛型定義：`fn parse<T>(...)`——這裡的 `<T>` 是宣告
- Turbofish：`.parse::<i32>()`——這裡的 `::<i32>` 是填入

函數、方法、struct 的 associated function 都可以用 turbofish：

```rust
// 函數的 turbofish
func::<i32>(arg);

// associated function 的 turbofish
Vec::<i32>::new();
```

### .parse() 做了什麼？

順便完整解釋一下 `parse`：它把字串轉換成你指定的型別。轉換可能失敗（比如 `"abc"` 不能轉成數字），所以需要搭配 `.expect()` 處理失敗的情況——這點在第一章就用過了。

## 範例程式碼

```rust
fn first<T>(a: T, _b: T) -> T {
    a
}

fn main() {
    // 通常 Rust 能自動推斷，不需要 turbofish
    let x = first(10, 20);
    println!("{}", x);

    // 手動用 turbofish 指定型別
    let y = first::<f64>(3.14, 2.71);
    println!("{}", y);

    // Vec 的 turbofish
    let v = Vec::<i32>::new();
    println!("{:?}", v);

    // parse 的 turbofish——呼應第一章的黑盒子
    let input = "42";
    let num = input.parse::<i32>().expect("不是數字");
    println!("{}", num);

    let pi = "3.14".parse::<f64>().expect("不是數字");
    println!("{}", pi);
}
```

## 重點整理
- **Turbofish** `::<>` 是手動指定泛型型別參數的語法
- 大部分時候 Rust 能自動推斷，不需要 turbofish
- 當編譯器推不出型別時（例如 `.parse()`），就需要用 turbofish 手動指定
- 第一章寫的 `.parse::<i32>()` 其實就是 turbofish——現在我們理解它為什麼這樣寫了
- `.parse()` 把字串轉成指定型別，轉換可能失敗所以搭配 `.expect()` 使用
