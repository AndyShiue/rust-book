# 第七章第 4 集：pub 可見性

## 本集目標

完整理解 Rust 的可見性規則，掌握 `pub` 的各種用法。

## 概念說明

第 2 集提到 mod 裡的東西預設是私有的，這一集我們來把可見性規則講清楚。

順帶一提——你可能注意到 `main.rs` 裡面直接寫的 `fn main()` 和其他函數並沒有被包在任何 `mod` 裡面。那是因為 `main.rs`（或 `lib.rs`）本身就是 crate 的**根 mod**，你寫在裡面的東西自動屬於這個根 mod，不用再額外包一層。

### 預設私有

Rust 的哲學是**預設封閉**——所有東西一開始都是私有的，你必須明確地用 `pub` 開放。這跟有些語言預設 public 的設計完全相反。

```rust
mod secrets {
    fn hidden() {
        // 外面看不到我
    }

    pub fn visible() {
        // 外面可以呼叫我
        hidden(); // 同 mod 內可以互相呼叫
    }
}

fn main() {
    secrets::visible();  // OK
    // secrets::hidden(); // 編譯錯誤！hidden 是私有的
}
```

你可能會好奇：`fn main()` 和 `mod secrets` 都沒加 `pub`，為什麼 `main` 能看到 `secrets`？因為它們都定義在根 mod 裡——同一個 mod 的成員互相看得到，不需要 `pub`。`pub` 是用來讓**其他 mod** 看到你的東西的。

### pub fn

函式加 `pub` 就對外公開，沒什麼好說的。

### pub struct —— 欄位要個別標記

struct 加 `pub` 只是讓這個**型別**公開，欄位還是私有的！每個欄位要**個別**加 `pub`：

```rust
mod user {
    pub struct Profile {
        pub name: String,     // 外部可讀寫
        pub email: String,    // 外部可讀寫
        age: u32,             // 私有！外部看不到
    }

    impl Profile {
        pub fn new(name: String, email: String, age: u32) -> Profile {
            Profile { name, email, age }
        }

        pub fn age(&self) -> u32 {
            self.age  // 透過方法公開唯讀存取
        }
    }
}

fn main() {
    let p = user::Profile::new(
        String::from("Yaju"),
        String::from("yaju@senpai.com"),
        24,
    );
    println!("名字：{}", p.name);      // OK，name 是 pub
    println!("年齡：{}", p.age());      // OK，透過方法存取
    // println!("{}", p.age);           // 編譯錯誤！age 欄位是私有的
}
```

這個設計很重要——它讓你可以控制哪些欄位要暴露、哪些要隱藏。如果 struct 有任何私有欄位，外部就無法直接用 `StructName { ... }` 建構，必須透過你提供的建構函式。

### pub enum —— variants 自動公開

enum 跟 struct 不一樣：只要 enum 本身是 `pub`，所有 variants 都**自動公開**。

```rust
mod status {
    pub enum Color {
        Red,
        Green,
        Blue,
    }
}

fn main() {
    let c = status::Color::Red;  // 所有 variant 都可用
    match c {
        status::Color::Red => println!("紅色"),
        status::Color::Green => println!("綠色"),
        status::Color::Blue => println!("藍色"),
    }
}
```

這很合理——如果你公開了一個 enum 但藏了某些 variant，別人根本沒辦法正確 match，那還不如不公開。

### pub trait 和 impl

trait 加 `pub` 後，它定義的方法都跟著公開（這也合理，trait 就是介面契約）：

```rust
mod animal {
    pub trait Speak {
        fn speak(&self);  // 不用加 pub，跟著 trait 走
    }

    pub struct Dog;

    impl Speak for Dog {
        fn speak(&self) {
            println!("汪！");
        }
    }
}

fn main() {
    let d = animal::Dog;
    d.speak();  // Speak trait 定義在同一個 crate，方法可以直接呼叫
}
```

`impl` 區塊本身**不需要也不能加 `pub`**——方法的可見性由各自的 `pub` 決定：

```rust
mod shapes {
    pub struct Circle {
        pub radius: f64,
    }

    impl Circle {
        pub fn area(&self) -> f64 {
            std::f64::consts::PI * self.radius * self.radius
        }

        // 這是私有方法，只有 mod 內部能用
        fn internal_check(&self) -> bool {
            self.radius > 0.0
        }
    }
}
```

### pub(crate)、pub(super)、pub(in path)

有時候你不想完全公開，但又想讓 crate 內部的其他 mod 使用。Rust 提供了精細的控制：

- `pub(crate)`：整個 crate 內部可見，但外部（別的 crate）看不到
- `pub(super)`：只有父 mod 可見
- `pub(in crate::some::path)`：只對指定的 mod 路徑可見——最精細的控制

```rust
mod database {
    pub(crate) fn connect() -> String {
        // 整個 crate 內部都能呼叫，但如果這是 library，
        // 使用你 library 的人看不到這個函式
        String::from("connected")
    }

    // 注意 queries 本身是 pub——如果這個 mod 不是 pub，
    // 那裡面的東西即使標了 pub(super) 也沒用，
    // 因為外面根本看不到這個 mod，更別說裡面的東西了。
    pub mod queries {
        pub(super) fn raw_query() -> String {
            // 只有 database mod（父 mod）能看到
            String::from("SELECT * FROM users")
        }

        pub fn safe_query() -> String {
            let raw = raw_query();  // 同 mod 內可以呼叫
            format!("SAFE: {}", raw)
        }
    }
}

fn main() {
    let conn = database::connect();          // OK，我們在同一個 crate
    let q = database::queries::safe_query(); // OK，pub
    println!("{}, {}", conn, q);
    // database::queries::raw_query();       // 編譯錯誤！pub(super) 只給父 mod
}
```

## 範例程式碼

```rust
mod game {
    pub struct Player {
        pub name: String,
        hp: i32,              // 私有：不讓外部直接改血量
        pub(crate) score: u32, // crate 內部可見
    }

    impl Player {
        pub fn new(name: &str) -> Player {
            Player {
                name: String::from(name),
                hp: 100,
                score: 0,
            }
        }

        pub fn hp(&self) -> i32 {
            self.hp
        }

        pub fn take_damage(&mut self, damage: i32) {
            self.hp -= damage;
            if self.hp < 0 {
                self.hp = 0;
            }
        }

        pub fn is_alive(&self) -> bool {
            self.hp > 0
        }
    }

    pub enum GameEvent {
        Start,
        Hit(i32),
        GameOver,
    }
}

fn main() {
    let mut player = game::Player::new("Andy");
    println!("{} 的血量：{}", player.name, player.hp());

    player.take_damage(30);
    println!("受到 30 傷害後：{}", player.hp());

    let event = game::GameEvent::Hit(30);
    match event {
        game::GameEvent::Start => println!("遊戲開始！"),
        game::GameEvent::Hit(dmg) => println!("受到 {} 傷害！", dmg),
        game::GameEvent::GameOver => println!("遊戲結束"),
    }
}
```

## 重點整理

- Rust **預設一切私有**，必須明確加 `pub` 才公開
- `pub struct` 只公開型別名稱，每個欄位需要**個別**加 `pub`
- `pub enum` 的所有 variants **自動公開**
- `impl Trait for T` 裡的 fn 可見性跟著 trait 走，不加 `pub`；`impl T` 裡的 fn 各自用 `pub` 控制
- `pub(crate)`：crate 內部可見，外部不可見
- `pub(super)`：只有父 mod 可見
- `pub(in path)`：只對指定的 mod 路徑可見
- 有私有欄位的 struct 無法從外部直接建構，必須提供建構函式
