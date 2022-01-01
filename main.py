
import PySimpleGUI as sg
import pandas as pd

ELEMENT_HEIGHT = 1
ELEMENT_OFFSET = 3

sg.theme('dark grey 8')

COINS_FOUND = [
    [sg.Text("Coinbase Statement (csv)"),sg.In(size=(10,1), enable_events=True, key="-CSV FILE-"),sg.FileBrowse(size=(6,1)),],
    [sg.Text(size=(20, ELEMENT_HEIGHT), text="Coins found in statement")],
    [sg.Listbox(values=[], enable_events=True, size=(44,20),key="-FILE LIST-",no_scrollbar = True,)],
]

COLUMN_1 = [
    [sg.Text(size=(20, ELEMENT_HEIGHT), text="Selected Coin:"), sg.Text(size=(20, ELEMENT_HEIGHT), enable_events=True, key="-SELECTED COIN-")],
    #Buys
    [sg.Text(size=(20, ELEMENT_HEIGHT), text="Buys")],
    [sg.Text(size=(ELEMENT_OFFSET, ELEMENT_HEIGHT), text=""), sg.Text(size=(20, ELEMENT_HEIGHT), text="Current Coin Value:"), sg.Input(size=(20, ELEMENT_HEIGHT), enable_events=True, key="-PRICE INPUT-")],
    [sg.Text(size=(ELEMENT_OFFSET, ELEMENT_HEIGHT), text=""), sg.Text(size=(20, ELEMENT_HEIGHT), text="Total Bought w/o Fees:"), sg.Text(size=(20, ELEMENT_HEIGHT), key="-BUY WITHOUT FEES-")],
    [sg.Text(size=(ELEMENT_OFFSET, ELEMENT_HEIGHT), text=""), sg.Text(size=(20, ELEMENT_HEIGHT), text="Total Buy Fees:"), sg.Text(size=(20, ELEMENT_HEIGHT), key="-BUY FEES-")],
    [sg.Text(size=(ELEMENT_OFFSET, ELEMENT_HEIGHT), text=""), sg.Text(size=(20, ELEMENT_HEIGHT), text="Total Bought With Fees:"), sg.Text(size=(20, ELEMENT_HEIGHT), key="-BUY WITH FEES-")],
    [sg.Text(size=(ELEMENT_OFFSET, ELEMENT_HEIGHT), text=""), sg.Text(size=(20, ELEMENT_HEIGHT), text="Total Coins Bought:"), sg.Text(size=(20, ELEMENT_HEIGHT), key="-BUY AMOUNT-")],
    [sg.Text(size=(ELEMENT_OFFSET, ELEMENT_HEIGHT), text=""), sg.Text(size=(20, ELEMENT_HEIGHT), text="Buy Cost Basis:"), sg.Text(size=(20, ELEMENT_HEIGHT), key="-BUY COST BASIS-")],
    [sg.Text(size=(ELEMENT_OFFSET, ELEMENT_HEIGHT), text=""), sg.Text(size=(20, ELEMENT_HEIGHT), text="Total Up or Down:"), sg.Text(size=(20, ELEMENT_HEIGHT), key="-UP OR DOWN-")],

    #Sells
    [sg.Text(size=(20, ELEMENT_HEIGHT), text="Sells")],
    [sg.Text(size=(ELEMENT_OFFSET, ELEMENT_HEIGHT), text=""), sg.Text(size=(20, ELEMENT_HEIGHT), text="Total Sold w/o Fees:"), sg.Text(size=(20, ELEMENT_HEIGHT), key="-SELL WITHOUT FEES-")],
    [sg.Text(size=(ELEMENT_OFFSET, ELEMENT_HEIGHT), text=""), sg.Text(size=(20, ELEMENT_HEIGHT), text="Total Sell Fees:"), sg.Text(size=(20, ELEMENT_HEIGHT), key="-SELL FEES-")],
    [sg.Text(size=(ELEMENT_OFFSET, ELEMENT_HEIGHT), text=""), sg.Text(size=(20, ELEMENT_HEIGHT), text="Total Sold With Fees:"), sg.Text(size=(20, ELEMENT_HEIGHT), key="-SELL WITH FEES-")],
    [sg.Text(size=(ELEMENT_OFFSET, ELEMENT_HEIGHT), text=""), sg.Text(size=(20, ELEMENT_HEIGHT), text="Total Coins Sold:"), sg.Text(size=(20, ELEMENT_HEIGHT), key="-SELL AMOUNT-")],
    [sg.Text(size=(ELEMENT_OFFSET, ELEMENT_HEIGHT), text=""), sg.Text(size=(20, ELEMENT_HEIGHT), text="Sell Cost Basis:"), sg.Text(size=(20, ELEMENT_HEIGHT), key="-SELL COST BASIS-")],
]

