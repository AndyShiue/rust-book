# 第六章第 4 集：閉包種類的推斷

## 本集目標
理解 Rust 如何根據閉包體的內容，自動推斷一個閉包是 FnOnce、FnMut 還是 Fn。

## 概念說明

上一集我們手動用 struct 模擬了三種閉包，對應 `self`、`&mut self`、`&self`。但你寫閉包的時候從來不需要告訴 Rust「這是 FnOnce」或「這是 FnMut」——Rust 會自動判斷。

### 推斷規則

Rust 看的是**閉包體裡面對捕捉變數做了什麼**：

1. **如果閉包體裡 move 了捕捉的變數**（例如 `let s = captured_string;`）→ 這個閉包是 **FnOnce**，因為 move 走了就沒了，只能呼叫一次
2. **如果閉包體裡修改了捕捉的變數**（例如 `count += 1;`）→ 這個閉包是 **FnMut**，可以多次呼叫但需要 `&mut`
3. **如果閉包體只讀取捕捉的變數**（例如 `println!("{}", name);`）→ 這個閉包是 **Fn**，只需要 `&self`

Rust 會選**最寬鬆但足夠的那個**——如果只讀取，就給 Fn（最寬鬆，因為 Fn 的閉包也能當 FnMut 和 FnOnce 用）。如果有修改，升級到 FnMut。如果有 move，再升級到 FnOnce。

### 範例對照

```rust
let name = String::from("Alice");

// 只讀取 name → Fn
let greet = || println!("Hi, {}!", name);

// 修改 count → FnMut
let mut count = 0;
let mut increment = || { count += 1; };

// move name → FnOnce
let consume = || { let s = name; };
```

你不需要寫任何標記——Rust 看閉包體就知道了。

### 如果沒有捕捉任何變數呢？

沒有捕捉變數的閉包自動是 Fn（最寬鬆的），因為它不需要存取任何外部狀態：

```rust
let add_one = |x: i32| x + 1;  // Fn
```

第 2 集提到的「不捕捉變數的閉包可以轉成函數指標」也是因為這個原因——它連 struct 都不需要。

## 範例程式碼

```rust
fn require_fn(f: impl Fn()) {
    f();
    f();
}

fn require_fn_mut(mut f: impl FnMut()) {
    f();
    f();
}

fn require_fn_once(f: impl FnOnce()) {
    f();
}

fn main() {
    let name = String::from("Rust");

    // 只讀取 → Fn → 可以傳給所有三種
    let read_only = || println!("Hello, {}!", name);
    require_fn(&read_only);
    require_fn_mut(&read_only);
    require_fn_once(&read_only);

    // 修改 → FnMut → 可以傳給 FnMut 和 FnOnce，但不能傳給 Fn
    let mut count = 0;
    let mut mutating = || { count += 1; println!("count = {}", count); };
    // require_fn(&mutating);  // 編譯錯誤！FnMut 不是 Fn
    require_fn_mut(&mut mutating);

    // move → FnOnce → 只能傳給 FnOnce
    let data = String::from("消耗我");
    let consuming = || { let _s = data; };
    // require_fn(&consuming);      // 編譯錯誤！
    // require_fn_mut(&consuming);   // 編譯錯誤！
    require_fn_once(consuming);
}
```

## 重點整理
- Rust 根據閉包體的內容自動推斷閉包的種類：move → FnOnce、修改 → FnMut、只讀 → Fn
- 不需要手動標記，編譯器會選最寬鬆但足夠的 trait
- 沒有捕捉變數的閉包是 Fn，也可以轉成函數指標
- Fn 的閉包可以傳給 FnMut 和 FnOnce；FnMut 可以傳給 FnOnce；反過來不行
