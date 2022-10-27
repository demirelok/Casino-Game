import uuid, random, datetime, sqlite3

def generate_uuid():
    return str(uuid.uuid4()).split("-")[1]

def login(user_name, password, captchaa, captcha):
    calc = {}
    if captchaa == captcha:
        with sqlite3.connect("users.db") as file:
            cursor = file.cursor()
            cursor.execute("SELECT * from users WHERE kullaniciadi == '{}'".format(user_name))
            for data in cursor.fetchall():
                user = data[0]
                passsword = str(data[3])
                name = data[1]
                surname = data[2]
                if user_name == user and password == passsword:
                    calc = user_name
                    print(f"\nWelcome to our game {name} {surname}..!")
                else:
                    break
    return calc

def conditions(username, cash, name, surname):
    with sqlite3.connect("users.db") as file:
        cursor = file.cursor()
        actual = str(datetime.datetime.now()).split(" ")[0]
        cursor.execute("SELECT * from users WHERE gun == '{}' AND kullaniciadi == '{}'".format(actual, username))
        if not cursor.fetchall():
            cash_update(username, cash, name, surname)
        else:
            print(f"\nDear {name} {surname}, you already won your daily reward or signed up today..!")

def cash_update(user_name, cash, name, surname):
    with sqlite3.connect("users.db") as file:
        cursor = file.cursor()
        actual = str(datetime.datetime.now()).split(" ")[0]
        cursor.execute("UPDATE users SET gun == '{}' WHERE kullaniciadi == '{}'".format(actual, user_name))
        cursor.execute("UPDATE users SET cash == {} + 1000 WHERE kullaniciadi == '{}'".format(cash, user_name))
        print(f"Dear {name} {surname}, 1000 $ was added to your account")

def daily(user_name):
    try:
        with sqlite3.connect("users.db") as file:
            cursor = file.cursor()
            cursor.execute("SELECT * from users WHERE kullaniciadi == '{}'".format(user_name))
            data = cursor.fetchall()
            money = data[0][4]
            name = data[0][1]
            surname = data[0][2]
            conditions(user_name, money, name, surname)

    except IndexError:
        print("There is no any user like this name. Please sign up..!")

def sign_up():
    with sqlite3.connect("users.db") as connection:
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS users(kullaniciadi TEXT, ad TEXT, soyadi TEXT, sifre INT, cash INT, gun TEXT)")

        user = input("Enter your username: ")
        name = input("Enter your first name: ")
        surname = input("Enter your surname: ")
        passss = input("Enter your password: ")
        cash = random.randint(1000, 2000)
        day = str(datetime.datetime.now()).split(" ")[0]

        cursor.execute("INSERT INTO users VALUES('{}', '{}', '{}', '{}', '{}', '{}')".format(user, name, surname, passss, cash, day))

        connection.commit()
        print(f"You successfully signed up..!")

def bet(cash, opponent, opponentCash, name, surname):
    print(f"\nYour oppenent will be {opponent}..!")

    while cash > 0 and opponentCash > 0:
        print(f"{opponent} has {opponentCash} $ in his account")
        bett = int(input(f"\nDear {name} {surname} you have : {cash} $ in your account\nPlease type into how much money to risk: "))
        print("--------------------------------------")
        if 0 < bett <= cash and 0 < bett <= opponentCash:
            roll1 = random.randint(1,6) + random.randint(1,6)
            roll2 = random.randint(1,6) + random.randint(1,6)
            print("\n{} {} rolled ==> {}".format(name, surname, roll1))
            print("{} rolled ==> {}".format(opponent, roll2))
            if roll1 > roll2:
                cash += bett
                opponentCash -= bett
            elif roll1 < roll2:
                cash -= bett
                opponentCash += bett
            else:
                continue
        else:
            print(f"\nWRONG BET..! Please type again..!")
    else:
        print("\nGAME OVER\nGAME OVER\nGAME OVER\nGAME OVER\nGAME OVER..!")

def randomBot():
    pick = random.choice(bots)
    return pick

def botNameSurname(pick):
    return pick['adSoyad']

def botCash(pick):
    return pick['cash_bot']

def main():
    while True:
        process = input("\nSign up ==> 1\nLogin ==> 2\nQuit ==> e\n\nPlease choose what you want: ")
        if process == "e":
            print("You successfully exited. We hope you come again..!")
            break
        if process == "1":
            sign_up()
        elif process == "2":
            captcha = generate_uuid()
            print(captcha)

            captchaa = input("Please type into this captcha: ")
            userr = input("Please type into your username: ")
            passw = input("Please type into your password: ")

            botPick = randomBot()
            opponentBotNameSurname = botNameSurname(botPick)
            opponenBotCash = int(botCash(botPick))
            me = login(userr, passw, captchaa, captcha)

            if me == {}:
                print("Login failed..!")
            else:
                daily(userr)
                with sqlite3.connect("users.db") as file:
                    cursor = file.cursor()
                    cursor.execute("SELECT * from users WHERE kullaniciadi == '{}'".format(me))
                    data = cursor.fetchall()
                    cash = data[0][4]
                    name = data[0][1]
                    surname = data[0][2]
                    bet(cash, opponentBotNameSurname, opponenBotCash, name, surname)
        else:
            print("\nPlease choose a correct selection..!")

bot1 = {
    "adSoyad": "Bot Alex",
    "cash_bot": 2000
}
bot2 = {
    "adSoyad": "Bot Bruce",
    "cash_bot": 3000
}
bot3 = {
    "adSoyad": "Bot Okan",
    "cash_bot": 5000
}
bots = [bot1, bot2, bot3]

main()
