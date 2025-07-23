import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

# উইন্ডো তৈরি
class TicTacToeApp(App):
    def build(self):
        self.current_player = "X"
        self.board = [""] * 9

        # মূল লেআউট তৈরি
        self.root = BoxLayout(orientation='vertical', padding=10)
        
        # শিরোনাম লেবেল (সাইজ ঠিক করা হয়েছে)
        self.title_label = Label(text="Tic Tac Toe ", font_size=180, color=(1, 0, 0, 1), size_hint=(None, None), size=(1100, 200))
        self.root.add_widget(self.title_label)
        
        # বর্তমান প্লেয়ারের টার্ন (সাইজ ঠিক করা হয়েছে)
        self.current_player_label = Label(text="Player X's Turn ", font_size=100, color=(1, 1, 1, 1), size_hint=(None, None), size=(1100, 200))
        self.root.add_widget(self.current_player_label)
        
        # বোর্ড তৈরি
        self.buttons_layout = GridLayout(cols=3, padding=10, spacing=10)
        self.buttons = []
        
        for i in range(9):
            btn = Button(text="", font_size=180, size_hint=(None, None), size=(340,549),
                        background_normal="", background_color=(0.2, 0.2, 0.2, 2))
            btn.bind(on_press=lambda instance, i=i: self.update_board(i, instance))
            self.buttons.append(btn)
            self.buttons_layout.add_widget(btn)

        self.root.add_widget(self.buttons_layout)

        # রিসেট বোতাম
        self.reset_button = Button(text="Reset Game", font_size=100, size_hint=(None, None), size=(1100,200))
        self.reset_button.bind(on_press=self.reset_game)
        self.root.add_widget(self.reset_button)

        return self.root

    # বোর্ড আপডেট ফাংশন
    def update_board(self, index, button):
        if self.board[index] == "" and not self.check_winner():
            self.board[index] = self.current_player
            button.text = self.current_player
            button.color = (1, 1, 1, 1) if self.current_player == "X" else (1, 0.8, 0, 1)  # X = White, O = Yellow

            # বিজয়ী চেক করা
            winner_combo = self.check_winner()
            if winner_combo:
                self.highlight_winner(winner_combo)
                self.show_game_over_popup(f"                                Congratulations Player ' {self.current_player} ' Wins!")
                return
            elif "" not in self.board:  # যদি সব ঘর ভর্তি হয়ে যায় এবং কেউ না জেতে
                self.show_game_over_popup("                                Sorry, It's a Draw!")
                return

            # পরবর্তী প্লেয়ার পরিবর্তন
            self.current_player = "O" if self.current_player == "X" else "X"
            self.current_player_label.text = f"Player {self.current_player}'s Turn"

    # বিজয়ী নির্ধারণ ফাংশন
    def check_winner(self):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        
        for combo in winning_combinations:
            a, b, c = combo
            if self.board[a] == self.board[b] == self.board[c] and self.board[a] != "":
                return combo
        return None

    # বিজয়ীর ঘর হাইলাইট করা
    def highlight_winner(self, combo):
        for index in combo:
            self.buttons[index].background_color = (0, 1, 0, 1)  # বিজয়ীর ঘর সবুজ হবে

    # কাস্টম গেম ওভার পপআপ
    def show_game_over_popup(self, message):
        popup_layout = BoxLayout(orientation='vertical', padding=-29)

        game_over_label = Label(text=message, font_size=50, color=(1, 0, 0, 1), size_hint=(0,0.15), size=(480, 150),
                              halign="center", valign="middle")

        ok_button = Button(text="OK", size_hint=(None,None), size=(890,100))
        ok_button.bind(on_press=self.close_popup)

        popup_layout.add_widget(game_over_label)
        popup_layout.add_widget(ok_button)

        self.popup = Popup(title="                                 Game Over", content=popup_layout, size_hint=(None,None), size=(900, 500))
        self.popup.open()

    # পপআপ বন্ধ এবং গেম রিসেট
    def close_popup(self, instance):
        self.popup.dismiss()
        self.reset_game()

    # রিসেট ফাংশন
    def reset_game(self, instance=None):
        self.current_player = "X"
        self.board = [""] * 9
        self.current_player_label.text = f"Player {self.current_player}'s Turn"
        
        for button in self.buttons:
            button.text = ""
            button.background_color = (0.2,0.2,0.2, 2)

# অ্যাপ রান করা
if __name__ == '__main__':
    TicTacToeApp().run()
