import os
import sys

import trello

def get_trello_client(auth_values):
    api_key = auth_values["TRELLO_API_KEY"]
    api_secret = auth_values["TRELLO_API_SECRET"]
    oauth_token = auth_values["TRELLO_OAUTH_TOKEN"]
    oauth_secret = auth_values["TRELLO_OAUTH_SECRET"]

    return trello.TrelloClient(
        api_key=api_key,
        api_secret=api_secret,
        token=oauth_token,
        token_secret=oauth_secret
    )

def delete_all_cards(lst):

    for c in lst.list_cards():
        c.delete()
    
def find_list(board, list_name):
    return next(lst for lst in board.all_lists() if lst.name == list_name)

if __name__ =="__main__":

    client = get_trello_client(os.environ)

    board = trello.Board(client, 'o6VGLWv0')
    to_buy_list = find_list(board, "To Buy")

    delete_all_cards(to_buy_list)

    new_board_entries = sys.stdin.readlines()

    for entry in new_board_entries:
        entry.strip()
        card = to_buy_list.add_card(entry)
