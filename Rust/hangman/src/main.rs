use std::io::{self, Write};

fn main() {
    render_game();
}


fn render_game() {
    loop {
        print_main_manu();
        let user_option = get_user_option(0, 3);
        match user_option {
            0 => {
                println!("| Exiting...");
                std::thread::sleep(std::time::Duration::from_secs(2));
                break;
            },
            1 => {
                println!("| Starting new game...");
                std::thread::sleep(std::time::Duration::from_secs(2));
            },
            2 => {
                println!("| Loading game...");
                std::thread::sleep(std::time::Duration::from_secs(2));
            },
            3 => {
                println!("| Showing ranking...");
                std::thread::sleep(std::time::Duration::from_secs(2));
            },
            _ => {
                println!("| Invalid option!");
                std::thread::sleep(std::time::Duration::from_secs(2));
            },
        }
    }
}

fn print_main_manu() {
    // clear screen
    print!("{}[2J", 27 as char);
    println!("
|---------------------------------------------------|
|                       Hangman                     |
|---------------------------------------------------|
| 1 - New Game                                      |
| 2 - Load Game                                     |
| 3 - Ranking                                       |
| 0 - Exit                                          | 
|---------------------------------------------------|");
}


fn get_user_option(min: u8, max: u8) -> u8 {
    loop {
        print!("| Please select an option: ");
        io::stdout().flush().unwrap();
        let mut user_input = String::new();
        io::stdin().read_line(&mut user_input).expect("Failed to read line");
        let user_input: u8 = match user_input.trim().parse() {
            Ok(num) => num,
            Err(_) => {
                println!("Please type a number!");
                std::thread::sleep(std::time::Duration::from_secs(2));
                continue;
            },
        };
        if user_input < min || user_input > max {
            println!("Please type a number between {} and {}!", min, max);
            std::thread::sleep(std::time::Duration::from_secs(2));
            continue;
        }
        return user_input;
    }
}