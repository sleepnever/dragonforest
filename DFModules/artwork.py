#
# Game ASCII Art
#

def show_title() -> None:
    print('''
╔════════════════════╤═════════╗
║                              ╟
║     -= ǷɌAGON FOREŞƮ =-     ┴╣
╠┴                             ╜
╚═════════════╧══════════════╝─╜
    ''')

def show_dead() -> None:
    print('''

    -= YOU ARE DEAD =-

    ''')

def show_inn() -> None:
    print('''
          _________||__
        /             \\
       /______INN______\\
        | [] [] [] [] |
        | [] [] [] [] |
        |________[ ]__|
    ''')

def show_blacksmith() -> None:
        print('''
          ____________
        /             \\
       /___BLACKSMITH__\\
        |              |
        |________[ ]___|
    ''')

def show_town() -> None:
    print('''
               _________      {**}
              /         \\   {****}
             /___________\\ {******}
     ______  |  ______   |  {******}
    /     \\ | /     \\  |    | |    
    |__[]__| |_|__[]__| _|    / \\ _________  
                                   |welcome|   
                                       ||
    ''')


def show_forest() -> None:
    print('''
   {**} {**}    {**}
  {****}****}  {****}
 {******}*****}******}
 {******}*****}******}
   | |   | |    | |
   / \\ /  \\  /  \\    

    ''')

def show_camp() -> None:
    print('''
        ______         
       /     /\\        `
      /     /  \\      ."".
     /_____/----\\_  xxXXXxx   
    "     "
    ''')

def show_dragon_cave() -> None:
    print('''
         ###
       #######
      ##########
     ###      ###
     ###       ####
    -------------------
    ''')

def show_dragon_amazement() -> None:
    print('''
       
       ^^^^^    ^^^^^
        ____    ____
       /    \\ /    \\
       |(O )|  |( O)|
       |    |  |    |
       \\___/  \\___/
           (    )
        _____________
       /            \\
       \\___________/
    ''')

def inn_gamble_pinfinger() -> None:
    print('''
        [ ]
       _[_]_
        | |
        | |
        \\/
     (_)(_)(_)O   
    ''')

def inn_gamble_number_guess() -> None:
    print('''
    
    ## Guess the Number ##
    
    ''')

def inn_gamble_high_points() -> None:
    print('''
      ________     _______
     /_______/|   /______/|
     | X  X | |  | X    | |
     |      | |  |   X  | |
     |_X__X_|/   |_____X|/

    ''')


def inn_gamble_thimblerig_a() -> None:
    print('''
     ____     ____     ____
    /    \\  /    \\  /    \\
    |____|   |____|   |____|
    
      ( )
    ''')

def inn_gamble_thimblerig_b() -> None:
    print('''
     ____     ____     ____
    /    \\  /    \\  /    \\
    |____|   |____|   |____|
    
              ( )
    ''')

def inn_gamble_thimblerig_c() -> None:
    print('''
     ____     ____     ____
    /    \\  /    \\  /    \\
    |____|   |____|   |____|
    
                        ( )
    ''')

def inn_gamble_thimblerig_end() -> None:
    print('''
     ____     ____     ____
    /    \\  /    \\  /    \\
    |____|   |____|   |____|
    ''')