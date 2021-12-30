
import PySimpleGUI as sg
import pandas as pd

element_height = 1

coins_found = [
    [
        sg.Text("Coinbase Statement (csv)"),
        sg.In(size=(10,1), enable_events=True, key="-CSV FILE-"),
        sg.FileBrowse(size=(6,1)),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40,15),
            key="-FILE LIST-",
            no_scrollbar = True,
        )
    ],
]

column1 = [
    [sg.Text(size=(20, element_height), text="Selected Coin:")],
    [sg.Text(size=(20, element_height), text="Current Coin Value:")],
    [sg.Text(size=(20, element_height), text="Total Without Fees:")],
    [sg.Text(size=(20, element_height), text="Total Fees:")],
    [sg.Text(size=(20, element_height), text="Total With Fees:")],
    [sg.Text(size=(20, element_height), text="Total Coins Bought:")],
    [sg.Text(size=(20, element_height), text="Cost Basis:")],
    [sg.Text(size=(20, element_height), text="Total Up or Down:")],

    [sg.Text(size=(20, element_height), text="")],
    # [sg.HSeparator],

    [sg.Text(size=(20, element_height), text="Portfolio:")],
    [sg.Text(size=(20, element_height), text="Total Bought Without Fees:")],
    [sg.Text(size=(20, element_height), text="Total Fees:")],
    [sg.Text(size=(20, element_height), text="Total Sold:")],
    [sg.Text(size=(20, element_height), text="Total Value:")],

]

column2 = [
    [sg.Text(size=(20, element_height), enable_events=True, key="-SELECTED COIN-")],
    [sg.Input(size=(20, element_height), enable_events=True, key="-PRICE INPUT-")],
    [sg.Text(size=(20, element_height), key="-WITHOUT FEES-")],
    [sg.Text(size=(20, element_height), key="-FEES-")],
    [sg.Text(size=(20, element_height), key="-WITH FEES-")],
    [sg.Text(size=(20, element_height), key="-AMOUNT-")],
    [sg.Text(size=(20, element_height), key="-WEIGHTED AVERAGE-")],
    [sg.Text(size=(20, element_height), key="-UP OR DOWN")],

    [sg.Text(size=(20, element_height), text="")],
    # [sg.HSeparator()],
    [sg.Text(size=(20, element_height), text="")],
    [sg.Text(size=(20, element_height), key="-TOTAL WITHOUT FEES-")],
    [sg.Text(size=(20, element_height), key="-TOTAL FEES-")],
    [sg.Text(size=(20, element_height), key="-TOTAL SOLD-")],
    [sg.Text(size=(20, element_height), key="-TOTAL VALUE-")],
]

layout =  [
    [
        sg.Column(coins_found),
        sg.VSeparator(),
        sg.Column(column1),
        sg.Column(column2),
    ]
]

window = sg.Window("Coinbase Statement Analyzer", layout, text_justification='left', resizable=True, keep_on_top=True)

sum_without_fees = 0
sum_fees = 0
sum_with_fees = 0
sum_amount = 0
sum_amount_price = 0
weighted_average = 0

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == "-CSV FILE-":
        filename = open(values["-CSV FILE-"])
        data = pd.read_csv(filename)
        coins = data['size unit']
        unique = coins.unique()
        window["-FILE LIST-"].update(unique)

        total_bought_without_fees = []
        fees = []
        total_bought_with_fees = []
        total_sold = []
        total_up_or_down = []

        #Get all the fees for buying and selling
        for idx, row in enumerate(data.iloc):
            fees.append(abs(row['fee']))

        sum_fees = sum(fees)

        # Get all the fees for buying and selling
        for idx, row in enumerate(data.iloc):
            if row['side'] == "BUY":
                total_bought_without_fees.append(abs(row['total']))

        sum_total_without_fees = sum(total_bought_without_fees)

        # Get all the fees for buying and selling
        for idx, row in enumerate(data.iloc):
            if row['side'] == "SELL":
                total_sold.append(abs(row['total']))

        sum_total_sold = sum(total_sold)

        window["-TOTAL WITHOUT FEES-"].update(sum_total_without_fees)
        window["-TOTAL FEES-"].update(sum_fees)
        window["-TOTAL SOLD-"].update(sum_total_sold)
        window["-TOTAL VALUE-"].update(sum_total_without_fees - sum_total_sold)

    elif event == "-FILE LIST-":
        try:

            without_fees = []
            fees = []
            with_fees = []
            amount = []
            coin_price = []
            amount_price = []

            selected = values["-FILE LIST-"]
            window["-SELECTED COIN-"].update(selected)

            # Basically none of this is working
            # coin = data[data['product'] == selected]
            # print(selected)
            # print(data)
            # coin_buy = coin[data['side'] == 'BUY']
            # coin_df = pd.DataFrame({'size': coin['size'], 'price': coin['price']})
            # coin_df["size*price"] = coin_df["size"] * coin_df["price"]
            # print(coin_df)
            # total_coin_cost = coin_df["price"].sum()
            # total_coin_owned = coin_df["amount"].sum()
            # total_coin_amount_price = coin_df["amount*price"].sum()
            # average_coin_cost_bought_at = total_coin_amount_price / total_coin_owned

            # Everything below works....
            for idx, row in enumerate(data.iloc):
                str_selected = str(selected)
                if row['size unit'] in str_selected:
                   if row['side'] == "BUY":
                       without_fees.append(abs(row['total']))
                       fees.append(abs(row['fee']))
                       with_fees.append(abs(row['total']) + abs(row['fee']))
                       amount.append(abs(row['size']))
                       amount_price.append(abs(row['size'])*abs(row['price']))


            sum_without_fees = sum(without_fees)
            sum_fees = sum(fees)
            sum_with_fees = sum(with_fees)
            sum_amount = sum(amount)
            sum_amount_price = sum(amount_price)
            weighted_average = sum_amount_price/sum_amount

            print(sum_without_fees)
            print(sum_fees)
            print(sum_with_fees)
            print(sum_amount)
            print(sum_amount_price)
            print(weighted_average)

            window["-WITHOUT FEES-"].update(sum_without_fees)
            window["-FEES-"].update(sum_fees)
            window["-WITH FEES-"].update(sum_with_fees)
            window["-AMOUNT-"].update(sum_amount)
            window["-WEIGHTED AVERAGE-"].update(weighted_average)

        except:
            pass


    elif event == "-PRICE INPUT-":
        price = values["-PRICE INPUT-"]
        number_price = 0;
        try:
            number_price = int(price)
        except ValueError:
            try:
                number_price = float(price)
            except ValueError:
                print("This is not a number")


        amount_up_or_down = (float(number_price) * sum_amount) - sum_with_fees
        print(amount_up_or_down)

        window["-UP OR DOWN-"].update(amount_up_or_down)

window.close()



