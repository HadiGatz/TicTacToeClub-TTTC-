class TTTManager:
    board = ""
    
    def __init__(self, board):
        self.board = board # using the "Board" module
    
    def handle_user_turn(self, tile_type):
        while True:
            tile = int(input("Enter your tile: "))
            if self.board.check_tile(tile):
                self.board.set_tile(tile, tile_type)
                return tile

    def handle_game_ending(self, result):
        if result == "TIE":
            print("The game has ended with a TIE")
    
        else:
            print(result.replace("_", " "))

    
