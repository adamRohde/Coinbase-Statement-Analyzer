
import PySimpleGUI as sg
import csv
import pandas as pd
import os.path

coins_found = [
    [
        sg.Text("Coinbase Statement (csv)"),
        sg.In(size=(15,1), enable_events=True, key="-CSV FILE-"),
        sg.FileBrowse(size=(6,1)),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(45,18),
            key="-FILE LIST-"
        )
    ],
]

column1 = [
    [sg.Text("Input Coin Value:")],
    [sg.Text(" ")],
    [sg.Text("Total Without Fees:")],
    [sg.Text(" ")],
    [sg.Text("Total Fees:")],
    [sg.Text(" ")],
    [sg.Text("Total With Fees:")],
    [sg.Text(" ")],
    [sg.Text("Total Coins Bought")],
    [sg.Text(" ")],
    [sg.Text("Weighted Average Price")],
    [sg.Text(" ")],
    [sg.Text("Total Up or Down")],
]

column2 = [
    [sg.Input(size=(20, 1), enable_events=True, key="-PRICE INPUT-")],
    [sg.Text(" ")],
    [sg.Text(size=(20, 1), key="-WITHOUT FEES-")],
    [sg.Text(" ")],
    [sg.Text(size=(20, 1), key="-FEES-")],
    [sg.Text(" ")],
    [sg.Text(size=(20, 1), key="-WITH FEES-")],
    [sg.Text(" ")],
    [sg.Text(size=(20, 1), key="-AMOUNT-")],
    [sg.Text(" ")],
    [sg.Text(size=(20, 1), key="-WEIGHTED AVERAGE-")],
    [sg.Text(" ")],
    [sg.Text(size=(20, 1), key="-UP OR DOWN-")],
]

layout =  [
    [
        sg.Column(coins_found),
        sg.VSeparator(),
        sg.Column(column1),
        sg.Column(column2),
    ]
]

window = sg.Window("Coinbase Statement Analyzer", layout)

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
        data= pd.read_csv(filename)
        coins = data['size unit']
        unique = coins.unique()
        window["-FILE LIST-"].update(unique)

    elif event == "-FILE LIST-":
        try:

            without_fees = []
            fees = []
            with_fees = []
            amount = []
            coin_price = []
            amount_price = []

            selected = values["-FILE LIST-"]
            for idx, row in enumerate(data.iloc):
                str_selected = str(selected)
                if row['size unit'] in str_selected:
                   if row['side'] == "BUY":
                       without_fees.append(abs(row['total']))
                       fees.append(abs(row['fee']))
                       with_fees.append(abs(row['total']) + abs(row['fee']))
                       amount.append(abs(row['size']))
                       # coin_price.append(row['price'])
                       amount_price.append(abs(row['size'])*abs(row['price']))


            sum_without_fees = sum(without_fees)
            sum_fees = sum(fees)
            sum_with_fees = sum(with_fees)
            sum_amount = sum(amount)
            sum_amount_price = sum(amount_price)
            weighted_average = sum_amount_price/sum_amount

            # print(sum_without_fees)
            # print(sum_fees)
            # print(sum_with_fees)
            # print(sum_amount)
            # print(sum_amount_price)
            # print(weighted_average)

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
        # if price.isnumeric():

        amount_up_or_down = float(number_price) * sum_amount - sum_with_fees
        print(amount_up_or_down)

        window["-UP OR DOWN-"].update(amount_up_or_down)

        # else:
        #     print("only numbers please")

2
window.close()