layout =  [
    [
        sg.Column(COINS_FOUND, key='-COINS FOUND-'),
        sg.VSeparator(),
        sg.Column(COLUMN_1),
    ]
]

window = sg.Window("Coinbase Statement Analyzer", layout, text_justification='left', element_padding=(2, 2), keep_on_top=True)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == "-CSV FILE-":
        filename = open(values["-CSV FILE-"])
        data = pd.read_csv(filename)
        coins = data['size unit']
        unique_coins = coins.unique()
        window["-FILE LIST-"].update(unique_coins)

    elif event == "-FILE LIST-":
        try:
            buy_without_fees = []
            buy_fees = []
            buy_with_fees = []
            buy_amount = []
            buy_coin_price = []
            buy_amount_price = []

            selected = values["-FILE LIST-"]
            window["-SELECTED COIN-"].update(selected)

            #Buys
            sum_without_fees = 0
            sum_fees = 0
            sum_with_fees = 0
            sum_amount = 0
            sum_amount_price = 0
            weighted_average = 0
            for idx, row in enumerate(data.iloc):
                str_selected = str(selected)
                if row['size unit'] in str_selected:
                   if row['side'] == "BUY":
                       buy_without_fees.append(abs(row['total']) - abs(row['fee']))
                       buy_fees.append(abs(row['fee']))
                       buy_with_fees.append(abs(row['total']))
                       buy_amount.append(abs(row['size']))
                       buy_amount_price.append(abs(row['size'])*abs(row['price']))

            if len(buy_amount) == 0:
                window["-BUY WITHOUT FEES-"].update("No buys found")
                window["-BUY FEES-"].update("No buys found")
                window["-BUY WITH FEES-"].update("No buys found")
                window["-BUY AMOUNT-"].update("No buys found")
                window["-BUY COST BASIS-"].update("No buys found")
            else:
                sum_without_fees = sum(buy_without_fees)
                sum_fees = sum(buy_fees)
                sum_with_fees = sum(buy_with_fees)
                sum_amount = sum(buy_amount)
                sum_amount_price = sum(buy_amount_price)

                window["-BUY WITHOUT FEES-"].update(round(sum_without_fees, 3))
                window["-BUY FEES-"].update(round(sum_fees, 3))
                window["-BUY WITH FEES-"].update(round(sum_with_fees, 3))
                window["-BUY AMOUNT-"].update(round(sum_amount, 3))
                window["-BUY COST BASIS-"].update(round((sum_amount_price/sum_amount), 3))


            #Sells
            sell_without_fees = []
            sell_fees = []
            sell_with_fees = []
            sell_amount = []
            sell_coin_price = []
            sell_amount_price = []
            for idx, row in enumerate(data.iloc):
                str_selected = str(selected)
                if row['size unit'] in str_selected:
                    if row['side'] == "SELL":
                        sell_without_fees.append(abs(row['total']) + abs(row['fee']))
                        sell_fees.append(abs(row['fee']))
                        sell_with_fees.append(abs(row['total']))
                        sell_amount.append(abs(row['size']))
                        sell_amount_price.append(abs(row['size']) * abs(row['price']))

            if len(sell_amount) == 0:
                window["-SELL WITHOUT FEES-"].update("No sells found")
                window["-SELL FEES-"].update("No sells found")
                window["-SELL WITH FEES-"].update("No sells found")
                window["-SELL AMOUNT-"].update("No sells found")
                window["-SELL COST BASIS-"].update("No sells found")
            else:
                sum_without_fees = sum(sell_without_fees)
                sum_fees = sum(sell_fees)
                sum_with_fees = sum(sell_with_fees)
                sum_amount = sum(sell_amount)
                sum_amount_price = sum(sell_amount_price)

                window["-SELL WITHOUT FEES-"].update(round(sum_without_fees, 3))
                window["-SELL FEES-"].update(round(sum_fees, 3))
                window["-SELL WITH FEES-"].update(round(sum_with_fees, 3))
                window["-SELL AMOUNT-"].update(round(sum_amount, 3))
                window["-SELL COST BASIS-"].update(round((sum_amount_price / sum_amount), 3))

        except ValueError:
            print(ValueError)


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

        window["-UP OR DOWN-"].update(round(amount_up_or_down))

window.close()



